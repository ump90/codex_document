### Build plugins

Source: [Build plugins](/codex/plugins/build.md)

This page is for plugin authors. If you want to browse, install, and use
plugins in Codex, see [Plugins](/codex/plugins). If you are still iterating on
one repo or one personal workflow, start with a local skill. Build a plugin
when you want to share that workflow across teams, bundle app integrations or
MCP config, package lifecycle hooks, or publish a stable package.

#### Create a plugin with `@plugin-creator`

For the fastest setup, use the built-in `@plugin-creator` skill.

It scaffolds the required `.codex-plugin/plugin.json` manifest and can also
generate a local marketplace entry for testing. If you already have a plugin
folder, you can still use `@plugin-creator` to wire it into a local
marketplace.

#### Build your own curated plugin list

A marketplace is a JSON catalog of plugins. `@plugin-creator` can generate one
for a single plugin, and you can keep adding entries to that same marketplace
to build your own curated list for a repo, team, or personal workflow.

In Codex, each marketplace appears as a selectable source in the plugin
directory. Use `$REPO_ROOT/.agents/plugins/marketplace.json` for a repo-scoped
list or `~/.agents/plugins/marketplace.json` for a personal list. Add one
entry per plugin under `plugins[]`, point each `source.path` at the plugin
folder with a `./`-prefixed path relative to the marketplace root, and set
`interface.displayName` to the label you want Codex to show in the marketplace
picker. Then restart Codex. After that, open the plugin directory, choose your
marketplace, and browse or install the plugins in that curated list.

You don't need a separate marketplace per plugin. One marketplace can expose a
single plugin while you are testing, then grow into a larger curated catalog as
you add more plugins.

#### Add a marketplace from the CLI

Use `codex plugin marketplace add` when you want Codex to install and track a
marketplace source for you instead of editing `config.toml` by hand.

```bash
codex plugin marketplace add owner/repo
codex plugin marketplace add owner/repo --ref main
codex plugin marketplace add https://github.com/example/plugins.git --sparse .agents/plugins
codex plugin marketplace add ./local-marketplace-root
```

Marketplace sources can be GitHub shorthand (`owner/repo` or
`owner/repo@ref`), HTTP or HTTPS Git URLs, SSH Git URLs, or local marketplace root
directories. Use `--ref` to pin a Git ref, and repeat `--sparse PATH` to use a
sparse checkout for Git-backed marketplace repos. `--sparse` is valid only for
Git marketplace sources.

To inspect, refresh, or remove configured marketplaces:

```bash
codex plugin marketplace list
codex plugin marketplace upgrade
codex plugin marketplace upgrade marketplace-name
codex plugin marketplace remove marketplace-name
```

`codex plugin marketplace list` prints each marketplace Codex is considering
and the root path it resolves from, including local default marketplaces and
configured marketplace snapshots.

#### Create a plugin manually

Start with a minimal plugin that packages one skill.

1. Create a plugin folder with a manifest at `.codex-plugin/plugin.json`.

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

Use a stable plugin `name` in kebab-case. Codex uses it as the plugin
identifier and component namespace.

2. Add a skill under `skills//SKILL.md`.

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

3. Add the plugin to a marketplace. Use `@plugin-creator` to generate one, or
   follow [Build your own curated plugin list](#build-your-own-curated-plugin-list)
   to wire the plugin into Codex manually.

From there, you can add MCP config, app integrations, or marketplace metadata
as needed.

#### Install a local plugin manually

Use a repo marketplace or a personal marketplace, depending on who should be
able to access the plugin or curated list.

    Add a marketplace file at `$REPO_ROOT/.agents/plugins/marketplace.json`
    and store your plugins under `$REPO_ROOT/plugins/`.

    **Repo marketplace example**

    Step 1: Copy the plugin folder into `$REPO_ROOT/plugins/my-plugin`.

```bash
mkdir -p ./plugins
cp -R /absolute/path/to/my-plugin ./plugins/my-plugin
```

    Step 2: Add or update `$REPO_ROOT/.agents/plugins/marketplace.json` so
    that `source.path` points to that plugin directory with a `./`-prefixed
    relative path:

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

    Step 3: Restart Codex and verify that the plugin appears.

    Add a marketplace file at `~/.agents/plugins/marketplace.json` and store
    your plugins under `~/.codex/plugins/`.

    **Personal marketplace example**

    Step 1: Copy the plugin folder into `~/.codex/plugins/my-plugin`.

```bash
mkdir -p ~/.codex/plugins
cp -R /absolute/path/to/my-plugin ~/.codex/plugins/my-plugin
```

    Step 2: Add or update `~/.agents/plugins/marketplace.json` so that the
    plugin entry's `source.path` points to that directory.

    Step 3: Restart Codex and verify that the plugin appears.

The marketplace file points to the plugin location, so those directories are
examples rather than fixed requirements. Codex resolves `source.path` relative
to the marketplace root, not relative to the `.agents/plugins/` folder. See
[Marketplace metadata](#marketplace-metadata) for the file format.

After you change the plugin, update the plugin directory that your marketplace
entry points to and restart Codex so the local install picks up the new files.

#### Share a local plugin with your workspace

After you create a plugin and add it to Codex, you can share it with other
members of your ChatGPT workspace from the Codex app.

1. Open **Plugins** in the Codex app.
2. Go to **Created by you** and open the plugin details page.
3. Select **Share**.
4. Add workspace members or workspace groups, or copy a share link.
5. Choose who has access, then send the invitation or link.

People you share with can find the plugin under **Shared with you** in the
plugin directory. Sharing a local plugin with your workspace doesn't publish
it to the public Plugin Directory. Shared plugins stay within your workspace
and organization boundary; accounts that aren't signed in to that workspace
can't access them. Use groups when a team or role should share the same plugin
access. Use a marketplace when you want repo or CLI distribution, and use
workspace sharing when you want selected teammates to install a plugin from the
Codex app.

Workspace admins can disable plugin sharing from cloud-managed requirements by
adding `plugin_sharing = false` to `requirements.toml`:

```toml
plugin_sharing = false
```

