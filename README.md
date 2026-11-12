# AI RAG Assistant

A practical Django application that answers questions using documents stored in PostgreSQL.

Built for the Linuxademy course **Build & Deploy an AI Web App with Django + DigitalOcean**, offered in partnership with AI Certification Council (AICC).

## What It Does

- Add, view, and delete knowledge documents.
- Split documents into smaller chunks.
- Generate embeddings using the OpenAI API.
- Retrieve relevant chunks when someone asks a question.
- Generate an answer using the retrieved information.
- Display the titles of retrieved source documents.

When the supplied information does not support an answer, the assistant is instructed to respond:

> I don't know based on the knowledge base.

AI responses can still be incorrect. Retrieved source titles indicate which documents were supplied to the model; they do not guarantee that those documents support every statement.

## Technology

Python · Django · PostgreSQL · OpenAI API · Gunicorn · Docker · Kamal · DigitalOcean

Embeddings are stored as JSON in PostgreSQL and compared in Python. This implementation is intended for a small knowledge base.

## Course and Resources

- [Linuxademy YouTube](https://www.youtube.com/@Linuxademy)
- [Linuxademy](https://linuxademy.com)
- [AI Certification Council](https://www.aicertificationcouncil.com)

## Development Environment

The course uses Windows 11 with WSL2 and Ubuntu 24.04.

Install these tools before starting:

- Python 3.12 with virtual environment support.
- PostgreSQL.
- Git.

Docker Engine, Ruby, and Kamal are needed for the later deployment steps.

## Run Locally

Open a terminal in this repository.

### 1. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 2. Start PostgreSQL

```bash
sudo systemctl start postgresql
```

### 3. Create the Database

Open PostgreSQL:

```bash
sudo -u postgres psql
```

Create the role and database:

```sql
CREATE USER ai_rag_assistant;
CREATE DATABASE ai_rag_assistant_production OWNER ai_rag_assistant;
```

Set the role's password:

```text
\password ai_rag_assistant
```

Exit PostgreSQL:

```text
\q
```

If this role and database already exist, reuse them instead of running the creation commands again.

### 4. Configure Environment Variables

Generate a Django secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Create `.env` in the project root:

```dotenv
DJANGO_SECRET_KEY=YOUR_GENERATED_DJANGO_SECRET_KEY
DJANGO_DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=ai_rag_assistant_production
POSTGRES_USER=ai_rag_assistant
POSTGRES_PASSWORD=YOUR_POSTGRES_PASSWORD
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432

OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

Replace the placeholders with your own values. Use the PostgreSQL password you set above.

Keep `.env` private. OpenAI API usage is billed separately.

If this terminal contains database variables from another project, clear them before starting Django:

```bash
unset POSTGRES_DB POSTGRES_USER POSTGRES_PASSWORD POSTGRES_HOST POSTGRES_PORT DATABASE_URL
```

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Start Django

```bash
python manage.py runserver
```

Open:

http://127.0.0.1:8000/

Add a document and ask a question about its contents.

Health endpoint:

http://127.0.0.1:8000/health/

Press **Ctrl+C** to stop Django.

## Run with Docker in WSL

Create the Docker environment file:

```bash
cp .env .env.docker
```

Confirm that `.env.docker` uses:

```dotenv
POSTGRES_HOST=127.0.0.1
```

Build the image:

```bash
docker build -t ai_rag_assistant .
```

Stop any application already listening on port 8000, then run:

```bash
docker run --rm \
  --network host \
  --env-file .env.docker \
  ai_rag_assistant
```

Open http://127.0.0.1:8000/.

This command uses Linux host networking so the container can reach PostgreSQL running in WSL at `127.0.0.1`.

The container uses the same local database as the development server.

Press **Ctrl+C** to stop the container.

## Deployment Configuration

`config/deploy.yml` contains the instructor's deployment IP address and domain.

**Replace both server IP entries, `proxy.host`, and the domain in `ALLOWED_HOSTS` with your own values before running Kamal. Do not deploy to the instructor's server.**

Create your own `.kamal/secrets` file:

```dotenv
DJANGO_SECRET_KEY=YOUR_PRODUCTION_DJANGO_SECRET_KEY
POSTGRES_PASSWORD=YOUR_PRODUCTION_POSTGRES_PASSWORD
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

Follow the course's deployment lessons for SSH access, DNS, registry configuration, Kamal setup, and production migrations.

Production uses a separate PostgreSQL database. Local documents are not automatically copied to the server.

## Before Making Your Site Public

This is educational course code. Review the application before inviting public users:

- Restrict adding and deleting knowledge to authorized users.
- Protect private documents and their contents.
- Restrict public access to paid AI requests and set appropriate usage limits.
- Keep production debugging disabled.
- Keep credentials outside Git and Docker images.
- Arrange database backups if you need to retain the data.

Do not assume that creating a Django administrator account automatically protects custom application views.

## Secret Files

Never commit:

```text
.env
.env.docker
.kamal/secrets
```

Never upload private SSH keys or database backups containing sensitive information.

If a real credential is exposed, revoke or rotate it. Adding a file to `.gitignore` does not remove earlier committed copies.

## Acknowledgment

Created by Linuxademy in partnership with AI Certification Council (AICC).

Learn by building. Understand your systems. Operate independently.
