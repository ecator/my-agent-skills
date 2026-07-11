
# Claude Science changelog

> Release notes for Claude Science, including new features, improvements, and bug fixes by version.

<Update label="0.1.18" description="July 9, 2026">
  **Features**

  * Sessions now pause and ask for your confirmation before spending extra usage. Billed usage credits are never drawn on a dismissible warning alone.
  * Claude can now monitor how much memory and processing power its computations are using, and plan its work accordingly.
  * Search from inside a project: the project view now has a search button that opens the same search as Cmd+K.
  * Download any artifact from any surface: every artifact menu now includes a download option.
  * Starred artifacts now pin to a new Starred section at the top of the Library, with a star badge.

  **Fixes**

  * Fixed a crash that could prevent very large sessions from loading.
  * Fixed several ways a running session could stall or stop early, including long thinking pauses being cut off mid-run and sessions resuming incorrectly after a crash.
  * Fixed the app sometimes becoming unresponsive after an automatic update.
  * Code blocks now switch correctly when your system switches between light and dark mode.
  * Lots of other miscellaneous improvements and fixes.
</Update>

<Update label="0.1.17" description="July 8, 2026">
  * **Fixed a bug where idle sessions were consuming usage.**
  * Lots of other miscellaneous improvements and fixes.
</Update>

<Update label="0.1.16" description="July 7, 2026">
  **Features**

  * Auto-review is now available on the Pro plan: turn it on from the session settings, and it stays off until you do.
  * Artifact previews: zoom HTML artifacts (including fit to width), zoom images to native resolution, and choose which version an artifact diff compares against
  * Import skills from private GitHub repositories using your own GitHub credentials
  * LaTeX previews now resolve cross-references — \ref, \eqref, and section numbering render the way your document intended
  * Dashboard upgrades: a project switcher with live per-project status, project names on the "Now" cards, a visible search button, and ⌘K search now matches project descriptions too
  * Annotate artifacts faster: drag image annotation pins to reposition them, and use @/# mentions in annotation comments

  **Fixes**

  * Pasted attachments no longer disappear before their first use, very large text and JSON previews no longer freeze the tab, and a stale usage-limit banner now clears itself once your usage limit resets
  * Cloning a repo or unpacking an archive no longer floods the chat with every image it contains
  * The Reviewer no longer gets stuck on "Reviewing…" or hides its findings tray
  * Flaky read-only connector tool calls now retry once automatically instead of failing your turn, and connector setup errors tell you what's actually wrong
  * A corrupt pasted image no longer breaks the transcript
  * Upgrading with a very large history database no longer fails partway through
  * Fixed a crash when the browser's auto-translate feature modified the page
  * Lots of other miscellaneous improvements and fixes
</Update>

<Update label="0.1.15" description="July 1, 2026">
  * Corporate networks: environment builds now work behind TLS-inspecting proxies (such as Zscaler or Netskope). On macOS, corporate root CAs in your keychain are picked up automatically for conda/pip package downloads; on macOS or Linux you can also point at a CA-bundle file under Settings > Network > Package mirror. The mirror card's Check button now verifies TLS trust with the same bundle the builds use. (In-session `pip`/`curl` and the Desktop app's guest-VM builds are not covered)
  * Package mirrors: point conda and pip at your organization's internal mirror (Artifactory/Nexus) via Settings > Network > Package mirror. Setting a mirror also drops the public package hosts from the sandbox network allowlist
  * OpenAlex now requires a free API key for full-text access. Claude Science resolves access automatically or asks you in the session when a key is needed; you can also add and validate a key anytime under Customize > Credentials
  * New Context usage view: see how full a session's context window is and where tokens go, from the + menu in the composer
  * Lots of other miscellaneous improvements and fixes
</Update>

<Update label="0.1.14" description="June 30, 2026">
  * Public launch of Claude Science
</Update>

