### Windows platform

Source: [Windows](/codex/windows.md)

Use Codex on Windows with the native [Codex app](/codex/app/windows), the
[CLI](/codex/cli), or the [IDE extension](/codex/ide).

The Codex app on Windows supports core workflows such as parallel agent threads,
worktrees, automations, Git functionality, the in-app browser, artifact previews,
plugins, and skills.

Depending on the surface and your setup, Codex can run on Windows in three
practical ways:

- natively on Windows with the stronger `elevated` sandbox,
- natively on Windows with the fallback `unelevated` sandbox,
- or inside [Windows Subsystem for Linux 2](https://learn.microsoft.com/en-us/windows/wsl/install) (WSL2), which uses the Linux sandbox implementation.

#### Windows sandbox

When you run Codex natively on Windows, agent mode uses a Windows sandbox to
block filesystem writes outside the working folder and prevent network access
without your explicit approval.

Native Windows sandbox support includes two modes that you can configure in
`config.toml`:

```toml
[windows]
sandbox = "elevated" # or "unelevated"
```

`elevated` is the preferred native Windows sandbox. It uses dedicated
lower-privilege sandbox users, filesystem permission boundaries, firewall
rules, and local policy changes needed for commands that run in the sandbox.

`unelevated` is the fallback native Windows sandbox. It runs commands with a
restricted Windows token derived from your current user, applies ACL-based
filesystem boundaries, and uses environment-level offline controls instead of
the dedicated offline-user firewall rule. It's weaker than `elevated`, but it
is still useful when administrator-approved setup is blocked by local or
enterprise policy.

If both modes are available, use `elevated`. If the default native sandbox
doesn't work in your environment, use `unelevated` as a fallback while you
troubleshoot the setup.

Enterprise administrators can constrain which native sandbox implementations
Codex can use through [`requirements.toml`](/codex/enterprise/managed-configuration#admin-enforced-requirements-requirementstoml):

```toml
[windows]
allowed_sandbox_implementations = ["elevated"]
```

This example requires the `elevated` sandbox and prevents users from falling
back to `unelevated`. To permit either implementation, include both values;
Codex prefers `elevated` when no mode is selected. See the
[`requirements.toml` reference](/codex/config-reference#requirementstoml) for
the supported values.

By default, both sandbox modes also use a private desktop for stronger UI
isolation. Set `windows.sandbox_private_desktop = false` only if you need the
older `Winsta0\\Default` behavior for compatibility.

#### Sandbox permissions

Running Codex in full access mode means Codex is not limited to your project
directory and might perform unintentional destructive actions that can lead to
data loss. For safer automation, keep sandbox boundaries in place and use
[rules](/codex/rules) for specific exceptions, or set your [approval policy to
never](/codex/agent-approvals-security#run-without-approval-prompts) to have
Codex attempt to solve problems without asking for escalated permissions,
based on your [approval and security setup](/codex/agent-approvals-security).

#### Windows version matrix

| Windows version                  | Support level   | Notes                                                                                                                                                                                 |
| -------------------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Windows 11                       | Recommended     | Best baseline for Codex on Windows. Use this if you are standardizing an enterprise deployment.                                                                                       |
| Recent, fully updated Windows 10 | Best effort     | Can work, but is less reliable than Windows 11. For Windows 10, Codex depends on modern console support, including ConPTY. In practice, Windows 10 version 1809 or newer is required. |
| Older Windows 10 builds          | Not recommended | More likely to miss required console components such as ConPTY and more likely to fail in enterprise setups.                                                                          |

Additional environment assumptions:

- `winget` should be available. If it's missing, update Windows or install
  the Windows Package Manager before setting up Codex.
- The recommended native sandbox depends on administrator-approved setup.
- Some enterprise-managed devices block the required setup steps even when the
  OS version itself is acceptable.

#### Grant sandbox read access

When a command fails because the Windows sandbox can't read a directory, use:

```text
/sandbox-add-read-dir C:\absolute\directory\path
```

The path must be an existing absolute directory. After the command succeeds, later commands that run in the sandbox can read that directory during the current session.

Use the native Windows sandbox by default. The native Windows sandbox offers the best performance and highest speeds while keeping the same security. Choose WSL2 when you
need a Linux-native environment on Windows, when your workflow already lives in
WSL2, or when neither native Windows sandbox mode meets your needs.

#### Windows Subsystem for Linux

If you choose WSL2, Codex runs inside the Linux environment instead of using the
native Windows sandbox. This is useful if you need Linux-native tooling on
Windows, if your repositories and developer workflow already live in WSL2, or
if neither native Windows sandbox mode works for your environment.

WSL1 was supported through Codex `0.114`. Starting in Codex `0.115`, the Linux
sandbox moved to `bubblewrap`, so WSL1 is no longer supported.

#### Launch VS Code from inside WSL

For step-by-step instructions, see the [official VS Code WSL tutorial](https://code.visualstudio.com/docs/remote/wsl-tutorial).

#### Prerequisites

- Windows with WSL installed. To install WSL, open PowerShell as an administrator, then run `wsl --install` (Ubuntu is a common choice).
- VS Code with the [WSL extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl) installed.

#### Open VS Code from a WSL terminal

```bash
# From your WSL shell
cd ~/code/your-project
code .
```

This opens a WSL remote window, installs the VS Code Server if needed, and ensures integrated terminals run in Linux.

#### Confirm you're connected to WSL

- Look for the green status bar that shows `WSL: `.
- Integrated terminals should display Linux paths (such as `/home/...`) instead of `C:\`.
- You can verify with:

  ```bash
  echo $WSL_DISTRO_NAME
  ```

  This prints your distribution name.

If you don't see "WSL: ..." in the status bar, press `Ctrl+Shift+P`, pick
`WSL: Reopen Folder in WSL`, and keep your repository under `/home/...` (not
`C:\`) for best performance.

If the Windows app or project picker does not show your WSL repository, type
\\wsl$ into the file picker or Explorer, then navigate to your
distro's home directory.

#### Use Codex CLI with WSL

Run these commands from an elevated PowerShell or Windows Terminal:

```powershell
# Install default Linux distribution (like Ubuntu)
wsl --install

# Start a shell inside Windows Subsystem for Linux
wsl
```

Then run these commands from your WSL shell:

```bash
# Install and run Codex in WSL
curl -fsSL https://chatgpt.com/codex/install.sh | sh
codex
```

#### Working on code inside WSL

- Working in Windows-mounted paths like /mnt/c/... can be slower than working in Windows-native paths. Keep your repositories under your Linux home directory (like ~/code/my-app) for faster I/O and fewer symlink and permission issues:
  ```bash
  mkdir -p ~/code && cd ~/code
  git clone https://github.com/your/repo.git
  cd repo
  ```
- If you need Windows access to files, they're under \\wsl$\Ubuntu\home\&lt;user&gt; in Explorer.
