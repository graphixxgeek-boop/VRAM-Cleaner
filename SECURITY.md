# Security policy

## Supported versions

The latest release receives fixes.

## Reporting a vulnerability

Please do not open a public issue for a security problem.

Use GitHub's private reporting: **Security tab → Report a vulnerability** on this repository. Include the affected version, steps to reproduce, and the impact you observed.

You can expect an acknowledgement within a few days.

## Scope notes

VRAM Zero makes no network connections and stores no data. It runs `nvidia-smi` and `taskkill` as the current user. Reports about antivirus false positives are not vulnerabilities: please open a regular issue and include the detection name.
