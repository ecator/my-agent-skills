---
name: claude-api-docs
description: Comprehensive Anthropic Claude API Documentation and Developer Guides
metadata:
  author: Ecat
  version: "1.1.0"
---

# Claude API Documentation

This skill provides comprehensive documentation and guides for integrating Anthropic's Claude models into your applications. Claude is a highly performant, trustworthy, and intelligent AI platform that excels at tasks involving language, reasoning, analysis, coding, and more.

## ⚠️ Important Note on References

Because this documentation is a local mirror, internal links found within the text may not map exactly to file paths. When you encounter a reference link (e.g., `/docs/en/cli-sdks-libraries`):

1. **Try appending `.md`**: Search for `docs/en/cli-sdks-libraries.md`.
2. **Check for an overview**: If the file doesn't exist, the path is likely a directory. Try looking for an `overview.md` inside it (e.g., `docs/en/cli-sdks-libraries/overview.md`).

## Entry Points & Documentation Index

- **[Introduction to Claude](docs/en/intro.md)**: An overview of Claude, available models, and the recommended path for new developers.
- **[Get Started with Claude](docs/en/get-started.md)**: Quickstart guides for making your first API call using cURL, the ant CLI, or official SDKs (Python, TypeScript, C#, Go, Java, PHP, Ruby).

### Directory Index

- **[about-claude](docs/en/about-claude)**: Information about Claude models, security, and general concepts.
- **[agents-and-tools](docs/en/agents-and-tools)**: Guides on building agents and using tools (e.g., MCP connector).
- **[api](docs/en/api)**: Comprehensive API reference, including messages, administration, compliance, and beta features.
- **[build-with-claude](docs/en/build-with-claude)**: Core guides on building applications with Claude (e.g., prompt engineering, context management, vision, embeddings, and adaptive thinking).
- **[cli-sdks-libraries](docs/en/cli-sdks-libraries)**: Documentation for the ant CLI, client SDKs, libraries, and middleware.
- **[manage-claude](docs/en/manage-claude)**: Documentation on managing workspaces, API access, compliance, and Workload Identity Federation.
- **[managed-agents](docs/en/managed-agents)**: Documentation for Claude Managed Agents, including setup, memory, skills, and tools.
- **[release-notes](docs/en/release-notes)**: Updates and release notes for the Claude API and system prompts.
- **[resources](docs/en/resources)**: Additional resources, glossaries, and references.
- **[test-and-evaluate](docs/en/test-and-evaluate)**: Guides on evaluating model performance, developing tests, and strengthening guardrails.

## Overview

Anthropic offers several primary ways to build with Claude:

- **Messages API**: Direct model prompting access. Best for custom agent loops and fine-grained control.
- **Claude Agent SDK**: Build agents that run in a process you operate.
- **Claude Managed Agents**: Pre-built, configurable agent harness running in managed infrastructure. Best for long-running tasks and asynchronous work.

### Latest Generation of Claude Models

- **Claude 5 Family** - Including the newly introduced **Claude Sonnet 5**, **Claude Fable 5**, and **Claude Mythos 5**.
- **Claude Opus 4.8** - The latest iteration of our most capable model for complex reasoning.
- _(Note: Previous frontier models include Claude Opus 4.7, Sonnet 4.6, and Haiku 4.5)._

## Key Capabilities

- **Text and code generation**: Summarize text, answer questions, extract data, translate text, and explain and generate code.
- **Vision & Document Analysis**: Process and analyze visual input, generate text and code from images, and extract content from PDF files.
- **Extended and Adaptive Thinking**: Allow models to dynamically determine when and how much to think for complex reasoning tasks (e.g., Claude Opus 4.8 and Claude 5 series).
- **Tool Use (Function Calling) & MCP**: Connect Claude to external APIs, built-in server-side tools (Web Search, Web Fetch, Code Execution), and remote MCP servers.
- **Computer Use & Client-side Tools**: Enable Claude to control computer interfaces, edit files, and utilize memory for cross-conversation context.
- **Agent Skills**: Extend capabilities with pre-built Skills (e.g., PowerPoint, Excel) or custom instructions.
- **Context Management**: Utilize prompt caching, automatic compaction, and token counting to optimize costs and latency for large-scale operations.
- **Files API**: Upload and manage files (PDFs, images, text) for reuse across requests.
- **Batch Processing**: Send asynchronous batches of requests for reduced costs when processing large volumes of data.

## Getting Started

To make your first API call, you will need an Anthropic Console account and an API key.

You can find quickstart instructions for various languages and tools in the [Get Started](docs/en/get-started.md) guide. For example, to use the Python SDK:

1. Set your API key: `export ANTHROPIC_API_KEY='your-api-key-here'`
2. Install the SDK: `pip install anthropic`
3. Create a client and make a request using `client.messages.create()`.

## Developer Resources

- **Developer Console**: Prototype and test prompts in your browser.
- **API Reference**: Explore the full Claude API and client SDK documentation.
- **Claude Cookbook**: Learn with interactive Jupyter notebooks.

Follow the links in the entry points to dive deeper into working with the Messages API, comparing models, and exploring advanced features like tool use and structured outputs.
