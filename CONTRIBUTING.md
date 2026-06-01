# Contributing to ML Learning Pathway

Thank you for your interest in contributing to the ML Learning Pathway project! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and inclusive in all interactions. We are committed to providing a harassment-free environment for everyone.

## How to Contribute

### 1. Fork the Repository

```bash
git clone https://github.com/YOUR-USERNAME/ML-Learning-Pathway.git
cd ML-Learning-Pathway
git remote add upstream https://github.com/channel4fun2020-lang/ML-Learning-Pathway.git
```

### 2. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes

- Keep commits atomic and well-documented
- Follow PEP 8 style guide for Python
- Add tests for new functionality
- Update documentation as needed

### 4. Test Your Changes

```bash
pytest tests/
```

### 5. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 6. Create a Pull Request

- Provide a clear title and description
- Reference any related issues
- Include before/after screenshots if UI changes

## Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install black flake8 pytest pytest-cov

# Run tests
pytest
```

## Code Style

- Use `black` for code formatting
- Use `flake8` for linting
- Follow PEP 257 for docstrings
- Use type hints where applicable

```bash
black .
flake8 .
```

## Pull Request Process

1. Update documentation
2. Add tests for new features
3. Ensure all tests pass
4. Update the changelog
5. Request reviews from maintainers

## Reporting Issues

- Use GitHub Issues to report bugs
- Provide clear steps to reproduce
- Include error messages and logs
- Specify Python version and OS

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to reach out to the maintainers or open a discussion in the GitHub Discussions tab.

Happy Contributing! 🚀
