# Chinar website

## Getting started

1. Clone the repository

```bash
git clone https://github.com/Ilkin777dev/Chinar_WEB.git
```

2. Build Docker image

```bash
docker build -t chinar_web .
```

3. Create `.env` file

```bash
touch .env
```

4. Add environment variables to `.env` file

```env
ADMIN_EMAIL=admin@email.com
ADMIN_PASSWORD=admin_password
SECRET_KEY=your_secret_key
```

5. Run Docker container

```bash
docker run -d --env-file=.env -p 80:80 -v /root/chinarv:/chinarv rasadov/chinar
```