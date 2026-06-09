### Permissions

Source: [Permissions](/codex/permissions.md)

#### Define and select a profile

Codex includes three built-in permission profiles:

- `:read-only` keeps local command execution read-only.
- `:workspace` allows writes inside the active workspace roots and system temp directories.
- `:danger-full-access` removes local sandbox restrictions and should be used
  only when that broad access is intentional.

Create a named profile under `[permissions.]`, then set the top-level
`default_permissions` key to that profile name or to one of the built-ins above.
In this example, `project-edit` is a user-defined profile name, not a built-in
value.

Custom profiles use two related concepts:

- `[permissions..workspace_roots]` adds concrete directories that should
  count as workspace roots for that profile.
- `[permissions..filesystem.":workspace_roots"]` defines the filesystem
  rules Codex applies inside every effective workspace root: the current
  session's runtime workspace roots plus the profile-defined roots above.

Profiles also use the normal config-layer model. Higher-precedence layers can
add or replace entries under the same profile name without restating the whole
profile.

For example, an organization-level config and a user-level config can extend
the same profile independently:

```toml
# /etc/codex/config.toml
[permissions.server.workspace_roots]
"~/code/server" = true
```

```toml
# ~/.codex/config.toml
[permissions.server.workspace_roots]
"~/code/mobile-app" = true
```

When `server` is active, both workspace roots participate in the effective
profile.

```toml
default_permissions = "project-edit"

[permissions.project-edit.workspace_roots]
"~/code/app" = true
"~/code/shared-lib" = true

[permissions.project-edit.filesystem]
":minimal" = "read"

[permissions.project-edit.filesystem.":workspace_roots"]
"." = "write"
".devcontainer" = "read"
"**/*.env" = "deny"

[permissions.project-edit.network]
enabled = true

[permissions.project-edit.network.domains]
"api.openai.com" = "allow"
"objects.githubusercontent.com" = "allow"
"*.github.com" = "allow"
"tracking.example.com" = "deny"
```

This profile:

- Reads the minimal runtime paths common developer tools need.
- Applies the same workspace-root rules to the current session and the
  profile-defined roots.
- Keeps IDE-adjacent settings such as `.devcontainer/` read-only under each
  root.
- Denies matching environment files with a glob rule.
- Allows network access only through the configured domain policy.

Inside an active profile, narrower deny rules stay in force even when a broader
path is readable or writable. For example, a profile can make workspace roots
writable while still setting a matching `.env` path to `deny`.

#### Extend a profile

Use `extends` when a profile is mostly the same as a built-in or another named
profile. Prefer extending a built-in profile over starting from scratch so
baseline protections carry forward. Extending `:workspace`, for example, keeps
the workspace root's `.codex` directory read-only unless you explicitly
override it. Set the parent once, then add or override only the rules that
differ.

```toml
default_permissions = "project-edit"

[permissions.project-edit]
description = "Project editing with OpenAI API access."
extends = ":workspace"

[permissions.project-edit.filesystem.":workspace_roots"]
"**/*.env" = "deny"

[permissions.project-edit.network]
enabled = true

[permissions.project-edit.network.domains]
"api.openai.com" = "allow"
```

This profile starts with `:workspace`, keeps matching `.env` files denied, and
allows requests to `api.openai.com`. A profile can extend `:read-only`,
`:workspace`, or another named profile. It cannot extend
`:danger-full-access`; Codex also rejects unknown parents and inheritance
cycles.

