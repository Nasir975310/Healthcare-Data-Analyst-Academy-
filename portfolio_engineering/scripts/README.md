# Portfolio helper scripts

`repository_audit.py` scans text-like files for a small set of possible secret and patient-identifier patterns. It may generate false positives and misses many sensitive formats. It is not a security scanner, DLP control, privacy review or permission to publish data.

Run from Academy root:
```bash
python portfolio_engineering/scripts/repository_audit.py /path/to/your/repository
```

Git preflight scripts inspect status, staged diff and sensitive-looking file names. Always manually inspect staged content and repository visibility.
