# Cross-platform learning standard: Linux + Windows

**Mandatory Academy rule:** learners must be able to complete every applicable workflow on both Linux and Windows. Instructions must be operational, not merely a list of equivalent products.

## 1. Required structure in every practical chapter

For each tool, command-line workflow, programming task, database task, dashboard, or deployment exercise, include:

1. **Shared concepts and outcome** — what the learner is building and how success is checked.
2. **Linux route** — installation or setup, exact commands, shell-specific notes where needed, execution, expected outputs, and common fixes.
3. **Windows route** — installation or setup, exact PowerShell commands (and GUI route where appropriate), execution, expected outputs, and common fixes.
4. **Portable project structure** — relative paths, environment variables, configuration files, dependency manifests, and Git practices that work across systems.
5. **OS-specific differences** — filesystem paths, permissions, services, package managers, line endings, shells, drivers, networking, containers, and application availability.
6. **Verification checklist** — the same measurable result must be obtained on both systems.
7. **Troubleshooting** — likely errors on each OS and safe recovery steps.
8. **Professional handoff** — how to document setup so a teammate can reproduce it on either OS.

Do not present Linux commands as if they run unchanged in Windows CMD or PowerShell, or Windows commands as if they run unchanged in Bash/Fish. Label every command by shell.

## 2. Standard environments

| Task | Linux route | Windows route | Cross-platform rule |
|---|---|---|---|
| Terminal | Bash or Zsh; Fish notes when relevant | PowerShell 7 preferred; CMD only when necessary | Label shell explicitly; explain syntax differences |
| Python | python3, venv, pip; distro package manager for system tools | Python.org or approved distribution, `py`, `venv`, pip | Use project virtual environments and `requirements.txt`/`pyproject.toml` |
| SQL | PostgreSQL/SQLite clients, DBeaver | PostgreSQL/SQLite clients, DBeaver | SQL examples must be database-specific where syntax differs |
| R | R + RStudio/Posit, Rscript | R + RStudio/Posit, Rscript | Use project-relative paths and `renv` where appropriate |
| Git | Native Git + terminal/GUI | Git for Windows + PowerShell/GUI | Include `.gitignore`, line-ending guidance, no secrets in commits |
| VS Code | Native Linux package/official distribution | Windows installer/official distribution | Use workspace settings and documented extensions |
| Jupyter | venv/conda environment + JupyterLab | venv/conda environment + JupyterLab | Select the correct kernel; pin dependencies |
| Containers | Docker Engine or compatible runtime | Docker Desktop with WSL 2 backend, subject to licensing and system requirements | Explain daemon/service differences, mounts, ports, and permissions |
| BI | Power BI Service/browser where available; Metabase/Superset/Tableau alternatives | Power BI Desktop and other supported BI tools | Clearly mark features that are Windows-only; do not imply Power BI Desktop runs natively on Linux |
| Cloud/API | CLI + browser + environment variables | CLI + PowerShell + browser + environment variables | Same API concepts; separate install/authentication commands |
| Office files | LibreOffice/OnlyOffice and portable formats | Microsoft Office/OnlyOffice/LibreOffice | Explain compatibility limits for complex Excel/PowerPoint features |

The Academy should not require a paid Windows license, paid cloud subscription, or powerful hardware for foundational learning. Where a tool is platform-restricted or paid, provide a realistic alternative and clearly describe what is not equivalent.

## 3. Shell and path conventions

- Linux examples must identify Bash/Zsh or Fish. Fish activation differs from Bash; for Python venv, use `source .venv/bin/activate.fish` in Fish and `source .venv/bin/activate` in Bash/Zsh.
- Windows examples should use PowerShell 7 syntax unless a task specifically requires CMD. Python launcher examples may use `py -m venv .venv`; activation in PowerShell is `.\.venv\Scripts\Activate.ps1`.
- Use `pathlib` in Python and project-relative paths instead of hard-coded `/home/...` or `C:\Users\...` paths.
- Explain Windows execution-policy errors without recommending unsafe global policy weakening. Prefer a process-scoped policy adjustment only when necessary and explain the implications.
- Explain Linux file permissions and Windows ACL/UAC separately. Never recommend running routine Python package installation with `sudo` or as Administrator.
- Use UTF-8, `.env.example` without secrets, and `.gitignore` for virtual environments, local credentials, generated data, and PHI.
- Explain CRLF/LF and Git `core.autocrlf` only where it affects the workflow.

## 4. Healthcare data safety applies on both systems

- Use synthetic or properly de-identified datasets for Academy exercises.
- Never copy real patient data to personal devices, cloud drives, public repositories, AI services, or unapproved environments.
- Apply the same access control, encryption, retention, audit, and disclosure requirements regardless of operating system.
- Do not claim that a local setup is automatically compliant with HIPAA, India's DPDP Act, ABDM requirements, or any institutional policy.
- Do not treat model outputs as clinical decisions. Require validation, governance, human oversight, and approved intended use.

## 5. Acceptance criteria for a chapter

A chapter is not considered cross-platform complete until:
- Linux setup and execution steps are present and internally consistent.
- Windows setup and execution steps are present and internally consistent.
- Shells and commands are labelled.
- Both routes reach the same defined output or an explicitly documented equivalent.
- Platform limitations and cost/licensing constraints are stated.
- Troubleshooting and verification steps exist.
- No unsafe privacy, permission, or credential practices are taught.

## 6. Learner's dual-OS competency target

By the end of the Academy, the learner should be able to:
- Set up a clean analysis workspace on Linux and Windows.
- Recreate Python/R environments and run notebooks/scripts on both.
- Query the same database from either OS.
- Use Git across both without corrupting project files or exposing data.
- Build and explain BI outputs while understanding platform-specific constraints.
- Run reproducible containerised workflows where supported.
- Move a project between Linux and Windows using Git and portable project files.
- Troubleshoot environment-specific errors independently and document the resolution.
