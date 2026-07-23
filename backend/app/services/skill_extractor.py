"""Extract skills from job descriptions using keyword matching."""

import re
import logging

logger = logging.getLogger(__name__)

# A comprehensive set of tech skills commonly found in job descriptions.
TECH_SKILLS = {
    # Languages
    "python",
    "javascript",
    "typescript",
    "java",
    "go",
    "golang",
    "rust",
    "c++",
    "c#",
    "ruby",
    "php",
    "swift",
    "kotlin",
    "scala",
    "perl",
    "r",
    "matlab",
    "sql",
    "bash",
    "shell",
    "elixir",
    "dart",
    # Web frameworks
    "fastapi",
    "flask",
    "django",
    "react",
    "angular",
    "vue",
    "svelte",
    "next.js",
    "nuxt",
    "express",
    "spring",
    "spring boot",
    "rails",
    "laravel",
    "asp.net",
    "node.js",
    "deno",
    "htmx",
    # Databases
    "postgresql",
    "postgres",
    "mysql",
    "mongodb",
    "redis",
    "elasticsearch",
    "cassandra",
    "dynamodb",
    "sqlite",
    "mariadb",
    "oracle",
    "cockroachdb",
    "neo4j",
    "influxdb",
    "clickhouse",
    # Cloud & DevOps
    "aws",
    "azure",
    "gcp",
    "google cloud",
    "docker",
    "kubernetes",
    "k8s",
    "terraform",
    "ansible",
    "jenkins",
    "github actions",
    "gitlab ci",
    "circleci",
    "argo",
    "helm",
    "prometheus",
    "grafana",
    "datadog",
    "new relic",
    "sentry",
    "cloudflare",
    # Data & ML
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "keras",
    "spark",
    "hadoop",
    "airflow",
    "dbt",
    "snowflake",
    "bigquery",
    "databricks",
    "mlflow",
    "kafka",
    "flink",
    # Tools & Concepts
    "git",
    "rest",
    "graphql",
    "grpc",
    "docker",
    "ci/cd",
    "microservices",
    "event-driven",
    "serverless",
    "oauth",
    "jwt",
    "tdd",
    "agile",
    "scrum",
    "linux",
    "unix",
    "nginx",
    "rabbitmq",
    "celery",
    # Python-specific
    "sqlalchemy",
    "pydantic",
    "alembic",
    "pytest",
    "poetry",
    "pip",
    "asyncio",
    "uvicorn",
    "gunicorn",
    "pydantic",
}


def extract_skills(text: str) -> list[str]:
    """Extract known tech skills from a block of text.

    Performs case-insensitive matching and returns a deduplicated,
    sorted list of skills found in the text.
    """
    if not text:
        return []

    lower = text.lower()
    found: set[str] = set()

    for skill in TECH_SKILLS:
        # Build a pattern that matches the skill as a whole word.
        # Escape dots (e.g. "c#" -> "c#", "node.js" -> "node\.js")
        escaped = re.escape(skill)
        pattern = rf"\b{escaped}\b"
        if re.search(pattern, lower):
            found.add(skill)

    return sorted(found)
