# Security

Use this server only for trusted development projects. OAuth approval
authorizes access to tools that can modify files and run shell commands.

- Do not mount the host home directory, SSH keys, credential files, or Docker socket.
- Keep the runtime unprivileged; retain capability removal and no-new-privileges.
- The file-tool allowlist does not sandbox arbitrary shell commands. The supplied
  container is the host boundary, and all projects in that container share it.
- Shell commands can access the runtime's own state and network. Treat an approved
  client as having control over this single-operator development instance.
- Never install a second person's project in the same instance as private work.
- Quick Tunnel URLs are temporary. Use a named tunnel for stable operation.
- Do not advertise this project as bypassing usage limits or reselling model access.

Report vulnerabilities through the repository's private vulnerability reporting
feature when available. Do not post credentials or a working exploit against
someone else's server in a public issue.
