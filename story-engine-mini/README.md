# SLAG Story Engine Mini

A streamlined version of the Story & Literature Auto Generation (SLAG) system, designed for generating short stories using AI.

## Features
- Short story generation (5,000 - 10,000 words)
- AI-powered creative writing using Claude 3.5 Sonnet
- RAG-enabled context awareness
- Docker-based deployment

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/story-engine-mini.git
cd story-engine-mini
```

2. Copy the environment template:
```bash
cp .env.template .env
```

3. Update the .env file with your API keys and configuration

4. Build and run with Docker:
```bash
docker-compose -f docker/docker-compose.yml up --build
```

5. Access the API at http://localhost:8000

## Development

### Prerequisites
- Docker
- Python 3.11+
- Poetry (optional)

### Local Development
1. Install dependencies:
```bash
poetry install
```

2. Run the development server:
```bash
poetry run uvicorn src.main:app --reload
```

## Testing
```bash
poetry run pytest
```

## Documentation
API documentation is available at http://localhost:8000/docs when running the server.
