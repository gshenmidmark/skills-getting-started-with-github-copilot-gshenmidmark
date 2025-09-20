"""
High School Activities API

A simple FastAPI application for managing extracurricular activities
at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import uvicorn
from pathlib import Path

app = FastAPI(
    title="Mergington High School Activities API",
    description="API for managing extracurricular activities",
    version="1.0.0"
)

# Mount static files
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# In-memory database for activities
activities = {
    "Chess Club": {
        "description": "Learn chess strategies and compete in tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM", 
        "max_participants": 15,
        "participants": ["alice@school.edu", "bob@school.edu"]
    },
    "Drama Club": {
        "description": "Participate in theater productions and acting workshops",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": ["charlie@school.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 12,
        "participants": ["diana@school.edu", "eve@school.edu", "frank@school.edu"]
    }
}

@app.get("/")
def read_root():
    """Redirect to the main page"""
    return RedirectResponse(url="/static/index.html")

@app.get("/activities")
def get_activities():
    """Get all available activities with participant counts"""
    result = {}
    for name, activity in activities.items():
        result[name] = {
            **activity,
            "current_participants": len(activity["participants"]),
            "spots_remaining": activity["max_participants"] - len(activity["participants"])
        }
    return result

@app.get("/activities/{activity_name}")
def get_activity(activity_name: str):
    """Get details for a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    activity = activities[activity_name]
    return {
        **activity,
        "current_participants": len(activity["participants"]),
        "spots_remaining": activity["max_participants"] - len(activity["participants"])
    }

@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    activity = activities[activity_name]
    
    # Check if already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Already signed up for this activity")
    
    # Check if activity is full
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")
    
    # Add participant
    activity["participants"].append(email)
    
    return {
        "message": f"Successfully signed up {email} for {activity_name}",
        "participants_count": len(activity["participants"]),
        "spots_remaining": activity["max_participants"] - len(activity["participants"])
    }

@app.delete("/activities/{activity_name}/signup")
def cancel_signup(activity_name: str, email: str):
    """Cancel signup for an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    activity = activities[activity_name]
    
    if email not in activity["participants"]:
        raise HTTPException(status_code=400, detail="Not signed up for this activity")
    
    activity["participants"].remove(email)
    
    return {
        "message": f"Successfully cancelled signup for {email} from {activity_name}",
        "participants_count": len(activity["participants"]),
        "spots_remaining": activity["max_participants"] - len(activity["participants"])
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)