# ORCAST Development Setup Guide

## Overview
This guide will help you set up the ORCAST project for local development while properly handling API keys and sensitive configuration.

## Prerequisites
- Node.js 18+ and npm
- Git
- Firebase CLI
- Google Cloud SDK (for BigQuery access)
- Python 3.8+ (for backend scripts)

## Initial Setup

### 1. Clone the Repository
```bash
git clone https://github.com/GilRaitses/orcast.git
cd orcast
```

### 2. Install Dependencies
```bash
npm install
pip install -r requirements.txt
```

### 3. Configure API Keys and Secrets

#### Environment Variables
1. Copy the environment template:
   ```bash
   cp env.template .env
   ```

2. Edit `.env` with your actual API keys:
   - **Google Maps API**: Get from [Google Cloud Console](https://console.cloud.google.com/)
   - **Firebase**: Get from [Firebase Console](https://console.firebase.google.com/)
   - **OpenWeather**: Get from [OpenWeatherMap](https://openweathermap.org/api)
   - **NOAA**: Get from [NOAA API](https://www.ncdc.noaa.gov/cdo-web/webservices/v2)

#### JavaScript Configuration
1. Copy the config template:
   ```bash
   cp config.js.template config.js
   ```

2. Fill in your API keys in `config.js`

### 4. Firebase Setup
```bash
firebase login
firebase use --add  # Select the orcast project
```

## Branch Strategy

### Main Branches
- `main`: Production-ready code
- `develop`: Integration branch for features

### Feature Branches
- `feature/frontend-ui`: UI components and styling
- `feature/map-visualization`: Google Maps integration
- `feature/backend-integration`: API and data processing
- `feature/api-development`: REST API endpoints
- `feature/documentation`: Documentation updates

### Working with Branches
```bash
# Start working on a feature
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name

# When ready to merge
git checkout develop
git pull origin develop
git merge feature/your-feature-name
```

## What You DON'T Need Access To

### Protected Resources
- Production Firebase project credentials
- Production Google Cloud project
- Cascadia Research Institute proprietary data
- Live DTAG biologging data
- Production API endpoints

### What's Available for Development
- Sample/mock data in `data/` folder
- Development Firebase project
- Test API endpoints
- Documentation and guides

## Security Best Practices

### Never Commit
- `.env` files
- `config.js` with real API keys
- Private keys (`.key`, `.pem` files)
- Any file in `secrets/`, `private/`, or `api_keys/` folders

### Always Use
- Template files for configuration
- Environment variables for sensitive data
- Mock data for development
- Development/staging environments

## Development Workflow

### 1. Frontend Development
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Test locally
npm run serve
```

### 2. Backend Development
```bash
# Run data processing scripts
cd scripts/data_processing
python realtime_data_collector.py

# Run ML services
cd scripts/ml_services
python behavioral_ml_service.py
```

### 3. Testing
```bash
# Run frontend tests
npm test

# Run backend tests
python -m pytest scripts/tests/
```

## API Access Levels

### Public APIs (No Authentication Required)
- Sample sighting data
- Basic probability grids
- Documentation endpoints

### Development APIs (Free Tier)
- Google Maps (with your key)
- OpenWeather (with your key)
- Firebase (development project)

### Restricted APIs (Project Admin Only)
- Production BigQuery datasets
- Live DTAG data streams
- Cascadia Research APIs

## Getting Help

1. Check the [Team Developer Guide](TEAM_DEVELOPER_GUIDE.md)
2. Review existing documentation in `docs/`
3. Ask in team communication channels
4. Create an issue for bugs or feature requests

## Troubleshooting

### Common Issues
- **Google Maps not loading**: Check API key and billing account
- **Firebase errors**: Ensure you're using the correct project
- **API rate limits**: Use development keys with higher limits
- **CORS errors**: Check API endpoint configurations

### Local Development URLs
- Frontend: `http://localhost:3000`
- API endpoints: `http://localhost:8080/api`
- Firebase emulator: `http://localhost:9099`

Remember: The goal is to enable productive development while keeping sensitive production data secure. 