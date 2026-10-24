---
name: pi-docs
description: Local knowledge base mirroring the official Pi Coding Agent documentation and examples. Use when using, configuring, extending (extensions, skills, prompt templates, themes, packages, custom providers, virtual models), automating (print/JSON/RPC modes), or embedding (TypeScript SDK) the Pi Coding Agent (`pi` CLI, `@earendil-works/pi-coding-agent`).
metadata:
  author: Ecat
  version: "1.5.0"
  source: https://github.com/earendil-works/pi/tree/main/packages/coding-agent
---

# Pi Docs Skill

Offline mirror of the official Pi Coding Agent docs and examples. Use it for setup, configuration, API references, and reference implementations when using, extending, or embedding Pi.

## How to Use This Skill

1. **Start from the map below.** For a general overview, open [`docs/index.md`](docs/index.md).
2. **Trust the local files over memory.** Pi's APIs change often. Before writing code, check the exact names, event types, and option fields in `docs/`.
3. **Search, don't skim.** Grep `docs/` and `examples/` for API names such as `registerTool`, `registerVirtualModel`, `createAgentSession`, or `extension_ui_request`.
4. **Copy patterns from examples.** Find the closest example in `examples/` and adapt it rather than writing from scratch.

Main npm packages: `@earendil-works/pi-coding-agent` (agent, SDK, extension API), `@earendil-works/pi-ai` (models, `getModel`, `StringEnum`), `@earendil-works/pi-tui` (terminal UI components).

---

## 📚 `docs/` Documentation Map (42 files)

### 1. Getting Started & Interactive Usage
- [`index.md`](docs/index.md): Landing page and entry points to all other docs.
- [`quickstart.md`](docs/quickstart.md): Install, start, pick a model, run a first task, choose a customization method, uninstall.
- [`usage.md`](docs/usage.md): Writing prompts, following Pi's work, changing direction (steering, aborting), running terminal commands (`!`), copy/export/share, diagnostics.
- [`slash-commands.md`](docs/slash-commands.md): Built-in slash commands (`/model`, `/settings`, `/tree`, `/fork`, `/compact`, `/mcp`, `/trust`, `/reload`, ...).
- [`keybindings.md`](docs/keybindings.md): Assigning keybindings, key syntax, list of actions.
- [`themes.md`](docs/themes.md): Using terminal colors, picking or creating themes, theme file format, loading themes from projects or packages.

### 2. Core Concepts & Sessions
- [`how-pi-works.md`](docs/how-pi-works.md): Agent loop, how context is built, session tree, interfaces, extensions and resources, trust and permissions.
- [`sessions.md`](docs/sessions.md): Continuing and switching sessions, branching, managing context, storage, export/share, bug reports.
- [`session-format.md`](docs/session-format.md): JSONL session file format: location, versioning, entry base and types, tree structure, context building, parsing example.
- [`compaction.md`](docs/compaction.md): Compaction and branch summarization, summary format, custom summarization via extensions, settings.
- [`message-types.md`](docs/message-types.md): Content blocks, usage, base and coding-agent messages, the `AgentMessage` union.

### 3. Extensibility & Customization
- [`extensions.md`](docs/extensions.md): Writing and loading extensions, runtime lifecycle, choosing an integration point, extension contracts.
- [`skills.md`](docs/skills.md): Writing skills, how skills load, portable frontmatter, validating and sharing.
- [`prompt-templates.md`](docs/prompt-templates.md): Writing, using, and loading prompt templates.
- [`packages.md`](docs/packages.md): Pi packages (`pi install/list/remove/update`): sources, writing a package, dependencies, choosing which resources to include, scope.
- [`tui.md`](docs/tui.md): Terminal UI: integration points, component model, built-in components, keyboard/mouse input and focus, custom screens and overlays, themes, keeping rendering responsive.

### 4. Advanced Capabilities
- [`codemode.md`](docs/codemode.md): The `codemode` tool. The model writes JavaScript that runs in a QuickJS sandbox and calls tools and non-LLM models; covers globals, stored values, and limits.
- [`mcp.md`](docs/mcp.md): MCP servers (stdio and HTTP): setup (`pi mcp add/list`), config files, migrating from other clients, OAuth, controlling tool exposure, resources, permissions, use from extensions and the SDK.
- [`virtual-models.md`](docs/virtual-models.md): Virtual models (`registerVirtualModel`): selection vs. dispatch, request routing, routing state.

### 5. Models, Providers & Local Inference
- [`models.md`](docs/models.md): Picking a connection, authenticating, selecting models, local models, compatible endpoints, classifier and image models.
- [`providers.md`](docs/providers.md): Logging in interactively, API keys from env vars or commands, provider-specific config (e.g., AWS Bedrock, Google Cloud).
- [`models-configuration.md`](docs/models-configuration.md): `models.json` schema: providers, models, model overrides, input limits, compatibility settings.
- [`custom-provider.md`](docs/custom-provider.md): Custom providers: registration, auth, fetching and refreshing models, reusing or writing streaming, reporting errors and usage, testing.
- [`llama-cpp.md`](docs/llama-cpp.md): llama.cpp router: start it, configure Pi, manage models (`/llama`), classification, troubleshooting.
- [`nvidia-rtx-llama-cpp.md`](docs/nvidia-rtx-llama-cpp.md): Turn NVIDIA RTX recipes into llama.cpp router presets.

### 6. Automation & Embedding
- [`cli.md`](docs/cli.md): CLI reference: invocation and output, models, sessions, tools, resources, and the package, credential, and MCP subcommands.
- [`cli-integration.md`](docs/cli-integration.md): Choosing a mode (Interactive / Print / JSON / RPC), forking and rebranding Pi.
- [`sdk.md`](docs/sdk.md): TypeScript SDK: session lifecycle, prompting, subscribing to events, configuring sessions, resources.
- [`rpc.md`](docs/rpc.md): RPC mode: startup, protocol records, framing, run lifecycle, errors, shutdown, a minimal client.
- [`rpc-commands.md`](docs/rpc-commands.md): RPC command reference: prompting, state, model, thinking, queue modes, compaction, retry, bash, session, discoverable commands.
- [`rpc-extension-ui.md`](docs/rpc-extension-ui.md): Extension UI over RPC: dialog and fire-and-forget requests, responses, limitations.
- [`json.md`](docs/json.md): JSON event stream: framing, session header, the order and types of events, TypeScript types.

### 7. Configuration & Platform Setup
- [`configuration.md`](docs/configuration.md): Agent directory (`~/.pi/agent/`), project `.pi/` directory, context files.
- [`settings.md`](docs/settings.md): `settings.json` reference: model/thinking, interaction, tools, sessions, display, network/retries, shell, resources, updates/telemetry.
- [`environment-variables.md`](docs/environment-variables.md): Process marker, environment of the shell tool's session, Pi process configuration.
- [`shell-aliases.md`](docs/shell-aliases.md): Which shell Pi uses, `shellPath`, `shellCommandPrefix`, enabling Bash aliases.
- [`terminal-setup.md`](docs/terminal-setup.md): Per-terminal setup (Kitty, iTerm2, Ghostty, WezTerm, Alacritty, VS Code, Zed, Windows Terminal, IntelliJ, ...), overriding detected capabilities.
- [`windows.md`](docs/windows.md): Native Windows vs. WSL, Git Bash, PowerShell tool, custom Bash, Windows Terminal.
- [`tmux.md`](docs/tmux.md): Extended keys setup for tmux 3.2 and later.
- [`termux.md`](docs/termux.md): Android/Termux install, shared storage, clipboard, troubleshooting.

### 8. Security & Isolation
- [`security.md`](docs/security.md): Ways to run Pi, project trust, limiting damage and recovering from mistakes, reporting security issues.
- [`containerization.md`](docs/containerization.md): Isolation options: plain Docker, Docker Sandboxes, OpenShell, Gondolin micro-VM.

---

## 💡 `examples/` Code Examples Catalog

### Process & RPC Integration (`examples/`)
- [`rpc-client.ts`](examples/rpc-client.ts): Runs Pi as a child process with the typed `RpcClient`, streams events, and waits with `promptAndWait()`.
- [`rpc-extension-ui.ts`](examples/rpc-extension-ui.ts): A small TUI chat client built on RPC that handles extension UI dialogs. Use it together with `extensions/rpc-demo.ts`.
- [`README.md`](examples/README.md): Overview of all examples.

### SDK Examples (`examples/sdk/`)
Embedding Pi with `createAgentSession()` / `createAgentSessionRuntime()`. See [`sdk/README.md`](examples/sdk/README.md) for a quick reference and the options table.

| File | Description |
|---|---|
| `01-minimal.ts` | All defaults |
| `02-custom-model.ts` | Choosing a model and thinking level |
| `03-custom-prompt.ts` | Replacing or changing the system prompt |
| `04-skills.ts` | Finding, filtering, or replacing skills |
| `05-tools.ts` | Allowlisting built-in tools |
| `06-extensions.ts` | Logging, blocking, and modifying results |
| `07-context-files.ts` | `AGENTS.md` context files |
| `08-prompt-templates.ts` | File-based prompt templates |
| `09-api-keys-and-oauth.ts` | Resolving API keys, OAuth config |
| `10-settings.ts` | Overriding compaction, retry, and terminal settings |
| `11-sessions.ts` | In-memory, persistent, continued, and listed sessions |
| `12-full-control.ts` | Everything configured by hand, no discovery |
| `13-session-runtime.ts` | Replacing runtime-backed sessions when the cwd changes |
| `14-codemode-mcp.ts` | `codemode`, `tool_search`, and MCP extensions |

### Extension Examples (`examples/extensions/`)
About 80 examples. [`extensions/README.md`](examples/extensions/README.md) has the full table and key patterns: use `StringEnum` for Google compatibility, and persist state in tool result `details`. Load an example with `pi -e examples/extensions/<file>.ts`.

#### Lifecycle & Safety
- `permission-gate.ts`: Asks for confirmation before dangerous bash commands.
- `protected-paths.ts`: Blocks writes to `.env`, `.git/`, and `node_modules/`.
- `confirm-destructive.ts`: Asks before clearing, switching, or forking a session.
- `dirty-repo-guard.ts`: Prevents session changes while git has uncommitted changes.
- `project-trust.ts`: The `project_trust` event.
- `bash-spawn-hook.ts`: Changes the command, cwd, and env before bash runs (`createBashTool`).
- `timed-confirm.ts`: Auto-closes `confirm()`/`select()` with an `AbortSignal`.
- `sandbox/`: OS-level sandboxing via `@anthropic-ai/sandbox-runtime`.
- `gondolin/`: Sends built-in tools and `!` commands into a Gondolin micro-VM.

#### Custom Tools & Subagents
- `hello.ts`: Smallest possible custom tool.
- `todo.ts`: Todo tool plus `/todos`, with custom rendering and state persistence.
- `question.ts` / `questionnaire.ts`: Asking the user one question, or several in a tabbed form.
- `tool-override.ts`: Overrides built-in tools (e.g., adds logging to `read`).
- `dynamic-tools.ts`: Registers tools at runtime, with prompt snippets and guidelines.
- `structured-output.ts`: A final tool that returns `terminate: true`.
- `built-in-tool-renderer.ts` / `minimal-mode.ts`: Compact or minimal rendering of built-in tools.
- `truncated-tool.ts`: Wraps ripgrep and truncates output at 50KB / 2000 lines.
- `ssh.ts`: Runs all tools on a remote host over SSH.
- `subagent/`: Hands tasks to subagents, each with its own context.

#### Commands & Input
- `commands.ts`: `/commands` lists every slash command via `pi.getCommands()`.
- `preset.ts`: Named presets (`--preset`, `/preset`) for model, thinking, tools, and instructions.
- `plan-mode/`: Read-only plan mode (`/plan`) with step tracking.
- `tools.ts`: `/tools` turns tools on and off; the choice persists with the session.
- `handoff.ts`: `/handoff <goal>` moves the context into a new session.
- `qna.ts`: Copies questions from the last response into the editor.
- `send-user-message.ts`: `pi.sendUserMessage()` with steer and followUp delivery.
- `input-transform.ts`: Rewrites or answers input in the `input` event (`?quick`, `ping`).
- `input-transform-streaming.ts`: Skips heavy preprocessing for mid-stream steering.
- `inline-bash.ts`: Expands `!{command}` inside prompts.
- `interactive-shell.ts`: Runs vim/htop through the `user_bash` hook.
- `github-issue-autocomplete.ts`: `#1234` issue completion through a custom autocomplete provider.
- `shutdown-command.ts`: `/quit` using `ctx.shutdown()`.
- `reload-runtime.ts`: `/reload-runtime` and a `reload_runtime` tool.

#### TUI & Display
- `custom-footer.ts` / `custom-header.ts` / `status-line.ts`: Footer, header, and status bar.
- `widget-placement.ts`: Widgets above or below the editor.
- `model-status.ts`: Shows model changes through the `model_select` hook.
- `system-prompt-header.ts`: Status widget showing the length of `ctx.getSystemPrompt()`.
- `hidden-thinking-label.ts` / `working-indicator.ts`: Thinking label and working indicator.
- `working-message-test.ts`: Checks that a custom working message persists.
- `modal-editor.ts` / `rainbow-editor.ts` / `border-status-editor.ts`: Custom editors (vim-like modal, rainbow, status in the border).
- `notify.ts` / `titlebar-spinner.ts`: Desktop notification (OSC 777) and a title bar spinner.
- `summarize.ts`: Summary of the conversation shown in a temporary UI.
- `overlay-test.ts` / `overlay-qa-tests.ts`: Overlay compositing tests.
- `rpc-demo.ts`: Calls every UI method that RPC supports.

#### Git
- `git-checkpoint.ts`: A stash checkpoint every turn, for restoring on fork.
- `auto-commit-on-exit.ts`: Commits on exit, using the last assistant message as the commit message.
- `git-merge-and-resolve.ts`: Fetches and merges upstream after each turn and sends merge conflicts to the agent to resolve.

#### System Prompt & Compaction
- `pirate.ts`: `systemPromptAppend`.
- `prompt-customizer.ts`: Prompt sections that depend on context, via `systemPromptOptions`.
- `claude-rules.ts`: Adds `.claude/rules/` to the system prompt.
- `custom-compaction.ts` / `trigger-compact.ts`: Custom compaction; automatic compaction above 100k tokens.

#### Messages, Events & Session Metadata
- `message-renderer.ts` / `entry-renderer.ts`: Custom renderers for messages and session entries.
- `event-bus.ts`: Communication between extensions via `pi.events`.
- `session-name.ts` / `bookmark.ts`: Session names; labels for `/tree`.

#### Providers & Model Routing
- `custom-provider-anthropic/`: Custom provider with OAuth and its own streaming.
- `custom-provider-gitlab-duo/`: GitLab Duo through a proxy.
- `jev-router.ts`: Virtual model `jev/auto`. It plans on Sol or Terra (picked by a classifier), then switches to Luna after the first edit.
- `provider-payload.ts`: Logs or replaces provider payloads (`before_provider_request` / `after_provider_response`).
- `debug-provider.ts`: `/debug-provider` captures the raw provider stream.

#### Resources, Integration & Dependencies
- `dynamic-resources/`: Loads skills, prompts, and themes via `resources_discover`.
- `file-trigger.ts`: Watches a file and adds its contents to the conversation.
- `mac-system-theme.ts`: Follows macOS dark/light mode.
- `with-deps/`: Extension with its own `package.json` dependencies.

#### Games
- `snake.ts`, `space-invaders.ts`, `tic-tac-toe.ts` (sequential `executionMode` tools), `doom-overlay/` (35 FPS overlay).

---

## 🎯 Quick Task Lookup

| Task | Docs | Examples |
|---|---|---|
| Write an extension / custom tool | `extensions.md` | `hello.ts`, `todo.ts` |
| Add slash commands or change input | `extensions.md`, `slash-commands.md` | `commands.ts`, `input-transform.ts` |
| Build custom TUI or overlays | `tui.md` | `modal-editor.ts`, `overlay-test.ts` |
| Gate dangerous actions | `security.md`, `extensions.md` | `permission-gate.ts`, `protected-paths.ts` |
| Embed Pi in Node.js/TS | `sdk.md` | `sdk/01-minimal.ts` … `sdk/14-codemode-mcp.ts` |
| Drive Pi from another process | `cli-integration.md`, `rpc.md`, `rpc-commands.md`, `json.md` | `rpc-client.ts`, `rpc-extension-ui.ts` |
| Connect MCP servers / codemode | `mcp.md`, `codemode.md` | `sdk/14-codemode-mcp.ts` |
| Route between models | `virtual-models.md` | `jev-router.ts` |
| Add a provider or endpoint | `custom-provider.md`, `models-configuration.md` | `custom-provider-*/` |
| Run local models | `llama-cpp.md`, `nvidia-rtx-llama-cpp.md` | — |
| Ship resources as a package | `packages.md`, `skills.md` | `with-deps/`, `dynamic-resources/` |
