# Support ticket agent

A support ticket agent built for learning and a portfolio.

## Stack
- agent/: Python, FastAPI and LangGraph
- mcp-server/: Java 21, Spring Boot and Spring AI MCP server
- data/: synthetic tickets and help docs
- evals/: test sets and scoring
- infra/: Docker Compose for Postgres and Qdrant
- Local model through Ollama; Amazon Bedrock later

## Rules
- Use only synthetic data. No real customer data or former employer code.
- Never commit secrets. Keep keys in .env, which Git ignores.
- Write tests for new code and keep changes small.
