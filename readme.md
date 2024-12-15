# Secure File Sharing Web Application

**Version Info:**
- Python: 3.11
- Django: 4.x
- Node: 18.x
- React: 18.x
- TypeScript: 4.x
- Redux Toolkit: 1.9+
- Poetry: 1.4+
- Docker & docker-compose: Latest stable

This application provides a secure file-sharing platform with:
- User registration, login, logout
- Multi-Factor Authentication (Still inder development) via TOTP (e.g., Google Authenticator)
- Role-Based Access Control (Admin, User, Guest)
- Client-side and server-side file encryption (AES-256)
- Secure share links with expiration
- JWT-based authentication with HttpOnly cookies
- Strict security best practices (HTTPS, bcrypt for passwords, sanitized inputs, etc.)

## Setup Instructions

1. **Clone the repository**:
   ```bash
   cd secure-file-share

2. **Run via Docker Compose**
```bash 
    docker-compose up --build
```

3. **Testing Run backend tests**:
```bash
docker-compose exec backend poetry run python manage.py test

