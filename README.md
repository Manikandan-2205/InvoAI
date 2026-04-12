# InvoAI

## Description
InvoAI is an AI-powered Invoice OCR Automation System built with Python. It extracts key details and tables from PDF or image invoices using OCR and machine learning, returning clean JSON via API with an interactive UI for visualization and validation.

## Best Practices

### Project Structure
- Follow PEP8 guidelines for Python code
- Organize modules by responsibility (models, repositories, services)
- Use Alembic for database migrations

### Development Workflow
1. Clone repository
2. Set up virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Configure environment variables in `.env`
5. Run migrations: `alembic upgrade head`
6. Test API endpoints via Swagger UI (`/api/docs`)

### Code Quality
- Write unit tests for critical components
- Document endpoints with Swagger-style comments
- Use type hints where possible

### Development Resources
- Documentation: `/docs` directory
- Code style: Enforced via linter
- Database schema: Defined in Alembic migrations

### Deployment
- Dockerize for production
- Use reverse proxy (e.g., Traefik) for HTTPS
- Set up monitoring for API performance

## Contributing

1. Fork this repository
2. Create a branch for your feature/bugfix
3. Write tests for new functionality
4. Submit pull request with clear description

## License
MIT

## Badges
[Build Status](https://github.com/manikandan-2205/claude-code/statuses)
[Code Coverage](https://github.com/manikandan-2205/claude-code/coverage)
[Version](https://github.com/manikandan-2205/claude-code/releases)