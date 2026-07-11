
# Config

> Set tenant-wide defaults for product behavior, lock settings so organizations can't override them, and preview how a change affects each organization.

> **Who this is for:** Tenant administrators who set and enforce product settings across every organization in their deployment.

Use this page to set tenant-wide defaults for product behavior, lock settings so organizations can't override them, and preview how a change would affect each organization.

## How settings are applied

Each setting is resolved through a chain: **Application default → Your tenant → Each organization**. A value you set here becomes the default for every organization, and an organization can still change the setting on its own Config page unless you lock it. When you expand a setting you can see each step of this chain, which value is **In effect**, and (in the tenant view) which organizations have set their own value.

A **lock** prevents levels below from changing the setting. When you lock a setting here it shows as **Enforced**, and organizations see it as **Managed**, which means it is read-only for them. Any value an organization had previously set is ignored while your lock is in place, and it comes back into effect if you later remove the lock.

> **For organization owners:** When a setting shows as **Managed** on your organization's Config page, it has been locked at the tenant level and you can't change it. Any value you had previously set is ignored while the lock is in place.

### Setting kinds

Settings combine across the chain in one of three ways, and the kind is fixed per setting (you don't choose it):

* A **simple value** is replaced at each level, and the most specific level that set it wins. Most settings work this way.
* A **restriction** is a limit where the tightest value across all levels wins. Any level can tighten the limit but none can loosen it. For example, if you set a session timeout of 30 minutes, an organization can set 15 but cannot set 60.
* A **collection** accumulates entries from each level. A level can add entries to what the level above provided, or replace the list entirely.

## Working with the list

Settings are grouped by category in the sidebar on the left. Select a category to see its settings; the number beside each category shows how many settings it contains.

Each setting appears as an expandable card showing its name, a one-line description, which products it applies to, its current value, and where that value comes from (for example, **From Anthropic default** or **Set at tenant**). Click a card to expand the full chain and the editor.

The scope bar above the list shows which level you are editing and lets you switch between levels when you have access to more than one. Use **Compare config across levels** to see every setting side by side across the Anthropic default, your tenant, and each organization.

To change a setting, expand it, adjust the value, and save. To stop overriding a setting at your level and return to whatever the level above provides, reset it.

## Previewing impact

After you change a setting, a **Preview impact** button appears next to **Save changes**. Select it to see a table listing every organization with its current effective value and what it would become after your change. Organizations where nothing would change are marked **unchanged**. This is especially useful when locking a setting, so you can see which organizations currently have a different value that your lock will override.

Preview isn't available for settings whose values are hidden for security reasons (for example, settings that can contain authorization tokens). For those settings the preview shows whether a value is set rather than what it is.

## Available settings

| Setting                                       | What it does                                                                                                                                                                                                                                                                                                                                                                                                        |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Session idle timeout (minutes)**            | This controls how long a user may be inactive before being signed out. The default is 1440 minutes (24 hours), and the value must be a whole number of minutes, 15 or higher. Lowering the timeout applies to new sign-ins only, while raising it takes effect on existing sessions the next time they are used. This is a restriction, so organizations can shorten it but not lengthen it past what you set here. |
| **Organizations manage their own seat tiers** | This controls whether organization owners may create and edit their own custom seat tiers in addition to the tenant-managed ones. Only tenant administrators can change this setting; organization owners cannot grant themselves the capability.                                                                                                                                                                   |
| **Compliance API keys enabled**               | This controls whether organization owners may create new credentials for the Compliance API. Listing and revoking existing keys remains available even when this is off, so that a disabled organization can still rotate an exposed key.                                                                                                                                                                           |
| **Telemetry endpoint (OTLP)**                 | This is the address where Claude products send usage telemetry using the OpenTelemetry protocol. Leave it empty to disable telemetry.                                                                                                                                                                                                                                                                               |
| **Telemetry headers**                         | These are additional headers (such as an authorization token) sent with every telemetry request. Values here are hidden in the preview for security.                                                                                                                                                                                                                                                                |
| **Managed MCP servers**                       | These are pre-configured Model Context Protocol servers made available to your users. An MCP server is an integration that extends Claude with external tools and data sources. This is a collection, so organizations can add to the list you provide here. Server addresses must use HTTPS.                                                                                                                       |
| **Desktop banner**                            | This is a persistent banner shown at the top of Claude Desktop. You can set the text, colors, and an optional link, and preview the result live.                                                                                                                                                                                                                                                                    |
| **Product availability**                      | A group of separate switches (**Claude Desktop enabled**, **Claude Code enabled**, **Claude for M365 enabled**, **Chat tab**, **Cowork tab**, **Code tab**, **Chat code execution**) that control which Claude products and tabs are available to users. All are on by default.                                                                                                                                     |

> Your deployment may include additional settings not listed above. Any extra setting still follows the same chain, status badges, and edit/reset behavior.

## Comparing settings across levels

Select **Compare config across levels** at the top of the Config page to open a read-only table that lays every setting out side by side across the full chain. This view is for understanding how a value got to be what it is, and for spotting which levels have overridden which settings. You can't change anything from here; each row has an **Edit** link that takes you back to that setting on the main Config page.

The table has one row per setting and one column per level in the chain: the **Anthropic default**, your **Tenant**, **Groups** (tenant-wide group settings), each **Organization**, **Org groups** (group settings scoped to one organization), and the **Final value** that actually takes effect. A dash means that level has not set a value for that setting. A lock icon next to a value means that level has locked it. Use the **All levels** / **Final only** toggle to hide the middle columns and show just the setting, where it was set, and the final value.

Before you pick a person, the **Groups** and **Organization** columns list every group and organization that has set its own value for that setting, so you can see at a glance where overrides exist across your tenant.

### Looking up one person's settings

Type a name into the search box above the table to see exactly what settings apply to that person. The table re-resolves every setting from that person's point of view: the **Groups** column shows the value from the one group that applies to them (with any lower-priority groups they belong to shown faded, since those do not count), the **Organization** column shows their organization's value, and the **Final value** column shows what they actually get. A summary card above the table lists the tenant, group, and organization being used for the lookup.

Click any row to expand a plain-English explanation of how the final value was reached, for example "Anthropic's default is On. Your tenant hasn't changed it. The Program-Reviewers group sets this to Off." This is the quickest way to answer a question like "why is this turned off for this person?"

## Group-specific settings

In addition to setting values for your whole tenant, you can set values for the members of a directory group. A directory group is a group that your identity provider has pushed to Claude for Government over SCIM, as described on the [Identity and access](/government/tenant-admin/identity-and-access) page. Group-level settings sit between the tenant and the organization in the chain, so a value you set for a group overrides your tenant default for that group's members, in every organization they belong to.

To edit settings for a group, open the scope bar above the settings list and choose the group's name from the dropdown. The page switches to show the same settings editor, now scoped to that group, and the scope bar reads "Applies to members of \[group], across all orgs." Editing, saving, resetting, and locking all work the same way as at the tenant level. A lock you set at the tenant level still applies here and shows the setting as **Managed** for the group.

### When someone belongs to more than one group

Only one group's settings apply to any given person. When someone is a member of more than one group, the settings from their highest-priority group that has any configuration are used, and the other groups are ignored for that person. You set the priority order on the [Identity and access](/government/tenant-admin/identity-and-access) page by dragging the groups into the order you want. The same priority order is used wherever configuration is resolved for a person; seat-tier group mappings on the [Provisioning](/government/org-admin/provisioning) page use a separate fixed order.

If no groups appear in the scope bar dropdown, none have been synced from your identity provider yet. Connect SCIM on the Identity and access page and push groups from your directory, and they will appear automatically.

## Things to know

* Changes saved here take effect across all organizations immediately, without requiring users to sign out. Client applications pick up the new values the next time they refresh their configuration, which is typically within moments. Lowering the session idle timeout is the one case that applies to new sign-ins only, as described above.
* Some settings can only be changed by tenant administrators (and not by organization owners at all), regardless of whether they are locked. These are noted in the descriptions above.
* Resetting a setting removes only the tenant's value. Organization values are unaffected and remain in effect once your value is gone.

