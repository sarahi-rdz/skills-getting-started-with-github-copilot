"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}

# Additional activities
activities.update({
    "Soccer Team": {
        "description": "Competitive soccer practices and matches",
        "schedule": "Mondays, Wednesdays, Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Lap swimming, technique coaching, and local meets",
        "schedule": "Tuesdays and Thursdays, 5:00 PM - 6:30 PM",
        "max_participants": 18,
        "participants": ["ava@mergington.edu"]
    },
    "Art Club": {
        "description": "Drawing, painting, and mixed-media workshops",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["isabella@mergington.edu"]
    },
    "Drama Class": {
        "description": "Acting exercises, scene study, and school productions",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 30,
        "participants": ["noah@mergington.edu"]
    },
    "Debate Team": {
        "description": "Competitive debate practice and tournaments",
        "schedule": "Mondays and Thursdays, 5:00 PM - 6:30 PM",
        "max_participants": 16,
        "participants": ["sophia@mergington.edu"]
    },
    "Math Club": {
        "description": "Problem solving, math contests, and study groups",
        "schedule": "Fridays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["ethan@mergington.edu"]
    }
})

# More activities (sports, artistic, intellectual)
activities.update({
    "Tennis Club": {
        "description": "Beginner to advanced tennis practice and intramural matches",
        "schedule": "Mondays and Thursdays, 4:30 PM - 6:00 PM",
        "max_participants": 16,
        "participants": ["maria@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball practices, conditioning, and games",
        "schedule": "Tuesdays, Thursdays, Fridays, 5:00 PM - 7:00 PM",
        "max_participants": 20,
        "participants": ["jack@mergington.edu"]
    },
    "Photography Club": {
        "description": "Learn photography techniques, editing, and host exhibitions",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["lucy@mergington.edu"]
    },
    "Ceramics Studio": {
        "description": "Wheel throwing, handbuilding, and glazing workshops",
        "schedule": "Saturdays, 10:00 AM - 12:30 PM",
        "max_participants": 12,
        "participants": ["oliver@mergington.edu"]
    },
    "Science Club": {
        "description": "Hands-on experiments, STEM projects, and science fair prep",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["mia@mergington.edu"]
    },
    "Robotics Team": {
        "description": "Build and program robots for regional competitions",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 6:30 PM",
        "max_participants": 18,
        "participants": ["noah@mergington.edu"]
    },
    "Volleyball Team": {
        "description": "Practice serves, teamwork, and competitive volleyball matches",
        "schedule": "Mondays and Wednesdays, 3:45 PM - 5:15 PM",
        "max_participants": 18,
        "participants": ["elena@mergington.edu"]
    },
    "Track Club": {
        "description": "Speed drills, endurance training, and track meets",
        "schedule": "Tuesdays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 24,
        "participants": ["henry@mergington.edu"]
    },
    "Choir": {
        "description": "Vocal training, ensemble practice, and school performances",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 30,
        "participants": ["sara@mergington.edu"]
    },
    "Creative Writing Club": {
        "description": "Work on poetry, short stories, and peer feedback workshops",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["noelle@mergington.edu"]
    },
    "Book Club": {
        "description": "Read novels, discuss themes, and share recommendations",
        "schedule": "Mondays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["amelia@mergington.edu"]
    },
    "Philosophy Club": {
        "description": "Explore big questions through discussion and critical thinking",
        "schedule": "Fridays, 4:00 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["lucas@mergington.edu"]
    }
})


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Validate student is not already signed up
    if email in activities[activity_name]["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up for this activity")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def remove_participant(activity_name: str, email: str):
    """Remove a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found in this activity")

    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
