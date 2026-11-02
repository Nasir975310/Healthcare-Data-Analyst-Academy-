# Scoring method and limitations

The evaluator is deterministic Python using the standard library. It reads a job-description text file and compares detected keyword groups with a user-editable profile. It is not an LLM, ATS replica, validated psychometric instrument, recruiter decision, or hiring-probability model.

| Dimension | Maximum |
|---|---:|
| Skills/tools group coverage | 35 |
| Education alignment | 15 |
| Experience alignment | 15 |
| Remote alignment | 10 |
| Healthcare-domain alignment | 10 |
| Transferable baseline | 15 |

Penalties: senior/lead/manager wording (-15), explicit higher-degree barrier (-20), and detected red-flag categories (-10 each, capped at -25). Scores are capped at 0–100. Keyword presence can be misleading; review the full vacancy manually. Missing keyword detection is not proof that a skill is unnecessary. Years parsing is intentionally conservative and can miss complex wording.

Risk patterns are screening prompts, not proof of fraud. A clean result does not certify an employer. Verify identity, vacancy, contract and payment terms independently. Never send OTPs or passwords or pay a fee to secure employment.

Default profile reflects an entry-level Pharm.D candidate with healthcare-domain context and listed learning/portfolio skills. Edit `examples/sample_profile.json` to remove skills you cannot currently demonstrate and add only verifiable evidence. The profile is an editable starter, not a certification of proficiency.
