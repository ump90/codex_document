### Example workflows

Source: [Workflows](/codex/workflows.md)

Codex works best when you treat it like a teammate with explicit context and a clear definition of "done."
This page gives end-to-end workflow examples for the Codex IDE extension, the Codex CLI, and Codex cloud.

If you are new to Codex, read [Prompting](/codex/prompting) first, then come back here for concrete recipes.

#### How to read these examples

Each workflow includes:

- **When to use it** and which Codex surface fits best (IDE, CLI, or cloud).
- **Steps** with example user prompts.
- **Context notes**: what Codex automatically sees vs what you should attach.
- **Verification**: how to check the output.

> **Note:** The IDE extension automatically includes your open files as context. In the CLI, you usually need to mention paths explicitly (or attach files with `/mention` and `@` path autocomplete).

---

#### Explain a codebase

Use this when you are onboarding, inheriting a service, or trying to reason about a protocol, data model, or request flow.

#### Recipe: explain a codebase in IDE

1. Open the most relevant files.
2. Select the code you care about (optional but recommended).
3. Prompt Codex:

   ```text
   Explain how the request flows through the selected code.

   Include:
   - a short summary of the responsibilities of each module involved
   - what data is validated and where
   - one or two "gotchas" to watch for when changing this
   ```

Verification:

- Ask for a diagram or checklist you can validate quickly:

```text
Summarize the request flow as a numbered list of steps. Then list the files involved.
```

#### Recipe: explain a codebase in CLI

1. Start an interactive session:

   ```bash
   codex
   ```

2. Attach the files (optional) and prompt:

   ```text
   I need to understand the protocol used by this service. Read @foo.ts @schema.ts and explain the schema and request/response flow. Focus on required vs optional fields and backward compatibility rules.
   ```

Context notes:

- You can use `@` in the composer to insert file paths from the workspace, or `/mention` to attach a specific file.

---

#### Fix a bug

Use this when you have a failing behavior you can reproduce locally.

#### Recipe: fix a bug in CLI

1. Start Codex at the repo root:

   ```bash
   codex
   ```

2. Give Codex a reproduction recipe, plus the file(s) you suspect:

   ```text
   Bug: Clicking "Save" on the settings screen sometimes shows "Saved" but doesn't persist the change.

   Repro:
   1) Start the app: npm run dev
   2) Go to /settings
   3) Toggle "Enable alerts"
   4) Click Save
   5) Refresh the page: the toggle resets

   Constraints:
   - Do not change the API shape.
   - Keep the fix minimal and add a regression test if feasible.

   Start by reproducing the bug locally, then propose a patch and run checks.
   ```

Context notes:

- Supplied by you: the repro steps and constraints (these matter more than a high-level description).
- Supplied by Codex: command output, discovered call sites, and any stack traces it triggers.

Verification:

- Codex should re-run the repro steps after the fix.
- If you have a standard check pipeline, ask it to run it:

```text
After the fix, run lint + the smallest relevant test suite. Report the commands and results.
```

#### Recipe: fix a bug in IDE

1. Open the file where you think the bug lives, plus its nearest caller.
2. Prompt Codex:

   ```text
   Find the bug causing "Saved" to show without persisting changes. After proposing the fix, tell me how to verify it in the UI.
   ```

---

#### Write a test

Use this when you want to be very explicit about the scope you want tested.

#### Recipe: write a test in IDE

1. Open the file with the function.
2. Select the lines that define the function. Choose "Add to Codex Thread" from command palette to add these lines to the context.
3. Prompt Codex:

   ```text
   Write a unit test for this function. Follow conventions used in other tests.
   ```

Context notes:

- Supplied by "Add to Codex Thread" command: the selected lines (this is the "line number" scope), plus open files.

#### Recipe: write a test in CLI

1. Start Codex:

   ```bash
   codex
   ```

2. Prompt with a function name:

   ```text
   Add a test for the invert_list function in @transform.ts. Cover the happy path plus edge cases.
   ```

---

#### Prototype from a screenshot

Use this when you have a design mock, screenshot, or UI reference and you want a working prototype quickly.

