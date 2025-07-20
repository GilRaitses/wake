# Gemini API Setup Guide for ORCAST

## Overview
This guide will help you integrate Google's Gemini API with the ORCAST agentic planning system for natural language processing and AI-powered trip planning.

## Prerequisites
- Google Cloud Project (you already have: `orca-466204`)
- Generative Language API enabled (✅ already done)
- Service account: `orca-237@orca-466204.iam.gserviceaccount.com` (✅ already exists)

## Step 1: Get Your API Key

### Option A: Create API Key (Recommended for Development)
1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Navigate to: **APIs & Services → Credentials**
3. Click **+ CREATE CREDENTIALS → API key**
4. Copy the API key (it will look like: `AIza...`)
5. **Optional but recommended:** Restrict the key:
   - Click on the key to edit
   - Under "API restrictions" → select "Restrict key"
   - Choose "Generative Language API"

### Option B: Use Service Account (For Production)
1. Download the service account JSON file for `orca-237@orca-466204.iam.gserviceaccount.com`
2. Store it securely (never commit to git)
3. Use Google Auth libraries for authentication

## Step 2: Configure ORCAST

### Update Environment Variables
```bash
# Copy the template
cp env.template .env

# Edit .env file and add your API key:
GEMINI_API_KEY=your_actual_api_key_here
GOOGLE_CLOUD_PROJECT_ID=orca-466204
GEMINI_MODEL=gemini-pro
```

### Update Configuration File
```bash
# Copy the template
cp config.js.template config.js

# Edit config.js and add your API key:
gemini: {
  apiKey: 'your_actual_api_key_here',
  projectId: 'orca-466204',
  model: 'gemini-pro'
}
```

## Step 3: Test the Integration

### Basic Connection Test
```javascript
// In browser console or your application:
const gemini = new GeminiIntegration({
  apiKey: 'your_api_key_here'
});

// Test connection
const isConnected = await gemini.testConnection();
console.log('Gemini connected:', isConnected);
```

### Test Constraint Extraction
```javascript
const userInput = "I want to plan a 3-day trip to see orcas from land this weekend";
const constraints = await gemini.extractConstraints(userInput);
console.log('Extracted constraints:', constraints);
```

### Test Trip Planning
```javascript
// Start voice planning
agenticPlanner.startVoicePlanning();
// Say: "Plan a 3-day orca watching trip from land with balcony accommodation"
```

## Step 4: Verify Integration

### Expected API Responses
When working correctly, you should see:

```json
{
  "timeframe": "weekend",
  "duration": 3,
  "preferredTime": "morning",
  "viewingType": "land",
  "accommodation": "balcony",
  "region": null,
  "groupSize": null,
  "interests": null,
  "confidence": 0.85
}
```

### Error Handling
The system includes fallback mechanisms:
- If Gemini API fails → falls back to rule-based extraction
- If API key is missing → uses local processing
- If rate limits hit → queues requests

## Step 5: Usage in ORCAST

### Voice Input Flow
1. User clicks "🎤 Start Voice Planning"
2. Speech-to-text captures: *"Plan a weekend trip to see orcas from land"*
3. Gemini extracts constraints: `{timeframe: "weekend", viewingType: "land"}`
4. ORCAST generates optimized plan with probability scores
5. User gets complete itinerary with export options

### API Usage Patterns
```javascript
// Extract constraints from natural language
const constraints = await gemini.extractConstraints(transcript);

// Generate AI-powered trip plan
const aiPlan = await gemini.generatePlan(constraints, locations);

// Optimize existing plan
const optimizations = await gemini.optimizePlan(currentPlan, constraints);
```

## Troubleshooting

### Common Issues

#### API Key Not Working
```
Error: Gemini API error: 403 API key not valid
```
**Solution:** Check that:
- API key is correct
- Generative Language API is enabled
- API key restrictions allow your domain

#### Rate Limiting
```
Error: Gemini API error: 429 Quota exceeded
```
**Solution:** 
- Implement request queuing (already included)
- Check quotas in Google Cloud Console
- Consider upgrading to paid tier

#### CORS Issues
```
Error: Access to fetch blocked by CORS policy
```
**Solution:** 
- API calls work from browser directly
- For production, proxy through your backend
- Or use Cloud Functions for server-side calls

### Debugging Tips

#### Enable Debug Logging
```javascript
// Add to config.js
debug: true

// Check browser console for detailed logs
```

#### Test API Directly
```bash
curl -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{"text": "Say hello"}]
    }]
  }'
```

## Cost Management

### Pricing (as of 2024)
- Gemini Pro: $0.50 per 1M input tokens, $1.50 per 1M output tokens
- Free tier: 60 requests per minute

### Optimization Tips
1. **Cache results** for common queries
2. **Shorter prompts** reduce token usage
3. **Batch requests** when possible
4. **Use temperature=0.3** for more deterministic results

## Security Best Practices

### API Key Security
- ✅ Never commit API keys to git
- ✅ Use environment variables
- ✅ Restrict API key to specific APIs
- ✅ Rotate keys regularly

### Production Considerations
- Use service account instead of API key
- Implement request rate limiting
- Add request logging and monitoring
- Use Cloud Functions for sensitive operations

## Next Steps

Once Gemini is working:
1. **Test voice planning** with various inputs
2. **Validate constraint extraction** accuracy
3. **Optimize prompts** for better results
4. **Add conversation memory** for follow-up questions
5. **Implement real-time plan updates** based on conditions

## Support

### Documentation
- [Gemini API Docs](https://ai.google.dev/docs)
- [ORCAST Technical Docs](../TEAM_DEVELOPER_GUIDE.md)

### Testing Commands
```bash
# Test complete integration
npm run test:agentic

# Test voice interface only  
npm run test:voice

# Test Gemini API only
npm run test:gemini
```

Your Gemini integration is ready! 🎯 Start testing voice-powered trip planning! 

## Overview
This guide will help you integrate Google's Gemini API with the ORCAST agentic planning system for natural language processing and AI-powered trip planning.

## Prerequisites
- Google Cloud Project (you already have: `orca-466204`)
- Generative Language API enabled (✅ already done)
- Service account: `orca-237@orca-466204.iam.gserviceaccount.com` (✅ already exists)

## Step 1: Get Your API Key

### Option A: Create API Key (Recommended for Development)
1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Navigate to: **APIs & Services → Credentials**
3. Click **+ CREATE CREDENTIALS → API key**
4. Copy the API key (it will look like: `AIza...`)
5. **Optional but recommended:** Restrict the key:
   - Click on the key to edit
   - Under "API restrictions" → select "Restrict key"
   - Choose "Generative Language API"

### Option B: Use Service Account (For Production)
1. Download the service account JSON file for `orca-237@orca-466204.iam.gserviceaccount.com`
2. Store it securely (never commit to git)
3. Use Google Auth libraries for authentication

## Step 2: Configure ORCAST

### Update Environment Variables
```bash
# Copy the template
cp env.template .env

# Edit .env file and add your API key:
GEMINI_API_KEY=your_actual_api_key_here
GOOGLE_CLOUD_PROJECT_ID=orca-466204
GEMINI_MODEL=gemini-pro
```

### Update Configuration File
```bash
# Copy the template
cp config.js.template config.js

# Edit config.js and add your API key:
gemini: {
  apiKey: 'your_actual_api_key_here',
  projectId: 'orca-466204',
  model: 'gemini-pro'
}
```

## Step 3: Test the Integration

### Basic Connection Test
```javascript
// In browser console or your application:
const gemini = new GeminiIntegration({
  apiKey: 'your_api_key_here'
});

// Test connection
const isConnected = await gemini.testConnection();
console.log('Gemini connected:', isConnected);
```

### Test Constraint Extraction
```javascript
const userInput = "I want to plan a 3-day trip to see orcas from land this weekend";
const constraints = await gemini.extractConstraints(userInput);
console.log('Extracted constraints:', constraints);
```

### Test Trip Planning
```javascript
// Start voice planning
agenticPlanner.startVoicePlanning();
// Say: "Plan a 3-day orca watching trip from land with balcony accommodation"
```

## Step 4: Verify Integration

### Expected API Responses
When working correctly, you should see:

```json
{
  "timeframe": "weekend",
  "duration": 3,
  "preferredTime": "morning",
  "viewingType": "land",
  "accommodation": "balcony",
  "region": null,
  "groupSize": null,
  "interests": null,
  "confidence": 0.85
}
```

### Error Handling
The system includes fallback mechanisms:
- If Gemini API fails → falls back to rule-based extraction
- If API key is missing → uses local processing
- If rate limits hit → queues requests

## Step 5: Usage in ORCAST

### Voice Input Flow
1. User clicks "🎤 Start Voice Planning"
2. Speech-to-text captures: *"Plan a weekend trip to see orcas from land"*
3. Gemini extracts constraints: `{timeframe: "weekend", viewingType: "land"}`
4. ORCAST generates optimized plan with probability scores
5. User gets complete itinerary with export options

### API Usage Patterns
```javascript
// Extract constraints from natural language
const constraints = await gemini.extractConstraints(transcript);

// Generate AI-powered trip plan
const aiPlan = await gemini.generatePlan(constraints, locations);

// Optimize existing plan
const optimizations = await gemini.optimizePlan(currentPlan, constraints);
```

## Troubleshooting

### Common Issues

#### API Key Not Working
```
Error: Gemini API error: 403 API key not valid
```
**Solution:** Check that:
- API key is correct
- Generative Language API is enabled
- API key restrictions allow your domain

#### Rate Limiting
```
Error: Gemini API error: 429 Quota exceeded
```
**Solution:** 
- Implement request queuing (already included)
- Check quotas in Google Cloud Console
- Consider upgrading to paid tier

#### CORS Issues
```
Error: Access to fetch blocked by CORS policy
```
**Solution:** 
- API calls work from browser directly
- For production, proxy through your backend
- Or use Cloud Functions for server-side calls

### Debugging Tips

#### Enable Debug Logging
```javascript
// Add to config.js
debug: true

// Check browser console for detailed logs
```

#### Test API Directly
```bash
curl -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{"text": "Say hello"}]
    }]
  }'
```

## Cost Management

### Pricing (as of 2024)
- Gemini Pro: $0.50 per 1M input tokens, $1.50 per 1M output tokens
- Free tier: 60 requests per minute

### Optimization Tips
1. **Cache results** for common queries
2. **Shorter prompts** reduce token usage
3. **Batch requests** when possible
4. **Use temperature=0.3** for more deterministic results

## Security Best Practices

### API Key Security
- ✅ Never commit API keys to git
- ✅ Use environment variables
- ✅ Restrict API key to specific APIs
- ✅ Rotate keys regularly

### Production Considerations
- Use service account instead of API key
- Implement request rate limiting
- Add request logging and monitoring
- Use Cloud Functions for sensitive operations

## Next Steps

Once Gemini is working:
1. **Test voice planning** with various inputs
2. **Validate constraint extraction** accuracy
3. **Optimize prompts** for better results
4. **Add conversation memory** for follow-up questions
5. **Implement real-time plan updates** based on conditions

## Support

### Documentation
- [Gemini API Docs](https://ai.google.dev/docs)
- [ORCAST Technical Docs](../TEAM_DEVELOPER_GUIDE.md)

### Testing Commands
```bash
# Test complete integration
npm run test:agentic

# Test voice interface only  
npm run test:voice

# Test Gemini API only
npm run test:gemini
```

Your Gemini integration is ready! 🎯 Start testing voice-powered trip planning! 
 