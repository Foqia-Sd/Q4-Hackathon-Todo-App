# Quickstart Guide: AI-Powered Natural Language Todo Control

## Overview
This guide will help you get the AI-powered chat feature up and running in the todo application. The feature allows users to manage tasks using natural language while preserving all existing functionality.

## Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL database (existing setup from previous phases)
- OpenAI API key
- Existing backend and frontend from Phases 1-2

## Environment Setup

### Backend Configuration
1. Add the following to your `.env` file:
```
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo  # or gpt-3.5-turbo for lower cost
```

2. Install new dependencies (if not already present):
```bash
pip install openai
```

### Database Setup
1. Run the database migration to create the chat message table:
```bash
# From the backend directory
python -m alembic revision --autogenerate -m "add chat_message table"
python -m alembic upgrade head
```

## Running the Application

### Backend
1. Navigate to the backend directory:
```bash
cd backend
```

2. Start the backend server:
```bash
python -m uvicorn src.main:app --reload --port 8000
```

The chat API will be available at `http://localhost:8000/api/v1/chat`

### Frontend
1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

## Key Features

### Natural Language Processing
- Users can interact with their todo list using natural language
- Supported commands: "Add a task to buy groceries", "Show me my tasks", "Mark groceries as done", "Delete the meeting task"

### Chat Interface
- Accessible through a new Chat button in the navbar
- Includes sidebar navigation with all app options
- Maintains conversation context across messages
- Responsive design works on desktop and mobile

### Backend Skills
- AI agent calls backend services to perform actual task operations
- No hardcoded AI logic in routes (as required by constitution)
- Preserves all existing functionality

## API Testing

### Test the Chat Endpoint
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Authorization: Bearer YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries"
  }'
```

Expected response:
```json
{
  "response": "I've added the task 'buy groceries' to your list.",
  "intent": "add_task",
  "taskId": "task_12345",
  "sessionId": "sess_abc123xyz"
}
```

## Frontend Testing

1. Log into the application
2. Click the "Chat" button in the navbar
3. Try natural language commands like:
   - "Add a new task to call mom"
   - "Show me what I need to do"
   - "Mark 'call mom' as completed"
   - "Delete the meeting task"

## Troubleshooting

### Common Issues

#### AI Processing Errors
- Verify your OpenAI API key is correct in the environment
- Check that the OpenAI service is accessible
- Look for rate limiting errors in the logs

#### Authentication Issues
- Ensure your authentication token is valid
- Verify that the BetterAuth integration is working properly

#### Database Connection Issues
- Check that PostgreSQL is running
- Verify database connection settings in your environment

### Logging
- Backend logs will show chat interactions and AI processing details
- Frontend console will show API calls and UI interactions
- Database logs can help troubleshoot chat history operations

## Next Steps

1. Customize the AI prompts for better domain-specific understanding
2. Add more sophisticated intent recognition
3. Implement conversation memory for longer context retention
4. Enhance the UI with typing indicators and message history