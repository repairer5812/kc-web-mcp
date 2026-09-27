# Privacy and data flow

This project is software you install on your own PC or server. The repository
maintainer does not operate a shared development service and receives no
telemetry, project files, authentication tokens, or tool requests from it.

When you connect the server to ChatGPT, tool arguments travel from ChatGPT to
your server. Requested file contents, command output, Git information, and
errors travel back to ChatGPT. OpenAI's policies for your account apply to
that data. Connect only projects you are authorized to process this way.

The supplied HTTPS transport uses Cloudflare Tunnel. Traffic passes through
Cloudflare infrastructure under Cloudflare's applicable terms and privacy
policy. TLS termination at Cloudflare means this is not end-to-end encryption
that excludes the tunnel operator from processing HTTP traffic.

Local Docker volumes persist project files, workspace state, OAuth client
registrations, and authentication state. Docker keeps bounded service logs.
There is no separate analytics collection. Operators are responsible for
retention, backups, access control, and deletion of their own volumes.

Each operator and user should use their own ChatGPT account and runtime.
Do not share owner tokens or ChatGPT session credentials. This release is
for a single trusted operator, not a multi-tenant hosting service.

Stop access with `docker compose stop`. Remove the ChatGPT connection to
disconnect the client. Delete local volumes only after backing up needed
work; deleting them permanently removes projects and authentication state.
