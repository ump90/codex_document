### Sites

Source: [Sites](/codex/sites.md)

Sites lets Codex create, save, deploy, and inspect websites, web apps, and
games hosted by OpenAI. Use the **Sites** plugin when you want to turn a prompt
or a compatible existing project into a hosted site without setting up a
separate deployment workflow.

Every Sites deployment URL is a production deployment. If you want to review a
build before it becomes live, ask Codex to save a version without deploying
it.

#### Understand projects, versions, and deployments

A Sites project links a local source project to hosting managed through Sites.
Codex stores that linkage and optional storage binding names in
`.openai/hosting.json`. A newly created local starter can begin without a
`project_id`; Sites adds one after it provisions the hosted project.

For example, a provisioned site that uses a relational database binding and no
file storage can contain:

```json
{
  "project_id": "",
  "d1": "DB",
  "r2": null
}
```

Sites publishing has two separate stages:

1. **Save a version.** Codex builds the deployable site and associates that
   version with the source Git commit used for the build. Use this stage when
   you want a reviewable deployment candidate.
2. **Deploy a version.** Codex publishes a saved version and reports the
   production URL when deployment succeeds. Use this only when you intend for
   the selected audience to access the site.

Ask Codex to list or inspect saved versions when you need to identify a
previous deployment candidate.

#### Choose a supported site shape

Sites hosts projects that build Cloudflare Worker-compatible output as ES
modules. For new projects, the Sites workflow can start with its recommended
site starter. For an existing site, ask Codex to confirm that the project's
build can produce compatible deployment artifacts before you request a
deployment.

Tell Codex about the product behavior you need so it can select the appropriate
site shape:

| Site need                                                      | What to ask Sites for                                                         |
| -------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Content-led website or landing page                            | A site with no persistent application state unless the experience requires it |
| Saved records, user progress, or game scores                   | D1, a relational database for durable structured data                         |
| Images, documents, audio, video, or other uploads              | R2, object storage for files                                                  |
| Uploaded files with searchable metadata                        | D1 for metadata and R2 for file contents                                      |
| Internal site that needs the current workspace user's identity | Workspace-authenticated user identity                                         |
| Public sign-in or an external identity provider                | An authentication-enabled Sites project                                       |

Don't request durable storage for temporary presentation state, such as a
theme choice or a dismissed banner. Do request it for product data that people
expect the hosted site to remember.

#### Control access and secrets

Set the audience before you share a deployed URL. For a new site, keep access
limited to the owner and workspace admins until you have reviewed the content,
data handling, and expected audience.

You can ask Sites to apply one of these access modes:

| Access mode                      | Who can access the site                                                                       |
| -------------------------------- | --------------------------------------------------------------------------------------------- |
| Owner and admins (`admins_only`) | The site owner and workspace admins                                                           |
| Workspace (`workspace_all`)      | All active users in the workspace                                                             |
| Custom (`custom`)                | Specific active users or workspace groups that you choose; Sites continues to allow the owner |

For example:

```text
@Sites Change this deployed site's access to everyone in my workspace after
showing me the current site and confirming the deployment URL.
```

#### Configure runtime environment values

Open **Sites** in the app sidebar and select a project to add, update, or remove
hosted environment variables and secrets in the Sites panel. Don't store these
values in `.openai/hosting.json`. Keep local `.env` and `.env.example` files
aligned with the keys needed for local development, and don't commit secret
values.

When you add, update, or remove hosted environment values, ask Codex to
redeploy the approved saved version so the next deployment uses the updated
configuration.

#### Review before you share

Before you deploy or widen access:

- Review the source changes and any database migrations in the Codex
  [review pane](/codex/app/review).
- Confirm that the build succeeded and that the selected saved version is the
  version you intend to publish.
- Check that only the intended audience can access the site.
- Confirm that you configured runtime secret values through Sites and didn't
  commit them in source files.
- After deployment, ask Codex to confirm deployment status and the production
  URL before you share it.

#### Related documentation

- [Plugins](/codex/plugins) explains how to install and invoke Codex plugins.
- [Codex app](/codex/app) introduces app navigation and project threads.
- [Review and ship changes](/codex/app/review) explains how to inspect source
  changes before publishing them.

