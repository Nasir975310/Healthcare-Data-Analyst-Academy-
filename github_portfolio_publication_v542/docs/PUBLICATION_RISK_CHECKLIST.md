# Publication risk checklist

- [ ] Dataset provenance is documented and permission to publish is established.
- [ ] No real patient data, identifiers, dates of service or free-text clinical notes.
- [ ] No credentials, API keys, tokens, private keys or local configuration files.
- [ ] No confidential employer/client material.
- [ ] No runtime databases, local logs, caches, temporary exports or personal paths.
- [ ] No screenshots containing account details or personal information.
- [ ] README claims match actual code and evidence.
- [ ] Limitations clearly distinguish synthetic education from real-world healthcare analytics.
- [ ] License decision is deliberate and legally appropriate.
- [ ] Git history has been reviewed; removing a secret from the latest commit is insufficient if it remains in history.
- [ ] Repository visibility is intentional.
- [ ] Fresh-clone reproduction is complete and recorded.

**Stop condition:** Any unresolved privacy, credential, ownership or provenance concern means do not publish.
