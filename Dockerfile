# Use the official Python lightweight image
FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install the project into /app
COPY . /app
WORKDIR /app

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED=1
#ENV PORT=8000
ENV GCP_OAUTH_CLIENT_ID=943485064678-38g66nnbf9b4sut9h3q7applid9e8s3n.apps.googleusercontent.com
ENV PORT=8000
ENV GCP_OAUTH_ALLOWED_EMAILS=aagirre92@gmail.com,andoni.agirre.bullhost@gmail.com

# Install dependencies
RUN uv sync

EXPOSE $PORT

# Run the FastMCP server
CMD ["uv", "run", "mcp-server-oauth-gcp-cloudRun.py"]