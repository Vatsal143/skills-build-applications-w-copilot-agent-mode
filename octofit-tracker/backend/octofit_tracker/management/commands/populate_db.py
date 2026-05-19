from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB directly for index creation
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()
        db.users.create_index([("email", 1)], unique=True)

        # Teams
        teams = [
            {"name": "Team Marvel"},
            {"name": "Team DC"}
        ]
        team_ids = db.teams.insert_many(teams).inserted_ids

        # Users
        users = [
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": "Team Marvel"},
            {"name": "Captain America", "email": "cap@marvel.com", "team": "Team Marvel"},
            {"name": "Batman", "email": "batman@dc.com", "team": "Team DC"},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "Team DC"}
        ]
        db.users.insert_many(users)

        # Activities
        activities = [
            {"user": "Iron Man", "activity": "Running", "duration": 30},
            {"user": "Captain America", "activity": "Cycling", "duration": 45},
            {"user": "Batman", "activity": "Swimming", "duration": 25},
            {"user": "Wonder Woman", "activity": "Yoga", "duration": 40}
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {"user": "Iron Man", "points": 100},
            {"user": "Captain America", "points": 90},
            {"user": "Batman", "points": 95},
            {"user": "Wonder Woman", "points": 98}
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {"user": "Iron Man", "workout": "Pushups", "reps": 50},
            {"user": "Captain America", "workout": "Situps", "reps": 60},
            {"user": "Batman", "workout": "Pullups", "reps": 40},
            {"user": "Wonder Woman", "workout": "Squats", "reps": 70}
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
