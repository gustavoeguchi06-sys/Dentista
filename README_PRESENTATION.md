# Presentation Quick Start

1. Start server:
```bash
cd "c:\Users\insti\Downloads\Dentista1"
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

2. Open in browser: http://127.0.0.1:8000/

3. Demo credentials:
- user: demo
- password: demo123

4. What to check:
- After login you will be redirected to `/pacientes/` with sample patients.
- Test navigation to Agenda, Prontuários, Estoque, Financeiro.
- Click `Sair` to logout and return to the login screen.

5. Troubleshooting
- If login fails, clear browser cookies for 127.0.0.1 and retry.
- If a `DisallowedHost` error appears in tests, ensure `ALLOWED_HOSTS` includes your host or use the provided commands.

6. Optional: Create superuser
```bash
python manage.py createsuperuser
```

Good luck with the presentation!