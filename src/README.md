# Mergington High School Activities API

A simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities with email
- Cancel activity signups
- Real-time participant count and availability
- Modern web interface

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python src/app.py
   ```

3. Open your browser and visit:
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Alternative API Documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/activities` | Get all activities with participant counts |
| GET | `/activities/{activity_name}` | Get details for a specific activity |
| POST | `/activities/{activity_name}/signup?email=student@school.edu` | Sign up for an activity |
| DELETE | `/activities/{activity_name}/signup?email=student@school.edu` | Cancel activity signup |

## Data Model

The application uses a simple in-memory data model:

1. **Activities** - Identified by activity name:
   - Description
   - Schedule
   - Maximum participants allowed
   - List of participant emails
   - Current participant count
   - Spots remaining

2. **Students** - Identified by email address

All data is stored in memory and will be reset when the server restarts.

## Example Usage

### Sign up for Chess Club
```bash
curl -X POST "http://localhost:8000/activities/Chess%20Club/signup?email=student@school.edu"
```

### View all activities
```bash
curl http://localhost:8000/activities
```

### Cancel signup
```bash
curl -X DELETE "http://localhost:8000/activities/Chess%20Club/signup?email=student@school.edu"
```