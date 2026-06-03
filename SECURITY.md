# Security Policy

## Supported Versions

Currently, only version 0.1.0 is actively maintained:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.0   | :white_check_mark: |

## Reporting a Vulnerability

**Do not** open public issues for security vulnerabilities. Instead, please email security concerns to the project maintainers or open a private security advisory on GitHub.

When reporting a security issue, please include:

1. **Description**: What is the vulnerability?
2. **Location**: Which component(s) are affected?
3. **Impact**: What is the potential impact?
4. **Reproduction**: Steps to reproduce (if applicable)
5. **Suggested Fix**: Any ideas for fixing the issue

## Security Considerations

### Permission Requirements

This tool requires appropriate permissions to access process information:

- **User processes**: Can read own processes without additional permissions
- **System processes**: May require elevated privileges (`sudo`) for full information
- **Root processes**: Requires root access to list all details

### Data Privacy

Process information collected by this tool may include:
- Command-line arguments (may contain sensitive data)
- Environment variables (stored in process memory)
- File paths and working directories
- Network connection details

**Never** export sensitive process data to shared systems or untrusted networks.

### Known Limitations

1. **Permission Denied**: Some process information is restricted by the OS
2. **Zombie Processes**: Limited information available for zombie processes
3. **Real-time Data**: Snapshots are point-in-time; processes may change between samples

## Security Best Practices

When using Process Monitor CLI:

1. **Use locally only**: Run on the system you wish to monitor
2. **Restrict exports**: Keep JSON exports in secure locations
3. **Handle output carefully**: Process lists may contain sensitive information
4. **Update dependencies**: Keep psutil and rich libraries current
5. **Review output**: Check for unexpected processes or behaviors

## Dependencies Security

This project depends on:

- **psutil**: Cross-platform system and process utilities
- **rich**: Rich terminal formatting and output
- **typer**: CLI framework with type hints

All dependencies are regularly checked for security updates. To update:

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## Vulnerability Disclosure Timeline

We follow responsible disclosure practices:

1. **Initial Report**: Acknowledged within 24 hours
2. **Investigation**: Completed within 7 days
3. **Fix Development**: Completed as soon as possible
4. **Release**: Published without disclosing details until fix is available
5. **Public Announcement**: Details shared after users have time to update

## Questions?

For security-related questions or concerns not covered here, please contact the project maintainers privately.
