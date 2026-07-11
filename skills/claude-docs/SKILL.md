---
name: claude-docs
description: Official documentation for the extended Claude ecosystem, including Claude Science, Claude Tag (Slack), Connectors (MCP), Cowork, Government, Office Agents, Plugins, Skills, and Third-Party integrations (Claude Desktop 3P).
metadata:
  author: Ecat
  version: "1.0.0"
---

# Claude Ecosystem Documentation

Welcome to the official documentation for the extended Claude ecosystem, including Claude Science, Claude Tag, Connectors, Cowork, Government, Office Agents, Plugins, Skills, and Third-Party integrations.

## ⚠️ Important Note on References

Because this documentation is a local mirror, internal links found within the text may not map exactly to file paths. When you encounter a reference link (e.g., `/connectors/building/mcp`):
1. **Try adding `docs/` and appending `.md`**: Search for `docs/connectors/building/mcp.md`.

## 📚 Documentation Directory

### 🔬 Claude Science
- [Overview](docs/claude-science/overview.md) | [Get started](docs/claude-science/get-started.md)
- [Core concepts](docs/claude-science/core-concepts.md) | [How Claude Science works with your data](docs/claude-science/how-claude-science-works-with-your-data.md)
- [Tools and environments](docs/claude-science/tools-and-environments.md) | [The reviewer](docs/claude-science/the-reviewer.md)
- [Literature access](docs/claude-science/literature-access.md) | [Annotations](docs/claude-science/annotations.md)
- [Connectors and skills](docs/claude-science/connectors-and-skills.md) | [Custom connectors](docs/claude-science/custom-connectors.md)
- [Cloud storage](docs/claude-science/cloud-storage.md) | [Remote compute clusters](docs/claude-science/remote-compute-clusters.md) | [Compute providers](docs/claude-science/compute-providers.md)
- [Artifacts](docs/claude-science/artifacts.md) | [Run on Windows with WSL](docs/claude-science/run-on-windows-wsl.md)
- [Enable Claude Science](docs/claude-science/enable-claude-science.md) | [Admin controls](docs/claude-science/admin-controls.md) | [Command line settings](docs/claude-science/command-line-settings.md)
- [Manage on devices](docs/claude-science/manage-on-devices.md) | [Monitor usage](docs/claude-science/monitor-usage.md)
- [Legal and compliance](docs/claude-science/legal-and-compliance.md) | [Glossary](docs/claude-science/glossary.md) | [What's not available yet](docs/claude-science/whats-not-available-yet.md) | [Changelog](docs/claude-science/changelog.md)

### 🏷️ Claude Tag (Slack)
- **Concepts:** [Overview](docs/claude-tag/overview.md) | [How it works](docs/claude-tag/concepts/how-it-works.md) | [Agent identity](docs/claude-tag/concepts/agent-identity.md) | [Security and data](docs/claude-tag/concepts/security-and-data.md) | [Glossary](docs/claude-tag/concepts/glossary.md)
- **Users:** [Get started](docs/claude-tag/users/getting-started.md) | [Good habits](docs/claude-tag/users/good-habits.md) | [Memory](docs/claude-tag/users/memory.md) | [Models](docs/claude-tag/users/models.md) | [Proactivity](docs/claude-tag/users/proactivity.md) | [Prompt library](docs/claude-tag/users/prompt-library.md) | [When Claude responds](docs/claude-tag/users/when-claude-responds.md) | [Troubleshooting](docs/claude-tag/users/troubleshooting.md)
- **Use Cases:** [Answer data questions](docs/claude-tag/users/use-cases/answer-data-questions.md) | [Catch up](docs/claude-tag/users/use-cases/catch-up.md) | [Create artifacts](docs/claude-tag/users/use-cases/create-artifacts.md) | [Find answers](docs/claude-tag/users/use-cases/find-answers.md) | [Fix bugs](docs/claude-tag/users/use-cases/fix-bugs.md) | [Marketing team](docs/claude-tag/users/use-cases/marketing-team.md) | [Pull deal state](docs/claude-tag/users/use-cases/pull-deal-state.md) | [Review documents](docs/claude-tag/users/use-cases/review-documents.md) | [Track projects](docs/claude-tag/users/use-cases/track-projects.md) | [Triage requests](docs/claude-tag/users/use-cases/triage-requests.md) | [Watch monitors](docs/claude-tag/users/use-cases/watch-monitors.md) | [Work with GitHub](docs/claude-tag/users/use-cases/work-with-github.md) | [Your own channel](docs/claude-tag/users/use-cases/your-own-channel.md)
- **Admins:** [Add connections](docs/claude-tag/admins/add-connections.md) | [Attach to scope](docs/claude-tag/admins/attach-to-scope.md) | [Audit](docs/claude-tag/admins/audit.md) | [Customize](docs/claude-tag/admins/customize.md) | [For Slack admins](docs/claude-tag/admins/for-slack-admins.md) | [Migrate](docs/claude-tag/admins/migrate-from-earlier.md) | [Network requirements](docs/claude-tag/admins/network-requirements.md) | [Pair workspace](docs/claude-tag/admins/pair-workspace.md) | [Restrict access](docs/claude-tag/admins/restrict-access.md) | [Set spend limit](docs/claude-tag/admins/set-spend-limit.md) | [Skills repo](docs/claude-tag/admins/skills-repo.md) | [Test it](docs/claude-tag/admins/test-it.md) | [Troubleshooting](docs/claude-tag/admins/troubleshooting.md) | [Workspaces](docs/claude-tag/admins/workspaces.md)
- **Connections:** [GitHub](docs/claude-tag/admins/configure-github.md) | [Asana](docs/claude-tag/admins/connections/asana.md) | [Atlassian](docs/claude-tag/admins/connections/atlassian.md) | [BigQuery](docs/claude-tag/admins/connections/bigquery.md) | [Custom](docs/claude-tag/admins/connections/custom.md) | [Datadog](docs/claude-tag/admins/connections/datadog.md) | [GitLab](docs/claude-tag/admins/connections/gitlab.md) | [Gong](docs/claude-tag/admins/connections/gong.md) | [Google](docs/claude-tag/admins/connections/google.md) | [HubSpot](docs/claude-tag/admins/connections/hubspot.md) | [Linear](docs/claude-tag/admins/connections/linear.md) | [Notion](docs/claude-tag/admins/connections/notion.md) | [PagerDuty](docs/claude-tag/admins/connections/pagerduty.md) | [Salesforce](docs/claude-tag/admins/connections/salesforce.md) | [Sentry](docs/claude-tag/admins/connections/sentry.md) | [Snowflake](docs/claude-tag/admins/connections/snowflake.md) | [Stripe](docs/claude-tag/admins/connections/stripe.md) | [Vercel](docs/claude-tag/admins/connections/vercel.md)

### 🔌 Connectors (MCP)
- **Overview:** [Overview](docs/connectors/overview.md) | [Directory](docs/connectors/directory.md) | [Getting started](docs/connectors/getting-started.md)
- **Building:** [Building custom connectors](docs/connectors/building.md) | [MCP](docs/connectors/building/mcp.md) | [MCP Apps](docs/connectors/building/mcp-apps/getting-started.md)
- **Integrations:** [GitHub](docs/connectors/github.md) | [Slack](docs/connectors/slack.md) | [Google Calendar](docs/connectors/google/calendar.md) | [Google Drive](docs/connectors/google/drive.md) | [Gmail](docs/connectors/google/gmail.md) | [Microsoft 365](docs/connectors/microsoft/365.md)

### 🤝 Cowork
- [Overview](docs/cowork/overview.md) | [Dispatch](docs/cowork/guide/dispatch.md) | [Plugins](docs/cowork/guide/plugins.md) | [Projects](docs/cowork/guide/projects.md) | [Monitoring](docs/cowork/monitoring.md) | [Changelog](docs/cowork/changelog.md)

### 🏛️ Government
- [Overview](docs/government/overview.md)
- **Account:** [Overview](docs/government/account/overview.md) | [Profile](docs/government/account/profile.md) | [Sessions](docs/government/account/sessions.md) | [Usage](docs/government/account/usage.md)
- **Org Admin:** [Overview](docs/government/org-admin/overview.md) | [Analytics](docs/government/org-admin/analytics.md) | [Billing](docs/government/org-admin/billing.md) | [Configuration](docs/government/org-admin/configuration.md) | [Provisioning](docs/government/org-admin/provisioning.md) | [Readiness](docs/government/org-admin/readiness.md) | [Seats](docs/government/org-admin/seats.md) | [Users](docs/government/org-admin/users.md)
- **Tenant Admin:** [Overview](docs/government/tenant-admin/overview.md) | [Admins](docs/government/tenant-admin/admins.md) | [Configuration](docs/government/tenant-admin/configuration.md) | [Credits](docs/government/tenant-admin/credits.md) | [Identity and Access](docs/government/tenant-admin/identity-and-access.md) | [Organizations](docs/government/tenant-admin/organizations.md)

### 🏢 Office Agents
- [Overview](docs/office-agents/overview.md)
- **Apps:** [Excel](docs/office-agents/excel.md) | [Outlook](docs/office-agents/outlook.md) | [PowerPoint](docs/office-agents/powerpoint.md) | [Word](docs/office-agents/word.md)
- **Features:** [Connectors and Skills](docs/office-agents/connectors-and-skills.md) | [Dictation](docs/office-agents/dictation.md) | [Enterprise Readiness](docs/office-agents/enterprise-readiness.md) | [FSI Plugins](docs/office-agents/fsi-plugins.md) | [Third-party Platforms](docs/office-agents/third-party-platforms.md) | [Work Across Apps](docs/office-agents/work-across-apps.md)

### 🧩 Plugins & Skills
- **Plugins:** [Overview](docs/plugins/overview.md) | [Submit](docs/plugins/submit.md)
- **Skills:** [Overview](docs/skills/overview.md) | [How-to](docs/skills/how-to.md)

### 🖥️ Third-Party Desktop
- [Overview](docs/third-party/claude-desktop/overview.md) | [Installation](docs/third-party/claude-desktop/installation.md) | [Feature Matrix](docs/third-party/claude-desktop/feature-matrix.md)
- **Configuration:** [Configuration](docs/third-party/claude-desktop/configuration.md) | [In-app config](docs/third-party/claude-desktop/in-app-configuration.md) | [Code](docs/third-party/claude-desktop/code.md) | [Extensions](docs/third-party/claude-desktop/extensions.md) | [Web Tools](docs/third-party/claude-desktop/web-tools.md)
- **Deployments:** [Bedrock](docs/third-party/claude-desktop/bedrock.md) | [Mantle](docs/third-party/claude-desktop/mantle.md) | [Foundry](docs/third-party/claude-desktop/foundry.md) | [Vertex](docs/third-party/claude-desktop/vertex.md) | [Gateway](docs/third-party/claude-desktop/gateway.md) | [Claude API](docs/third-party/claude-desktop/claude-api.md)
