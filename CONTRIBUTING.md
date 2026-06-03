# Contributing to Process Monitor CLI

Thank you for your interest in contributing to Process Monitor CLI! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

Before creating bug reports, check the issue list as you might find that the issue has already been reported.

When creating a bug report, include as many details as possible:
- **Use a clear, descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed**
- **Explain which behavior you expected and why**
- **Include error messages and stack traces**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:
- **Use a clear, descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and expected behavior**

### Pull Requests

- Follow the Python [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Include appropriate docstrings and type hints
- Add or update tests as needed
- Update README.md if behavior changes
- Run `python -m unittest discover -s tests` before submitting

## Development Setup

1. Fork the repository and clone locally:
```bash
git clone https://github.com/YOUR_USERNAME/process-monitor-cli.git
cd process-monitor-cli
```

2. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

4. Make your changes and test:
```bash
python main.py list
python -m unittest discover -s tests
```

5. Commit and push:
```bash
git add .
git commit -m "Description of changes"
git push origin feature/your-feature-name
```

6. Create a pull request on GitHub

## Code Guidelines

- Write clear, descriptive commit messages
- One feature or fix per pull request
- Add tests for new functionality
- Update documentation as needed
- Use type hints for function arguments and return values
- Include docstrings for public methods and classes

## Running Tests

```bash
# Run all tests
python -m unittest discover -s tests -v

# Run specific test class
python -m unittest tests.test_basic.TestAnalyzer -v

# Run specific test
python -m unittest tests.test_basic.TestAnalyzer.test_sort_by_cpu -v
```

## Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use meaningful variable names
- Keep functions focused and concise
- Maximum line length: 100 characters
- Use `from __future__ import annotations` for modern type hints

## License

By contributing to Process Monitor CLI, you agree that your contributions will be licensed under the MIT License.
