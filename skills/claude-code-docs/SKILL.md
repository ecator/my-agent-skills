---
name: claude-code-docs
description: Official documentation for Claude Code, Anthropic's agentic coding tool available in the terminal, IDE, desktop app, and browser. Covers installation, configuration, skills, subagents, hooks, MCP, the Agent SDK, and reference material.
metadata:
  author: Ecat
  version: "2.1.207"
---

# Claude Code Documentation

Welcome to the official documentation for Claude Code, Anthropic's agentic coding tool available in the terminal, IDE, desktop app, and browser.

## ⚠️ Important Note on References

Because this documentation is a local mirror, internal links found within the text may not map exactly to file paths. When you encounter a reference link (e.g., `/en/claude-code-on-the-web`):
1. **Try adding `docs/` and appending `.md`**: Search for `docs/en/claude-code-on-the-web.md`.

## 📚 Documentation Directory

### 🚀 Getting Started
- [Quickstart](docs/en/quickstart.md) - Welcome to Claude Code!
- [Overview](docs/en/overview.md) - What is Claude Code?
- [Features Overview](docs/en/features-overview.md) - Understand when to use different features.
- [Setup](docs/en/setup.md) - Advanced setup, requirements, and version management.
- [How Claude Code works](docs/en/how-claude-code-works.md) - The agentic loop and built-in tools.

### 💻 Platforms & Integrations
- [Platforms Overview](docs/en/platforms.md) - Choose where to run Claude Code.
- [Desktop App](docs/en/desktop.md) | [Desktop Quickstart](docs/en/desktop-quickstart.md)
- [VS Code Extension](docs/en/vs-code.md)
- [JetBrains IDEs](docs/en/jetbrains.md)
- [Claude Code on the Web](docs/en/claude-code-on-the-web.md) | [Web Quickstart](docs/en/web-quickstart.md)
- [Chrome (Beta)](docs/en/chrome.md)
- [Slack](docs/en/slack.md)

### ⚙️ Usage & Core Workflows
- [Commands](docs/en/commands.md) - Reference for commands and bundled skills.
- [Interactive Mode](docs/en/interactive-mode.md) - Keyboard shortcuts and input modes.
- [Common Workflows](docs/en/common-workflows.md) - Guides for exploring, bug fixing, and refactoring.
- [Best Practices](docs/en/best-practices.md) - Tips for getting the most out of Claude Code.
- [Computer Use](docs/en/computer-use.md) - Enable Claude to use your computer from the CLI.
- [Context Window](docs/en/context-window.md) & [Memory](docs/en/memory.md) - How Claude remembers your project.
- [Checkpointing](docs/en/checkpointing.md) - Rewind and summarize edits.

### 🛠️ Configuration & Customization
- [Settings](docs/en/settings.md) & [Environment Variables](docs/en/env-vars.md)
- [CLI Reference](docs/en/cli-reference.md)
- [Model Configuration](docs/en/model-config.md)
- [Terminal Config](docs/en/terminal-config.md) | [Keybindings](docs/en/keybindings.md) | [Statusline](docs/en/statusline.md)
- [Explore the .claude directory](docs/en/claude-directory.md)
- [Output Styles](docs/en/output-styles.md) | [Voice Dictation](docs/en/voice-dictation.md) | [Fast Mode](docs/en/fast-mode.md)

### 🧩 Extending Claude Code
- **Skills:** [Extend Claude with Skills](docs/en/skills.md)
- **MCP:** [Connect to Tools via MCP](docs/en/mcp.md)
- **Hooks:** [Hooks Guide](docs/en/hooks-guide.md) | [Hooks Reference](docs/en/hooks.md)
- **Plugins:** [Create Plugins](docs/en/plugins.md) | [Plugins Reference](docs/en/plugins-reference.md) | [Marketplaces](docs/en/plugin-marketplaces.md)
- **Subagents:** [Create Custom Subagents](docs/en/sub-agents.md)
- **Channels:** [Push Events](docs/en/channels.md) | [Channels Reference](docs/en/channels-reference.md)

### 🤖 Agent SDK
- [Agent SDK Overview](docs/en/agent-sdk/overview.md) | [Quickstart](docs/en/agent-sdk/quickstart.md)
- **References:** [TypeScript Reference](docs/en/agent-sdk/typescript.md) | [Python Reference](docs/en/agent-sdk/python.md)
- **Features:** [Agent Loop](docs/en/agent-sdk/agent-loop.md) | [Custom Tools](docs/en/agent-sdk/custom-tools.md) | [Streaming Output](docs/en/agent-sdk/streaming-output.md)
- *See the `docs/en/agent-sdk/` directory for the complete SDK documentation.*

### ⚡ Advanced Workflows & Orchestration
- [Parallel Sessions with Worktrees](docs/en/worktrees.md)
- [Agent Teams](docs/en/agent-teams.md) | [Manage Multiple Agents (Agent View)](docs/en/agent-view.md) | [Run Agents in Parallel](docs/en/agents.md)
- [Code Review](docs/en/code-review.md) | [Ultrareview (Research Preview)](docs/en/ultrareview.md)
- [Plan in the Cloud with Ultraplan](docs/en/ultraplan.md)
- [Automate Work with Routines](docs/en/routines.md) | [Scheduled Tasks](docs/en/scheduled-tasks.md)
- [CI/CD Integrations:](docs/en/third-party-integrations.md) [GitHub Actions](docs/en/github-actions.md) | [GitLab CI/CD](docs/en/gitlab-ci-cd.md)

### 🏢 Enterprise & Administration
- [Admin Setup](docs/en/admin-setup.md) | [Server-Managed Settings](docs/en/server-managed-settings.md)
- [Permissions](docs/en/permissions.md) | [Permission Modes](docs/en/permission-modes.md) | [Auto Mode Config](docs/en/auto-mode-config.md)
- [Security](docs/en/security.md) | [Authentication](docs/en/authentication.md) | [Network Config](docs/en/network-config.md)
- [Manage Costs](docs/en/costs.md) | [Track Usage with Analytics](docs/en/analytics.md) | [Monitoring (OpenTelemetry)](docs/en/monitoring-usage.md)
- **Providers:** [AWS](docs/en/claude-platform-on-aws.md) | [Bedrock](docs/en/amazon-bedrock.md) | [Vertex AI](docs/en/google-vertex-ai.md) | [Foundry](docs/en/microsoft-foundry.md)
- [Data Usage Policies](docs/en/data-usage.md) | [Zero Data Retention](docs/en/zero-data-retention.md) | [Legal & Compliance](docs/en/legal-and-compliance.md)

### 🐛 Troubleshooting & Reference
- [Troubleshooting](docs/en/troubleshooting.md) | [Troubleshoot Installation](docs/en/troubleshoot-install.md) | [Debug your Configuration](docs/en/debug-your-config.md)
- [Error Reference](docs/en/errors.md)
- [Tools Reference](docs/en/tools-reference.md)
- [Glossary](docs/en/glossary.md)


### 🆕 Newly Added Documentation
- [Escalate hard decisions with the advisor tool](docs/en/advisor.md)
- [Share session output as artifacts](docs/en/artifacts.md)
- [Claude apps gateway configuration](docs/en/claude-apps-gateway-config.md)
- [Claude apps gateway deployment and operations](docs/en/claude-apps-gateway-deploy.md)
- [Deploy Claude apps gateway on Google Cloud](docs/en/claude-apps-gateway-on-gcp.md)
- [Claude apps gateway spend limits](docs/en/claude-apps-gateway-spend-limits.md)
- [Launch sessions from links](docs/en/deep-links.md)
- [Claude Desktop on Linux (beta)](docs/en/desktop-linux.md)
- [Schedule recurring tasks in Claude Code Desktop](docs/en/desktop-scheduled-tasks.md)
- [Development containers](docs/en/devcontainer.md)
- [Discover and install prebuilt plugins through marketplaces](docs/en/discover-plugins.md)
- [Feature availability](docs/en/feature-availability.md)
- [Fullscreen rendering](docs/en/fullscreen.md)
- [Run Claude Code through a gateway](docs/en/gateways.md)
- [Claude Code with GitHub Enterprise Server](docs/en/github-enterprise-server.md)
- [Keep Claude working toward a goal](docs/en/goal.md)
- [Run Claude Code programmatically](docs/en/headless.md)
- [Set up Claude Code in a monorepo or large codebase](docs/en/large-codebases.md)
- [Connect Claude Code to an LLM gateway](docs/en/llm-gateway-connect.md)
- [Gateway protocol reference](docs/en/llm-gateway-protocol.md)
- [Roll out an LLM gateway for your organization](docs/en/llm-gateway-rollout.md)
- [Control MCP server access for your organization](docs/en/managed-mcp.md)
- [Connect to MCP servers](docs/en/mcp-quickstart.md)
- [Constrain plugin dependency versions](docs/en/plugin-dependencies.md)
- [Recommend your plugin from your CLI](docs/en/plugin-hints.md)
- [Recommend plugins for your org](docs/en/plugin-relevance.md)
- [How Claude Code uses prompt caching](docs/en/prompt-caching.md)
- [Prompt library](docs/en/prompt-library.md)
- [Continue local sessions from any device with Remote Control](docs/en/remote-control.md)
- [Choose a sandbox environment](docs/en/sandbox-environments.md)
- [Configure the sandboxed Bash tool](docs/en/sandboxing.md)
- [Catch security issues as Claude writes code](docs/en/security-guidance.md)
- [Manage sessions](docs/en/sessions.md)
- [Orchestrate subagents at scale with dynamic workflows](docs/en/workflows.md)

### 📢 Updates & Community
- [Changelog](docs/en/changelog.md)
- [What's New](docs/en/whats-new.md)
- [Champion Kit](docs/en/champion-kit.md) | [Communications Kit](docs/en/communications-kit.md)
