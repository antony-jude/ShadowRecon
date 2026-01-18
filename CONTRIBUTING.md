# Contributing to ShadowRecon

Thank you for your interest in contributing to ShadowRecon! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful and professional in all interactions. This project is intended for ethical security research only.

## How Can You Contribute?

### 1. **Report Bugs**
- Use the [Bug Report](https://github.com/yourusername/ShadowRecon/issues/new?template=bug_report.md) template
- Check if the bug has already been reported
- Include:
  - Clear description of the bug
  - Steps to reproduce
  - Expected vs actual behavior
  - Your environment details

### 2. **Suggest Features**
- Use the [Feature Request](https://github.com/yourusername/ShadowRecon/issues/new?template=feature_request.md) template
- Explain the use case and benefits
- Consider if it aligns with ShadowRecon's goals

### 3. **Submit Code**
1. **Fork** the repository
2. Create a **feature branch**: `git checkout -b feature/your-feature`
3. Make your **changes** with clear commit messages
4. **Test** your changes thoroughly
5. Submit a **Pull Request** with description

### 4. **Improve Documentation**
- Fix typos and unclear sections
- Add examples and clarifications
- Update outdated information
- Document new features

### 5. **Report Security Issues**
⚠️ **DO NOT** create public issues for security vulnerabilities.
Email security issues to: **your-email@example.com**

## Development Setup

### 1. Fork and Clone
```bash
git clone https://github.com/YOUR_USERNAME/ShadowRecon.git
cd ShadowRecon
```

### 2. Setup Development Environment
```bash
# Windows (PowerShell)
.\setup.ps1

# macOS/Linux
bash setup.sh
```

### 3. Install Development Dependencies
```bash
pip install pylint flake8 pytest pytest-cov black isort
```

### 4. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
git checkout -b bugfix/issue-number
```

## Code Style Guidelines

### Python Style (PEP 8)
- Use 4 spaces for indentation
- Maximum line length: 120 characters
- Use meaningful variable names
- Add docstrings to functions and classes

### Example
```python
def check_username(username):
    """
    Check if username exists on multiple platforms.
    
    Args:
        username (str): Username to check
        
    Returns:
        dict: Platform availability status
        
    Raises:
        ValueError: If username is empty
    """
    if not username:
        raise ValueError("Username cannot be empty")
    # Implementation here
```

### Formatting Tools
```bash
# Auto-format with Black
black modules/ main.py utils.py

# Sort imports with isort
isort modules/ main.py utils.py

# Check with Flake8
flake8 modules/ --max-line-length=120

# Lint with Pylint
pylint modules/ --max-line-length=120
```

## Testing

### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=modules --cov-report=html
```

### Writing Tests
```python
import pytest
from modules import UsernameRecon

def test_username_check():
    """Test username reconnaissance"""
    recon = UsernameRecon()
    results = recon.check_username("test_user")
    assert results is not None
    assert isinstance(results, dict)
```

## Commit Message Guidelines

### Format
```
[TYPE] Brief description

Longer explanation if needed.
- Point 1
- Point 2

Fixes #123
```

### Types
- `[FEATURE]` - New feature
- `[BUGFIX]` - Bug fix
- `[DOCS]` - Documentation
- `[REFACTOR]` - Code refactoring
- `[PERF]` - Performance improvement
- `[TEST]` - Test additions/changes
- `[CI/CD]` - CI/CD workflow changes

### Examples
```
[FEATURE] Add blockchain address reconnaissance

Implement new module for analyzing Ethereum addresses
- Query blockchain APIs
- Extract transaction history
- Calculate risk scores

Closes #42
```

```
[BUGFIX] Fix async timeout issue in domain recon

The async timeout was not properly handling slow DNS queries.
Use aiohttp timeout context manager correctly.

Fixes #89
```

## Pull Request Process

### Before Submitting
1. ✅ Code follows style guidelines (`black`, `isort`, `flake8`)
2. ✅ All tests pass (`pytest`)
3. ✅ No new warnings introduced
4. ✅ Documentation is updated
5. ✅ Commit history is clean and descriptive

### Submission
1. Use the [PR Template](.github/pull_request_template.md)
2. Link related issues: `Closes #123`
3. Describe changes clearly
4. Include any breaking changes
5. Add screenshots if UI changes

### Review Process
- Maintainers will review your PR
- Request changes may be made
- All checks must pass
- Approved PRs will be merged

## Coding Standards

### Module Structure
```python
# Imports
import os
from typing import Dict, List

# Constants
DEFAULT_TIMEOUT = 10

# Classes
class MyClass:
    """Class documentation"""
    pass

# Functions
def my_function():
    """Function documentation"""
    pass
```

### Error Handling
```python
try:
    result = fetch_data(url)
except requests.ConnectionError as e:
    logger.error(f"Connection failed: {e}")
    raise
except Exception as e:
    logger.warning(f"Unexpected error: {e}")
    return None
```

### Logging
```python
import logging

logger = logging.getLogger("ShadowRecon")

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

## Adding New Modules

### Structure
```python
# modules/newmodule.py

from utils import Utils
import logging

logger = logging.getLogger("ShadowRecon")

class NewModuleRecon:
    def __init__(self, target):
        self.target = target
    
    def recon(self):
        """Execute reconnaissance"""
        return {
            "target": self.target,
            "timestamp": Utils.format_timestamp(),
            "findings": self._gather_intelligence()
        }
    
    def _gather_intelligence(self):
        """Gather intelligence"""
        # Implementation
        pass
```

### Register Module
Add to `main.py` menu:
```python
elif choice == "X":
    target = input("Enter target: ")
    from modules import NewModuleRecon
    recon = NewModuleRecon(target)
    results = recon.recon()
    print(results)
```

## Documentation

### README Section
If adding major feature, update README:
1. Add to **Features** section
2. Add usage example
3. Add to project structure
4. Update requirements if dependencies added

### Code Comments
```python
# Bad
x = y + 1  # Add one

# Good
# Calculate next available port
next_port = last_port + 1
```

## Release Process

1. Update version in code
2. Update CHANGELOG.md
3. Create release notes
4. Tag release: `git tag v1.0.0`
5. Push tag: `git push origin v1.0.0`

## Resources

- [PEP 8 Style Guide](https://pep8.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Semantic Versioning](https://semver.org/)
- [pytest Documentation](https://docs.pytest.org/)

## Questions?

- 📖 Check [README.md](README.md)
- 🔗 Search [existing issues](https://github.com/yourusername/ShadowRecon/issues)
- 💬 Create new [discussion](https://github.com/yourusername/ShadowRecon/discussions)

## License

By contributing, you agree your code will be released under the project's license.

---

**Thank you for contributing! 🚀**
