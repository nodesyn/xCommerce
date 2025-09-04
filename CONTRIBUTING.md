# Contributing to xCommerce

Thank you for your interest in contributing to xCommerce! We welcome contributions from the community.

## Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/xCommerce.git
   cd xCommerce
   ```

3. **Set up virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Set up database**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Run development server**:
   ```bash
   python manage.py runserver
   ```

## Making Changes

1. **Create a new branch** for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards
3. **Write tests** for new functionality
4. **Run tests** to ensure nothing is broken:
   ```bash
   python manage.py test
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: description of your changes"
   ```

## Coding Standards

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Write docstrings for functions and classes
- Keep functions small and focused
- Use type hints where appropriate

## Code Style

We use the following tools to maintain code quality:

- **Black** for code formatting
- **flake8** for linting
- **isort** for import sorting

Run these before committing:
```bash
black .
flake8 .
isort .
```

## Testing

- Write unit tests for new features
- Ensure all tests pass before submitting PR
- Include integration tests for complex features
- Test on different browsers for frontend changes

## Pull Request Process

1. **Update documentation** if needed
2. **Add changelog entries** for significant changes
3. **Create pull request** with clear description
4. **Link related issues** in PR description
5. **Respond to feedback** promptly

## Commit Message Format

Use conventional commit format:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

Example:
```
feat: add product review system

- Add review model with ratings
- Create review form and templates
- Include review display on product pages
```

## Issue Reporting

When reporting issues:

1. **Search existing issues** first
2. **Use issue templates** provided
3. **Include system information**
4. **Provide reproduction steps**
5. **Add screenshots** if helpful

## Feature Requests

For new features:

1. **Check existing feature requests**
2. **Discuss in issues** before implementing
3. **Consider backwards compatibility**
4. **Update documentation**

## Documentation

- Keep README.md updated
- Update API documentation
- Add docstrings to new functions
- Include examples in documentation

## Questions?

- Create a GitHub issue for questions
- Join our community discussions
- Check existing documentation first

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to xCommerce!