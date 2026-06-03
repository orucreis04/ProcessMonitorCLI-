# Process Monitor CLI

A powerful, modular command-line tool for monitoring, analyzing, and reporting on running system processes on Linux/Fedora platforms. Built with Python for system administrators, security professionals, and DevOps engineers.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Linux%2FFedora-red)

## Features

✨ **Process Monitoring**
- Real-time process collection and monitoring
- Periodic snapshots with configurable refresh intervals
- Detailed resource usage metrics (CPU, memory)

📊 **Process Listing & Sorting**
- List all running processes with rich table formatting
- Sort by CPU, memory, PID, or process name
- Configurable process limit
- UTF-8 support for process names

🔒 **Security Risk Analysis**
- Automated risk scoring system
- Intelligent threat detection
- Risk categorization (LOW/MEDIUM/HIGH)
- Suspicious process identification
- Rule-based analysis engine

🔍 **Process Details**
- Comprehensive process information display
- Command-line arguments and working directory
- Open file handles and network connections
- Memory breakdown (RSS/VMS)
- Process relationships (PID/PPID)

📁 **JSON Export**
- Export process lists to JSON format
- Integrated risk analysis results
- ISO 8601 timestamps
- UTF-8 encoded output
- Perfect for automated reporting and integration

🛡️ **Robust Error Handling**
- Graceful handling of permission denied errors
- Support for zombie processes
- Safe process information gathering

## Technology Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | 3.11+ | Core language |
| psutil | 6.0.0+ | Process information collection |
| rich | 13.7.0+ | Terminal UI and formatting |
| typer | 0.12.5+ | CLI framework |

## Installation

### Prerequisites

- Python 3.11 or higher
- Linux/Fedora operating system
- pip package manager

### Step-by-Step Setup

1. **Clone the repository**
```bash
git clone https://github.com/orucreis04/ProcessMonitorCLI-.git
cd ProcessMonitorCLI-
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Verify installation**
```bash
python main.py --help
```

5. **Run tests**
```bash
python -m unittest discover -s tests
```

### Fedora-Specific Notes

If you encounter `psutil` compilation issues on Fedora:

```bash
sudo dnf install python3-devel gcc
pip install --upgrade pip setuptools
pip install -r requirements.txt
```

## Usage

All commands below are run from the project root after installing dependencies.

### Monitor Command
Collect and display process metrics periodically.

```bash
# Single snapshot
python main.py monitor

# Multiple snapshots with 2-second intervals
python main.py monitor -r 2 -n 3

# Options
python main.py monitor --help
```

### List Command
List all running processes with sorting and filtering.

```bash
# Default (CPU usage, top 20)
python main.py list

# Sort by memory usage
python main.py list --sort memory --limit 10

# Sort by process name
python main.py list --sort name --limit 50

# Export to JSON
python main.py list --json processes.json
python main.py list --json report.json --sort memory

# All options
python main.py list --help
```

### Scan Command
Analyze processes for security risks.

```bash
# Basic risk analysis
python main.py scan

# Custom limit
python main.py scan --limit 30

# Export with risk analysis
python main.py scan --json security_report.json

# Show help
python main.py scan --help
```

### Detail Command
Display comprehensive information about a specific process.

```bash
# Process 1 (init)
python main.py detail 1

# Process 1234
python main.py detail 1234

# PID not found
python main.py detail 99999
```

## Risk Analysis Rules

The risk scoring system evaluates processes based on:

| Criterion | Points | Trigger |
|-----------|--------|---------|
| High CPU Usage | +30 | ≥ 80% |
| High Memory Usage | +25 | ≥ 50% |
| Unknown Process Name | +20 | `<unknown>` |
| Running as Root | +10 | uid=0 |
| Suspicious Keywords | +40 | miner, crypto, payload, reverse, backdoor, nc, netcat |

### Risk Levels

- **LOW** (0-29 points): No significant issues
- **MEDIUM** (30-59 points): Requires attention
- **HIGH** (60-100 points): Immediate investigation recommended

## Project Structure

```
process-monitor-cli/
├── process_monitor/
│   ├── __init__.py           # Package initialization
│   ├── cli.py                # CLI command definitions
│   ├── monitor.py            # Process monitoring engine
│   ├── analyzer.py           # Risk analysis & evaluation
│   ├── reporter.py           # Output formatting & export
│   └── utils.py              # Utility functions
├── tests/
│   └── test_basic.py         # Basic unit tests
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .gitignore                # Git ignore patterns
└── LICENSE                   # MIT License
```

## Development Checklist

This project is designed as a small junior system/cyber security portfolio CLI:

- Linux/Fedora process enumeration with `psutil`
- Type hints and docstrings on the main modules
- Friendly CLI errors for invalid input and missing PIDs
- JSON export for reports and automation
- Basic unit tests for analyzer, monitor, and reporter behavior

## Example Output

### Monitor Command
```
                    Process Monitor Snapshot 1/1
┏━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━━┳━━━━━━┓
┃ PID ┃ Name                    ┃ User     ┃ CPU % ┃ MEM % ┃ Status   ┃ Flag ┃
┡━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━━╇━━━━━━┩
│   1 │ init                    │ root     │   0.0 │   0.1 │ sleeping │  OK  │
│  22 │ code                    │ user     │   0.1 │   1.8 │ running  │  OK  │
│ 165 │ python3                 │ user     │   0.5 │   2.1 │ sleeping │  OK  │
└─────┴─────────────────────────┴──────────┴───────┴───────┴──────────┴──────┘
```

### Scan Command
```
                  Security Risk Analysis (40 total processes)
┏━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┓
┃ PID ┃ Name     ┃ User     ┃ CPU % ┃ MEM % ┃ Risk Score┃ Risk Level┃ Reason    ┃
┡━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━┩
│   1 │ init     │ root     │   0.0 │   0.1 │         0 │   LOW    │ No issues │
│  22 │ code     │ user     │   0.1 │   1.8 │         0 │   LOW    │ No issues │
└─────┴──────────┴──────────┴───────┴───────┴───────────┴──────────┴───────────┘
```

### Detail Command
```
╭───── Basic Information ──────╮
│ PID: 22                      │
│ PPID: 1                      │
│ Name: code                   │
│ User: user                   │
│ Status: sleeping             │
│ Created: 2026-06-03 13:59:20 │
╰──────────────────────────────╯

╭─────────────────────────── Execution Information ────────────────────────────╮
│ Command: /usr/bin/code --reuse-window                                        │
│ Working Dir: /home/user                                                      │
╰──────────────────────────────────────────────────────────────────────────────╯

╭────── Resource Usage ──────╮
│ CPU Usage: 0.1%            │
│ Memory Usage: 1.8%         │
│ Memory (RSS): 260.5 MB     │
│ Memory (VMS): 2480.2 MB    │
╰────────────────────────────╯
```

## JSON Export Format

Export process data and analysis results in JSON format for integration with external tools.

```json
{
  "timestamp": "2026-06-03T14:38:17.837569",
  "total_processes": 40,
  "processes": [
    {
      "pid": 1,
      "name": "init",
      "user": "root",
      "cpu_percent": 0.0,
      "memory_percent": 0.10,
      "status": "sleeping",
      "start_time": "2026-06-03 10:00:00",
      "suspicious": false,
      "risk_score": 0,
      "risk_level": "LOW",
      "risk_reason": "No issues detected"
    },
    {
      "pid": 22,
      "name": "code",
      "user": "user",
      "cpu_percent": 0.1,
      "memory_percent": 1.8,
      "status": "running",
      "start_time": "2026-06-03 13:59:20",
      "suspicious": false,
      "risk_score": 0,
      "risk_level": "LOW",
      "risk_reason": "No issues detected"
    }
  ]
}
```

## Security Considerations

⚠️ **Important Security Notes:**

1. **Permissions**: Some process information requires elevated privileges. Use `sudo` if needed:
   ```bash
   sudo python main.py scan
   ```

2. **Permission Denied**: The tool gracefully handles access denied errors. Processes you can't access will show `<access denied>` for restricted fields.

3. **No Privilege Escalation**: This tool does not request or escalate privileges. It respects system security boundaries.

4. **Local Use Only**: Designed for local system monitoring. Not recommended for remote execution without proper security considerations.

5. **Data Privacy**: Process information collected may contain sensitive data. Handle exports carefully.

## Future Enhancements

Planned features for upcoming versions:

- 📈 Process history and trending
- 🔔 Alert system for threshold violations
- 📧 Email notifications for critical risks
- 💾 Database logging and analytics
- 🌐 Web interface dashboard
- 📊 Performance profiling
- 🔗 Integration with SIEM systems
- 🎯 Custom rule definition system
- 🔄 Recursive process tree visualization
- 📱 Mobile app companion

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

## Testing

Run the test suite:

```bash
python -m unittest discover -s tests
```

## Troubleshooting

### Permission Denied Errors

Some process details are restricted by Linux permissions. Run `detail` with your own user's processes first, and use `sudo python main.py detail <PID>` only when you intentionally need elevated access.

### ModuleNotFoundError

Ensure virtual environment is activated:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### psutil Issues on Fedora

```bash
sudo dnf install python3-devel gcc libffi-devel openssl-devel
pip install --upgrade psutil
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

MIT License grants you the freedom to use, modify, and distribute this software.

## Author

**Process Monitor CLI**  
Created as a professional system monitoring tool for Linux/Fedora environments.

## Support

For issues, questions, or suggestions:
- Check existing GitHub issues
- Review the troubleshooting section above
- Create a new issue with detailed information
- Include system info: `python --version`, `uname -a`

## Changelog

### Version 0.1.0 (Initial Release)
- ✅ Process monitoring and listing
- ✅ Risk analysis system
- ✅ Detailed process information
- ✅ JSON export functionality
- ✅ Rich terminal UI
- ✅ Comprehensive error handling

---

**Made for System Administrators, Linux learners, and junior security analysts**
