---
name: opencode-docs
description: Local knowledge base mirroring the official OpenCode AI coding agent documentation V2.
metadata:
  author: Ecat
  version: "2.1.4"
---

# OpenCode Documentation (v2)

## ⚠️ Important Note on References

Because this documentation is a local mirror of the official OpenCode documentation (`https://opencode.ai/v2/docs`), internal reference links within the Markdown files use website root-relative paths without the `docs/` prefix or `.md` extension (e.g., `[Permissions](/permissions)`, `[CLI settings](/cli/config)`, `[Plugins](/build/plugins/migrate-v1)`).

When navigating between documents:

1. **Remove anchors/fragments**: Strip any trailing `#anchor` (e.g., `/config#experimental` ➔ `/config`).
2. **Directory & Landing Page Mappings**:
   - `/` or `/intro` ➔ `docs/intro.md`
   - `/cli` ➔ `docs/cli.md`
   - `/build` ➔ `docs/build.md`
   - `/console` ➔ `docs/console.md`
3. **Standard Links**: Prepend `docs` and append `.md`:
   - `/<path>` ➔ `docs/<path>.md`
   - Examples:
     - `[Permissions](/permissions)` ➔ `docs/permissions.md`
     - `[CLI settings](/cli/config)` ➔ `docs/cli/config.md`
     - `[OpenCode Go](/console/go)` ➔ `docs/console/go.md`
     - `[Plugin RPC](/build/plugins/rpc)` ➔ `docs/build/plugins/rpc.md`
     - `[Claude Code](/console/harnesses/claude-code)` ➔ `docs/console/harnesses/claude-code.md`
4. **External Links**: Absolute URLs (e.g. `https://models.dev`, `https://modelcontextprotocol.io`) remain external resources.

---

## 📚 Documentation Directory

### 🚀 Getting Started & Migration

- [Introduction & Installation](docs/intro.md) - OpenCode overview, platform binaries (macOS, Windows, Linux), terminal, desktop app, and web UI.
- [Migrate from V1](docs/migrate-v1.md) - Upgrading from OpenCode v1 to v2, breaking changes, config consolidation (`cli.json` vs `opencode.jsonc`), and policy migration.
- [Troubleshooting](docs/troubleshooting.md) - Common issues, debugging OpenCode with self-diagnostics, server logs, and compatibility issue reporting.

### 🧠 Core Concepts & Workflows

- [Instructions (`AGENTS.md`)](docs/instructions.md) - Persistent project guidance, build commands, architecture notes, and coding rules.
- [Agents](docs/agents.md) - Custom sub-agents (e.g., read-only reviewers), roles, tool overrides, and request options.
- [Skills](docs/skills.md) - Reusable task instructions defined in `.opencode/skills/<skill-id>/SKILL.md`.
- [Tools](docs/tools.md) - Built-in tool capabilities (`read`, `write`, `edit`, `patch`, `bash`, `websearch`), tool selection, and execution permissions.
- [Attachments](docs/attachments.md) - Adding local files, images, and context to prompt interactions.
- [References](docs/references.md) - Named external directory and Git repository references outside the project workspace.
- [Snapshots](docs/snapshots.md) - Session checkpointing to undo conversation steps and file modifications together.
- [Compaction](docs/compaction.md) - Automatic and manual context compaction, history summarization, and token budget preservation.
- [Session Warming](docs/warming.md) - Periodic background requests to preserve provider-side prompt caching.

### ⚙️ Configuration & Governance

- [Configuration](docs/config.md) - Server and project settings in `opencode.jsonc`, JSON schema validation, and config precedence.
- [Providers](docs/providers.md) - LLM provider setup (Anthropic, OpenAI, Google, AWS Bedrock, Ollama, OpenCode Go, etc.).
- [Models](docs/models.md) - Model selection (`/models`), default models, context limits, variants, and provider options.
- [Permissions](docs/permissions.md) - Rule-based security controls for tools, command execution, and file paths (`allow`, `ask`, `deny`).
- [Policies](docs/policies.md) - Organization and workspace policies, provider restrictions, and hard denials.
- [Network](docs/network.md) - Proxy environment variables, corporate network configurations, and loopback exclusions.
- [Formatters](docs/formatters.md) - Auto-formatting file edits with tools like Prettier, rustfmt, gofmt, etc.
- [Web Search](docs/websearch.md) - Web search configuration, DuckDuckGo / Brave / Google search providers, and query permissions.
- [MCP Servers](docs/mcp-servers.md) - Model Context Protocol integration, connecting external tools, prompts, resources, and instructions.

### 💻 CLI & Terminal Client (`cli/`)

- [CLI Overview](docs/cli.md) - Terminal CLI overview, starting interactive sessions, and quick start.
- [TUI Guide](docs/cli/tui.md) - Terminal User Interface usage, interactive chatting, and keyboard navigation.
- [CLI Settings](docs/cli/config.md) - Terminal client configuration via global `cli.json` (keybinds, themes, plugins).
- [CLI Commands](docs/cli/commands.md) - Command-line reference (`opencode run`, `opencode server`, flags).
- [Custom Slash Commands](docs/commands.md) - Defining custom prompt slash commands in `.opencode/commands/<name>.md`.
- [Keybinds](docs/cli/keybinds.md) - Keyboard shortcut customization in `cli.json`.
- [Theme Settings](docs/cli/theme.md) - Terminal themes, mode (`light`, `dark`, `system`), and ANSI palette colors.
- [Themes Reference](docs/themes.md) - Built-in themes catalog and styling reference.
- [CLI Providers](docs/cli/providers.md) - Managing and authenticating provider credentials directly in the TUI.
- [CLI Plugins](docs/cli/plugins.md) - Loading UI and terminal plugins within the CLI.
- [Web Interface](docs/cli/web.md) - Web-based UI served from the OpenCode server (`opencode web`, `opencode pair`).
- [Agent Client Protocol (ACP)](docs/cli/acp.md) - Running OpenCode as an ACP agent server (`opencode acp`).

### 🛠️ Build & SDK Development (`build/`)

- [Build Overview](docs/build.md) - Overview of building extensions, apps, and integrations on OpenCode.
- [Plugin System Overview](docs/build/plugins.md) - Architecture and lifecycle for developing OpenCode plugins.
- [Plugin Configuration](docs/plugins.md) - Registering local and published npm plugins in `opencode.jsonc`.
- [CLI Plugins Development](docs/build/plugins/cli.md) - Extending the terminal with custom commands, UI slots, routes, and Markdown renderers.
- [Plugin RPC](docs/build/plugins/rpc.md) - Exposing custom server-side RPC methods and events.
- [Migrate Plugins from V1](docs/build/plugins/migrate-v1.md) - Porting legacy v1 plugins to the v2 plugin architecture.
- [JavaScript Client](docs/build/client.md) - TypeScript / JavaScript client (`@opencode/client`) for the OpenCode HTTP API.
- [Embedded SDK](docs/build/sdk.md) - Hosting OpenCode in-process inside Node.js applications (`@opencode/sdk`).
- [Cloudflare Workers / DO](docs/build/sdk/cloudflare.md) - Running OpenCode inside Cloudflare Durable Objects (`@opencode/sdk/workerd`).
- [Effect-TS Plugin API](docs/build/plugins/effect.md) - Developing typed plugins with Effect (`@opencode/plugin/effect`).
- [Effect-TS Plugin RPC](docs/build/plugins/effect/rpc.md) - Building typed Effect RPC methods and event streams.
- [Effect-TS Client](docs/build/client/effect.md) - Effect-native client for the OpenCode HTTP API (`@opencode/client/effect`).
- [Effect-TS SDK](docs/build/sdk/effect.md) - Effect-native embedded SDK (`@opencode/sdk/effect`).

### ☁️ OpenCode Console & Cloud Services (`console/`)

- [Console Overview](docs/console.md) - OpenCode Console cloud service, team management, and workspace features.
- [Workspaces](docs/console/workspaces.md) - Workspace configuration, shared resources, and team isolation.
- [Members & Roles](docs/console/members.md) - Managing team members, owners, admins, and usage policies.
- [Budgets](docs/console/budgets.md) - Monthly spending caps and budget enforcement policies.
- [Billing](docs/console/billing.md) - Prepaid usage credits and pay-as-you-go model billing without seat fees.
- [Single Sign-On (SSO)](docs/console/sso.md) - Enterprise SAML / OIDC single sign-on integration.
- [Directory Sync (SCIM)](docs/console/scim.md) - Automated user lifecycle provisioning via SCIM 2.0.
- [OpenCode Go](docs/console/go.md) - Curated, reliable coding model subscription plans.
- [Console Models](docs/console/models.md) - Verified model catalog, free models, and benchmarked LLMs.
- [Console Providers](docs/console/providers.md) - Centralized BYOK provider accounts shared across workspace members.
- [Console Web Search](docs/console/websearch.md) - Hosted web search for workspace members without separate API keys.
- [Console API Overview](docs/console/api.md) - Cloud API overview and authentication via API keys.
- [Inference API](docs/console/api/inference.md) - OpenAI, Anthropic, and Gemini-compatible cloud inference endpoint.
- [Providers API Gateway](docs/console/api/providers.md) - Gateway routing requests through workspace connected provider accounts.
- [Harnesses Overview](docs/console/harnesses.md) - Pointing external AI coding agents to the Console gateway.
- [Claude Code Integration](docs/console/harnesses/claude-code.md) - Using Anthropic Claude Code with Console and Go models.
- [Codex Integration](docs/console/harnesses/codex.md) - Using OpenAI Responses API agents with Console.
- [Hermes Agent Integration](docs/console/harnesses/hermes.md) - Connecting Nous Hermes Agent to Console.
- [Pi Integration](docs/console/harnesses/pi.md) - Connecting Pi agent to Console and Go models.
- [Raycast Integration](docs/console/harnesses/raycast.md) - Using Console and Go models in Raycast AI Chat, Quick AI, and AI Commands.
