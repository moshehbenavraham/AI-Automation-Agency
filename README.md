# AI Agency Management System

A FastAPI-based system for managing AI service projects and tracking their status and costs.

## Features

- Client authentication and authorization
- Project management with status tracking
- Multiple AI service integration (GPT, DALL-E)
- Usage analytics and cost tracking
- Secure database operations with Row Level Security

## Setup

1. Create a `.env` file with the following variables:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_jwt_secret_key
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Authentication
- POST `/auth/register` - Register a new client
- POST `/auth/token` - Login and get access token

### Projects
- POST `/projects` - Create a new project
- GET `/projects` - List all client projects
- GET `/projects/{project_id}` - Get specific project details

### Analytics
- GET `/analytics/usage` - Get usage statistics and costs

## Project Structure

```
app/
├── main.py           # FastAPI application setup
├── config.py         # Configuration and settings
├── database.py       # Database connection
├── dependencies.py   # Dependencies and middleware
├── models/          
│   ├── project.py    # Project models
│   └── user.py       # User models
├── routers/
│   ├── auth.py       # Authentication routes
│   ├── projects.py   # Project management routes
│   └── analytics.py  # Analytics routes
└── services/
    └── ai_service.py # AI service integration
```