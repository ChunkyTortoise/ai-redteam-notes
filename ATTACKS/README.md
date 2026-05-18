# ATTACKS Directory

This directory contains structured attack entries documenting various red team techniques, vulnerabilities, and exploitation methods.

## Structure

Each attack entry follows a standardized format defined in [_template.md](_template.md) and includes:

- **Metadata Frontmatter**: YAML-formatted header with disclosure information, dates, and classification
- **Technical Description**: Detailed explanation of the attack vector
- **MITRE ATT&CK Mapping**: References to relevant tactics and techniques
- **Proof of Concept**: Example commands, scripts, or demonstrations
- **Detection & Mitigation**: Guidance on identifying and defending against the attack
- **References**: Links to related research, advisories, or tools

## Validation

All attack entries are automatically validated by CI pipelines using:
- `pipeline/scripts/check-attack-entry.sh`: Validates structure and required sections
- `pipeline/scripts/check-disclosure.sh`: Ensures proper disclosure metadata

## Contributing

When adding new attack entries:
1. Copy `_template.md` to a new file with descriptive name (YYYY-MM-DD-descriptive-title.md)
2. Fill in all sections according to the template guidelines
3. Ensure the entry passes validation scripts before submitting a PR
4. Include appropriate MITRE ATT&CK tactic/technique mappings
