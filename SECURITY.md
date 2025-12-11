# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please **do not** open a public GitHub issue.

Instead, please:

1. Email the security issue to your project maintainer (create an issue or check project documentation)
2. Include a detailed description of the vulnerability
3. Provide steps to reproduce (if possible)
4. Allow time for a fix before public disclosure

## Security Best Practices

### For Users

1. **Keep Dependencies Updated**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Use Environment Variables**
   - Never commit `.env` files with secrets
   - Store API keys in environment variables
   - Use `.env.example` for configuration templates

3. **HTTPS in Production**
   - Always use HTTPS for API endpoints
   - Use SSL certificates (Let's Encrypt is free)

4. **API Authentication**
   - Implement API key validation
   - Use JWT tokens for session management
   - Set appropriate CORS policies

5. **Input Validation**
   - Validate all file uploads
   - Check file types and sizes
   - Sanitize user inputs

### For Developers

#### Code Security

```python
# ❌ Don't do this
PASSWORD = "admin123"
DATABASE_URL = "postgresql://user:pass@localhost/db"

# ✅ Do this instead
from os import getenv
PASSWORD = getenv('DB_PASSWORD')
DATABASE_URL = getenv('DATABASE_URL')
```

#### File Upload Security

```python
# ✅ Validate file uploads
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def is_allowed_file(filename):
    return '.' in filename and \
           os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS
```

#### API Security

```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# Configure CORS properly
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:8000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})
```

#### Logging Security

```python
# ❌ Don't log sensitive data
logging.info(f"User {username} with password {password} logged in")

# ✅ Only log necessary information
logging.info(f"User {username} logged in successfully")
```

## Known Security Limitations

1. **Default Configuration**: Change all default values in production
2. **Authentication**: Add proper authentication layer before production use
3. **HTTPS**: Use HTTPS for all communications
4. **Rate Limiting**: Implement rate limiting on API endpoints
5. **Database**: Use database credentials from environment variables

## Security Checklist for Production

- [ ] HTTPS enabled
- [ ] Authentication implemented
- [ ] API rate limiting configured
- [ ] Input validation in place
- [ ] Secrets in environment variables
- [ ] Database backups configured
- [ ] Logging configured (no sensitive data)
- [ ] CORS properly configured
- [ ] Dependencies kept up to date
- [ ] Security headers configured
- [ ] Error messages don't reveal system info
- [ ] File uploads restricted
- [ ] SQL injection protection (parameterized queries)
- [ ] XSS protection enabled
- [ ] CSRF tokens implemented

## Dependencies with Known Vulnerabilities

We strive to keep all dependencies up to date. Check for vulnerabilities:

```bash
pip install safety
safety check
```

Or using GitHub's dependency scanner (automatic for public repos).

## Responsible Disclosure

We appreciate responsible vulnerability disclosure. Please allow:
- 90 days for a fix and release
- 14 days additional for patch releases
- Public disclosure after fix is released

## Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security](https://flask.palletsprojects.com/en/2.0.x/security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- [Secure Coding Guidelines](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)

## Updates

Security updates will be:
- Released as soon as possible
- Marked as `[SECURITY]` in commit messages
- Announced in release notes
- Backported to recent versions if necessary

---

**Thank you for helping keep this project secure!**
