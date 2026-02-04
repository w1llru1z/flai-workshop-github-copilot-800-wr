from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime


class UserModelTestCase(TestCase):
    def test_create_user(self):
        user = User.objects.create(
            name='Test User',
            email='test@example.com',
            team='Team Alpha'
        )
        self.assertEqual(user.name, 'Test User')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.team, 'Team Alpha')


class TeamModelTestCase(TestCase):
    def test_create_team(self):
        team = Team.objects.create(
            name='Team Alpha',
            description='First team'
        )
        self.assertEqual(team.name, 'Team Alpha')
        self.assertEqual(team.description, 'First team')


class ActivityModelTestCase(TestCase):
    def test_create_activity(self):
        activity = Activity.objects.create(
            user_id='user123',
            activity_type='Running',
            duration=30,
            distance=5.0,
            calories=300,
            date=datetime.now()
        )
        self.assertEqual(activity.activity_type, 'Running')
        self.assertEqual(activity.duration, 30)
        self.assertEqual(activity.calories, 300)


class LeaderboardModelTestCase(TestCase):
    def test_create_leaderboard_entry(self):
        entry = Leaderboard.objects.create(
            user_id='user123',
            user_name='Test User',
            team='Team Alpha',
            total_calories=1000,
            total_activities=5,
            rank=1
        )
        self.assertEqual(entry.rank, 1)
        self.assertEqual(entry.total_calories, 1000)


class WorkoutModelTestCase(TestCase):
    def test_create_workout(self):
        workout = Workout.objects.create(
            user_id='user123',
            workout_name='Morning Routine',
            description='Daily morning workout',
            exercises={'push_ups': 20, 'squats': 30},
            difficulty='Medium'
        )
        self.assertEqual(workout.workout_name, 'Morning Routine')
        self.assertEqual(workout.difficulty, 'Medium')


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'name': 'API Test User',
            'email': 'apitest@example.com',
            'team': 'Team Beta'
        }

    def test_create_user_api(self):
        response = self.client.post('/api/users/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'API Test User')

    def test_get_users_api(self):
        User.objects.create(**self.user_data)
        response = self.client.get('/api/users/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TeamAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.team_data = {
            'name': 'API Test Team',
            'description': 'Team for API testing'
        }

    def test_create_team_api(self):
        response = self.client.post('/api/teams/', self.team_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)

    def test_get_teams_api(self):
        Team.objects.create(**self.team_data)
        response = self.client.get('/api/teams/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ActivityAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.activity_data = {
            'user_id': 'user123',
            'activity_type': 'Cycling',
            'duration': 45,
            'distance': 15.0,
            'calories': 450,
            'date': datetime.now().isoformat()
        }

    def test_create_activity_api(self):
        response = self.client.post('/api/activities/', self.activity_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)


class APIRootTestCase(APITestCase):
    def test_api_root(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)
