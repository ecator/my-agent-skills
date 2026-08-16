---
name: pi-docs
description: Local knowledge base mirroring the official Pi Coding Agent documentation.
metadata:
  author: Ecat
  version: "0.84.2"
  source: https://github.com/earendil-works/pi/tree/main/packages/coding-agent
---

# Pi Docs Skill

This skill serves as a comprehensive local knowledge base mirroring the official Pi Coding Agent documentation. It provides immediate, offline access to references, guides, and practical code snippets for using, extending, and integrating the Pi Coding Agent.

## Overview of Contents

The knowledge base is divided into two main areas: `docs/` for written documentation and `examples/` for reference code implementations.

### 📚 `docs/` (Documentation)

The `docs/` directory contains detailed Markdown guides covering all aspects of Pi. Important sub-topics include:

- **Getting Started & Setup:** `quickstart.md`, `usage.md`, `terminal-setup.md`, `windows.md`, `termux.md`.
- **Core Concepts:** Learn about `sessions.md`, context `compaction.md`, `settings.md`, `keybindings.md`, and `environment-variables.md`.
- **Extensibility & Customization:** Build and apply `extensions.md`, `skills.md`, `themes.md`, `prompt-templates.md`, and custom `tui.md` components.
- **Models & Providers:** Configure built-in `providers.md`, add `models.md` entries, run local models with `llama-cpp.md`, or create a `custom-provider.md`.
- **Programmatic Integration:** Understand how to leverage the `sdk.md`, `rpc.md` mode, `session-format.md`, and `json.md` event streams.
- **Security & Sandboxing:** Read up on `security.md` boundaries and `containerization.md` (e.g., Gondolin, Docker).

### 💡 `examples/` (Code Examples)

The `examples/` directory is packed with practical implementations demonstrating Pi's API and extensibility:

- **`sdk/`:** Contains a sequence of numbered TypeScript files (e.g., `01-minimal.ts` through `13-session-runtime.ts`) demonstrating how to embed Pi inside Node.js applications programmatically using `createAgentSession()`. It covers topics like injecting custom tools, settings, skills, and prompts.
- **`extensions/`:** A large collection of over 70 custom extension examples. Here you will find reference implementations for:
  - **Custom UIs:** Model status widgets, custom headers/footers, rainbow editors, and working indicators.
  - **Custom Tools:** Inline bash execution, interactive shell management, bookmarks, and structured outputs.
  - **Lifecycle Events & Safety:** Permission gates, confirmation dialogs (destructive actions), bash spawn hooks, and dirty repo guards.
  - **Integrations:** Git checkpoints, SSH tunneling, file watchers, system theme syncing.
  - **Games & Miniapps:** Interactive applications like `snake.ts`, `tic-tac-toe.ts`, and `space-invaders.ts` running natively inside Pi's terminal UI.

## Usage

When working on tasks related to the Pi Coding Agent—such as writing a new extension, configuring a local router, or embedding the Pi SDK in another application—explore the `docs/` and `examples/` directories to retrieve correct API usage and implementation patterns.
