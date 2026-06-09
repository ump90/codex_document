### 规则

Source: [Rules](https://developers.openai.com/codex/rules.md)

使用 rules 控制 Codex 可以在沙箱外运行哪些命令。

Rules 是实验性的，可能会变化。

#### 创建规则文件

1. 在活动配置层旁边的 `rules/` 文件夹下创建 `.rules` 文件（例如 `~/.codex/rules/default.rules`）。
2. 添加一条 rule。此示例会在允许 `gh pr view` 在沙箱外运行之前提示。

   ```python
   # Prompt before running commands with the prefix `gh pr view` outside the sandbox.
   prefix_rule(
       # The prefix to match.
       pattern = ["gh", "pr", "view"],

       # The action to take when Codex requests to run a matching command.
       decision = "prompt",

       # Optional rationale for why this rule exists.
       justification = "Viewing PRs is allowed with approval",

       # `match` and `not_match` are optional "inline unit tests" where you can
       # provide examples of commands that should (or should not) match this rule.
       match = [
           "gh pr view 7888",
           "gh pr view --repo openai/codex",
           "gh pr view 7888 --json title,body,comments",
       ],
       not_match = [
           # Does not match because the `pattern` must be an exact prefix.
           "gh pr --repo openai/codex view 7888",
       ],
   )
   ```

3. 重启 Codex。

Codex 会在启动时扫描每个活动配置层下的 `rules/`，包括 [Team Config](64-admin-setup.md#team-config) 位置，以及位于 `~/.codex/rules/` 的用户层。项目本地 `/.codex/rules/` 只有在项目 `.codex/` 层受信任时才会加载。

当你在 TUI 中把命令添加到允许列表时，Codex 会写入用户层的 `~/.codex/rules/default.rules`，使未来运行可以跳过提示。

启用 Smart approvals（默认）时，Codex 可能会在升级权限请求期间为你提出 `prefix_rule`。接受前请仔细审查建议的 prefix。

管理员还可以从 [`requirements.toml`](67-managed-configuration.md#admin-enforced-requirements-requirementstoml) 强制执行限制性 `prefix_rule` 条目。

#### 理解规则字段

`prefix_rule()` 支持以下字段：

- `pattern` **（必需）**：定义要匹配的命令 prefix 的非空列表。每个元素可以是：
  - 字面字符串（例如 `"pr"`）。
- `decision` **（默认为 `"allow"`）**：rule 匹配时采取的操作。当多条 rules 匹配时，Codex 会应用最严格的 decision（`forbidden` > `prompt` > `allow`）。
  - `allow`：无需提示，在沙箱外运行命令。
  - `prompt`：每次匹配调用前提示。
  - `forbidden`：不提示，直接阻止请求。
- `justification` **（可选）**：说明该 rule 存在原因的非空、人类可读文本。Codex 可能会在审批提示或拒绝消息中显示它。当使用 `forbidden` 时，请在适当情况下在 justification 中包含建议的替代方案（例如 `"Use \`rg\` instead of \`grep\`."`）。
- `match` 和 `not_match` **（默认为 `[]`）**：Codex 加载你的 rules 时会验证的示例。使用它们在 rule 生效前捕获错误。

当 Codex 考虑运行命令时，它会将命令的参数列表与 `pattern` 比较。在内部，Codex 会把命令视为参数列表（类似 `execvp(3)` 接收的内容）。

#### Shell 包装器和复合命令

有些工具会把多个 shell 命令包装成一次调用，例如：

```text
["bash", "-lc", "git add . && rm -rf /"]
```

因为这种命令可能把多个操作隐藏在一个字符串中，Codex 会特别处理 `bash -lc`、`bash -c` 以及它们的 `zsh` / `sh` 等价形式。

#### Codex 何时可以安全拆分脚本

如果 shell 脚本是只由以下内容组成的线性命令链：

- 普通词（没有变量展开，没有 `VAR=...`、`$FOO`、`*` 等）
- 通过安全运算符（`&&`、`||`、`;` 或 `|`）连接

那么 Codex 会解析它（使用 tree-sitter），并在应用你的 rules 之前将其拆分成单独命令。

上面的脚本会被视为两个独立命令：

- `["git", "add", "."]`
- `["rm", "-rf", "/"]`

然后 Codex 会根据你的 rules 评估每个命令，并采用最严格的结果。

即使你允许 `pattern=["git", "add"]`，Codex 也不会自动允许 `git add . && rm -rf /`，因为 `rm -rf /` 部分会被单独评估，并阻止整个调用被自动允许。

这可以防止危险命令与安全命令一起被夹带进来。

#### Codex 何时不会拆分脚本

如果脚本使用更高级的 shell 特性，例如：

- 重定向（`>`、`>>`、`<`）
- 替换（`$(...)`、`...`）
- 环境变量（`FOO=bar`）
- 通配符模式（`*`、`?`）
- 控制流（`if`、`for`、带赋值的 `&&` 等）

那么 Codex 不会尝试解释或拆分它。

在这些情况下，整个调用会被视为：

```text
["bash", "-lc", ""]
```

你的 rules 会应用到这个**单一**调用。

通过这种处理方式，在安全时可以获得按命令评估的安全性；在不安全时则采用保守行为。

#### 测试规则文件

使用 `codex execpolicy check` 测试你的 rules 如何应用到某个命令：

```shell
codex execpolicy check --pretty \
  --rules ~/.codex/rules/default.rules \
  -- gh pr view 7888 --json title,body,comments
```

该命令会输出 JSON，显示最严格的 decision 以及任何匹配的 rules，包括已匹配 rules 中的任何 `justification` 值。使用多个 `--rules` 标志可以组合文件，添加 `--pretty` 可格式化输出。

#### 理解规则语言

`.rules` 文件格式使用 `Starlark`（参见 [language spec](https://github.com/bazelbuild/starlark/blob/master/spec.md)）。它的语法类似 Python，但被设计为安全运行：rules engine 可以在没有副作用的情况下运行它（例如，不触碰文件系统）。
