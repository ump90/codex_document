### 构建插件

Source: [Build plugins](https://developers.openai.com/codex/plugins/build.md)

本页面面向插件作者。如果你想在 Codex 中浏览、安装和使用
插件，请参阅 [Plugins](78-plugins.md)。如果你仍在迭代
一个仓库或一个个人工作流，请从本地技能开始。当你想跨团队共享该工作流、捆绑 app 集成或
MCP 配置、打包生命周期钩子，或发布稳定包时，再构建插件。

#### 使用 `@plugin-creator` 创建插件

最快的设置方式是使用内置 `@plugin-creator` 技能。

它会搭建必需的 `.codex-plugin/plugin.json` manifest，并且还可以
生成用于测试的本地 marketplace 条目。如果你已经有插件
文件夹，仍可使用 `@plugin-creator` 将其接入本地
marketplace。

#### 构建你自己的精选插件列表

Marketplace 是插件的 JSON 目录。`@plugin-creator` 可以为单个插件生成一个，
你也可以继续向同一个 marketplace 添加条目，
为仓库、团队或个人工作流构建自己的精选列表。

在 Codex 中，每个 marketplace 都会作为插件
目录中可选的来源显示。仓库作用域
列表使用 `$REPO_ROOT/.agents/plugins/marketplace.json`，个人列表使用 `~/.agents/plugins/marketplace.json`。在 `plugins[]` 下为每个插件添加一个
条目，将每个 `source.path` 指向插件
文件夹，路径相对于 marketplace 根目录，并以 `./` 为前缀；设置
`interface.displayName` 为你希望 Codex 在 marketplace
选择器中显示的标签。然后重启 Codex。之后，打开插件目录，选择你的
marketplace，并浏览或安装该精选列表中的插件。

每个插件不需要单独的 marketplace。一个 marketplace 可以在
你测试时暴露单个插件，随后随着你添加更多插件，
扩展为更大的精选目录。

#### 从 CLI 添加市场

当你希望 Codex 为你安装并跟踪
marketplace 来源，而不是手动编辑 `config.toml` 时，请使用 `codex plugin marketplace add`。

```bash
codex plugin marketplace add owner/repo
codex plugin marketplace add owner/repo --ref main
codex plugin marketplace add https://github.com/example/plugins.git --sparse .agents/plugins
codex plugin marketplace add ./local-marketplace-root
```

Marketplace 来源可以是 GitHub 简写（`owner/repo` 或
`owner/repo@ref`）、HTTP 或 HTTPS Git URL、SSH Git URL，或本地 marketplace 根
目录。使用 `--ref` 固定 Git ref，并可重复 `--sparse PATH` 来为 Git 后端的 marketplace 仓库使用
稀疏 checkout。`--sparse` 只对
Git marketplace 来源有效。

要检查、刷新或移除已配置的 marketplace：

```bash
codex plugin marketplace list
codex plugin marketplace upgrade
codex plugin marketplace upgrade marketplace-name
codex plugin marketplace remove marketplace-name
```

`codex plugin marketplace list` 会打印 Codex 正在考虑的每个 marketplace
以及它解析出的根路径，包括本地默认 marketplace 和
已配置的 marketplace 快照。

#### 手动创建插件

从打包一个技能的最小插件开始。

1. 创建包含 `.codex-plugin/plugin.json` manifest 的插件文件夹。

```bash
mkdir -p my-first-plugin/.codex-plugin
```

`my-first-plugin/.codex-plugin/plugin.json`

```json
{
  "name": "my-first-plugin",
  "version": "1.0.0",
  "description": "Reusable greeting workflow",
  "skills": "./skills/"
}
```

使用 kebab-case 的稳定插件 `name`。Codex 会将其用作插件
标识符和组件命名空间。

2. 在 `skills//SKILL.md` 下添加 skill。

```bash
mkdir -p my-first-plugin/skills/hello
```

`my-first-plugin/skills/hello/SKILL.md`

```md
---
name: hello
description: Greet the user with a friendly message.
---

Greet the user warmly and ask how you can help.
```

3. 将插件添加到 marketplace。使用 `@plugin-creator` 生成一个，或
   按照 [Build your own curated plugin list](#build-your-own-curated-plugin-list)
   将插件手动接入 Codex。

从这里开始，你可以按需添加 MCP 配置、app 集成或 marketplace 元数据。

#### 手动安装本地插件

根据谁应能访问该插件或精选列表，使用仓库 marketplace 或个人 marketplace。

    在 `$REPO_ROOT/.agents/plugins/marketplace.json` 添加 marketplace 文件，
    并将插件存放在 `$REPO_ROOT/plugins/` 下。

    **仓库 marketplace 示例**

    Step 1: 将插件文件夹复制到 `$REPO_ROOT/plugins/my-plugin`。

```bash
mkdir -p ./plugins
cp -R /absolute/path/to/my-plugin ./plugins/my-plugin
```

    Step 2: 添加或更新 `$REPO_ROOT/.agents/plugins/marketplace.json`，使
    `source.path` 指向该插件目录，并使用以 `./` 为前缀的
    相对路径：

```json
{
  "name": "local-repo",
  "plugins": [
    {
      "name": "my-plugin",
      "source": {
        "source": "local",
        "path": "./plugins/my-plugin"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

    Step 3: 重启 Codex 并确认插件出现。

    在 `~/.agents/plugins/marketplace.json` 添加 marketplace 文件，并将
    插件存放在 `~/.codex/plugins/` 下。

    **个人 marketplace 示例**

    Step 1: 将插件文件夹复制到 `~/.codex/plugins/my-plugin`。

```bash
mkdir -p ~/.codex/plugins
cp -R /absolute/path/to/my-plugin ~/.codex/plugins/my-plugin
```

    Step 2: 添加或更新 `~/.agents/plugins/marketplace.json`，使
    插件条目的 `source.path` 指向该目录。

    Step 3: 重启 Codex 并确认插件出现。

Marketplace 文件指向插件位置，因此这些目录是
示例，而不是固定要求。Codex 会相对于 marketplace 根目录解析 `source.path`，
而不是相对于 `.agents/plugins/` 文件夹。文件格式请参阅
[Marketplace metadata](#marketplace-metadata)。

更改插件后，请更新 marketplace
条目指向的插件目录，并重启 Codex，使本地安装获取新文件。

#### 与你的工作区共享本地插件

创建插件并将其添加到 Codex 后，你可以从 Codex app
将其共享给 ChatGPT 工作区的其它成员。

1. 在 Codex app 中打开 **Plugins**。
2. 前往 **Created by you** 并打开插件详情页。
3. 选择 **Share**。
4. 添加工作区成员或工作区组，或复制分享链接。
5. 选择谁有访问权限，然后发送邀请或链接。

你共享的人可以在插件目录的 **Shared with you** 下找到该插件。与工作区共享本地插件不会将其发布到公共 Plugin Directory。共享插件会保留在你的工作区
和组织边界内；未登录该工作区的账户
无法访问。团队或角色应共享相同插件
访问权限时，请使用组。当你想要仓库或 CLI 分发时，请使用 marketplace；当你希望选定队友从
Codex app 安装插件时，请使用
工作区共享。

工作区管理员可以通过在 `requirements.toml` 中添加 `plugin_sharing = false`，从云托管要求禁用插件共享：

```toml
plugin_sharing = false
```
