# Contributing to AI-Based Smart Traffic Signal Control System

Thank you for your interest in contributing! We welcome all contributions to improve this project.

## 🚀 How to Contribute

### 1. Fork the Repository
```bash
git clone https://github.com/your-username/AI-Based-Smart-Traffic-Signal-Control-System.git
cd AI-Based-Smart-Traffic-Signal-Control-System
```

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or for bug fixes
git checkout -b bugfix/issue-name
```

### 3. Make Your Changes
- Follow the existing code style
- Add comments for complex logic
- Update documentation if needed
- Test your changes thoroughly

### 4. Commit Your Changes
```bash
git add .
git commit -m "feat: add your feature description"
# or
git commit -m "fix: resolve issue with xyz"
```

**Commit Message Format:**
- `feat:` - A new feature
- `fix:` - A bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring without feature changes
- `test:` - Adding or updating tests
- `perf:` - Performance improvements

### 5. Push to Your Fork
```bash
git push origin feature/your-feature-name
```

### 6. Submit a Pull Request
- Go to GitHub and click "New Pull Request"
- Select your branch
- Provide a clear description of your changes
- Link any related issues

## 📋 Before You Submit

### Code Quality
- [ ] Code follows the project's style guide
- [ ] No unnecessary console.log or print statements
- [ ] Functions are well-documented
- [ ] No hardcoded values (use config file)

### Testing
- [ ] Changes tested locally
- [ ] All existing features still work
- [ ] Edge cases considered

### Documentation
- [ ] README updated if needed
- [ ] API documentation updated
- [ ] Comments added for complex logic

## 🐛 Reporting Bugs

### Before Reporting
- Check existing issues
- Test with the latest version
- Verify it's not a configuration issue

### Create a Bug Report
Include:
1. **Environment**: OS, Python version, browser
2. **Steps to reproduce**: Clear step-by-step instructions
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happens
5. **Logs**: Relevant error logs from `traffic_system.log`
6. **Screenshots**: If applicable

## 💡 Suggesting Features

- Check existing issues and discussions
- Describe the feature clearly
- Explain the use case and benefit
- Suggest implementation approach (if applicable)

## 🏗️ Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests (if available)
pytest

# Run the system
python run_system.py
```

## 📝 Code Style Guide

### Python
- Use PEP 8 style guide
- Max line length: 100 characters
- Use meaningful variable names
- Add docstrings to functions

```python
def detect_vehicles(image_path):
    """
    Detect vehicles in an image using YOLOv11.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        dict: Detection results with vehicle count and types
    """
    pass
```

### JavaScript
- Use camelCase for variables and functions
- Use meaningful names
- Add comments for complex logic
- Use const/let, not var

```javascript
function updateTrafficLight(direction, state) {
    // Update the traffic light display
    const light = document.getElementById(`${direction}-light`);
    light.className = state;
}
```

### HTML/CSS
- Use semantic HTML
- Use CSS classes for styling
- Keep inline styles minimal

## 🔍 Code Review Process

1. **Automated checks**: GitHub Actions will run tests
2. **Manual review**: Maintainers will review your code
3. **Feedback**: Changes may be requested
4. **Approval**: Once approved, your PR will be merged

## 📦 Adding Dependencies

If you add a new Python package:
1. Update `requirements.txt`
2. Document why it's needed in the PR
3. Ensure it doesn't conflict with existing packages

```bash
pip freeze > requirements.txt
```

## 🚀 Release Process

Versions follow [Semantic Versioning](https://semver.org/):
- `1.0.0` = MAJOR.MINOR.PATCH
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙌 Recognition

Contributors will be acknowledged in:
- README.md
- Commit history
- Release notes

## ❓ Questions?

- Open an issue with the label `question`
- Check existing discussions
- Comment on related issues

---

**Thank you for contributing! 🎉**
