# SLAG: Starfall - Lost Age of Giants

An AI-powered graphic novel experience that combines storytelling and image generation to create an immersive sci-fi fantasy world.

## Overview

SLAG (Starfall: Lost Age of Giants) is an innovative web application that leverages AI technology to generate both narrative content and visual artwork. The project explores themes of future civilizations, unknown alien technology, and the remnants of a world shaped by giant mechanical-sentient beings.

## Features

- **AI-Generated Narrative**: Fully autonomous story generation with consistent plot and character development
- **Context-Aware Generation**: RAG system ensures narrative coherence and adherence to established lore
- **Real-time Generation Logs**: Live monitoring of the AI story generation process
- **Vector-Based Memory**: Pinecone integration for maintaining story context and world-building elements
- **Multi-Model Architecture**: Combines Claude and Titan embeddings for optimal performance
- **Responsive Design**: Fully optimized for both desktop and mobile viewing

## Setting

- **Time Period**: 4424 CE
- **Starting Location**: Station Omega, a research facility dedicated to Fragment

## Tokenomics

- **Project Name**: Starfall - Lost Age of Giants
- **Token Symbol**: $SLAG
- **Total Supply**: 1,000,000,000
- **Token Distribution**: The token will be fairly launched on pump.fun. The token generation even will be announced in advance on the official website (https://lostage.io) and on the official X account (https://x.com/slag_ai).

## Tech Stack

### Frontend
- **Framework**: Next.js 15.1.1, React 19
- **Styling**: Tailwind CSS
- **Animations**: React Spring
- **Typography**: IBM Plex Mono
- **Deployment**: Vercel

### Backend
- **AI Models**: AWS Bedrock (Claude, Titan)
- **Vector Store**: Pinecone
- **Testing**: Pytest
- **Monitoring**: AWS CloudWatch
- **Language**: Python 3.11

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SLAG.git
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Configure environment variables:
```bash
# Backend (.env)
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENVIRONMENT=your_environment

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

5. Run the development servers:
```bash
# Backend
python -m uvicorn main:app --reload

# Frontend
npm run dev
```

## Project Structure

```
├── backend/
│   ├── src/
│   │   ├── services/          # Core services (RAG, Story Engine, etc.)
│   │   ├── reference-documents/ # World-building and context documents
│   │   └── tests/            # Test suites
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/             # Next.js app router pages
│   │   ├── components/      # React components
│   │   └── styles/         # Global styles
│   └── package.json
└── README.md
```

## Contributing

This project is currently in development. Feel free to submit issues and enhancement requests.

## License

This project is private and proprietary. All rights reserved.

## Disclaimer

The $SLAG token mentioned in this project has no inherent value and is meant for entertainment purposes only. Purchasing $SLAG is done at your own risk, under your own discretion, and is not intended to be a financial investment. NFA. DYOR.
