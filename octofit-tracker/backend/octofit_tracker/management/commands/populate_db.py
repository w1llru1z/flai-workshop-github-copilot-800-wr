from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing existing data...')
        
        # Delete existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        self.stdout.write('Creating teams...')
        
        # Create teams
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Earth\'s Mightiest Heroes'
        )
        
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League United'
        )
        
        self.stdout.write('Creating users...')
        
        # Create Marvel users
        marvel_heroes = [
            {'name': 'Iron Man', 'first_name': 'Tony', 'last_name': 'Stark', 'username': 'ironman', 'email': 'tony.stark@avengers.com', 'bio': 'Genius, billionaire, playboy, philanthropist'},
            {'name': 'Captain America', 'first_name': 'Steve', 'last_name': 'Rogers', 'username': 'captainamerica', 'email': 'steve.rogers@avengers.com', 'bio': 'First Avenger and Super Soldier'},
            {'name': 'Thor', 'first_name': 'Thor', 'last_name': 'Odinson', 'username': 'thor', 'email': 'thor.odinson@avengers.com', 'bio': 'God of Thunder from Asgard'},
            {'name': 'Hulk', 'first_name': 'Bruce', 'last_name': 'Banner', 'username': 'hulk', 'email': 'bruce.banner@avengers.com', 'bio': 'The strongest Avenger'},
            {'name': 'Black Widow', 'first_name': 'Natasha', 'last_name': 'Romanoff', 'username': 'blackwidow', 'email': 'natasha.romanoff@avengers.com', 'bio': 'Master spy and assassin'},
            {'name': 'Spider-Man', 'first_name': 'Peter', 'last_name': 'Parker', 'username': 'spiderman', 'email': 'peter.parker@avengers.com', 'bio': 'Your friendly neighborhood Spider-Man'},
        ]
        
        # Create DC users
        dc_heroes = [
            {'name': 'Superman', 'first_name': 'Clark', 'last_name': 'Kent', 'username': 'superman', 'email': 'clark.kent@justiceleague.com', 'bio': 'Man of Steel from Krypton'},
            {'name': 'Batman', 'first_name': 'Bruce', 'last_name': 'Wayne', 'username': 'batman', 'email': 'bruce.wayne@justiceleague.com', 'bio': 'Dark Knight of Gotham'},
            {'name': 'Wonder Woman', 'first_name': 'Diana', 'last_name': 'Prince', 'username': 'wonderwoman', 'email': 'diana.prince@justiceleague.com', 'bio': 'Amazonian Warrior Princess'},
            {'name': 'Flash', 'first_name': 'Barry', 'last_name': 'Allen', 'username': 'flash', 'email': 'barry.allen@justiceleague.com', 'bio': 'Fastest man alive'},
            {'name': 'Aquaman', 'first_name': 'Arthur', 'last_name': 'Curry', 'username': 'aquaman', 'email': 'arthur.curry@justiceleague.com', 'bio': 'King of Atlantis'},
            {'name': 'Green Lantern', 'first_name': 'Hal', 'last_name': 'Jordan', 'username': 'greenlantern', 'email': 'hal.jordan@justiceleague.com', 'bio': 'Guardian of Sector 2814'},
        ]
        
        marvel_users = []
        for hero in marvel_heroes:
            user = User.objects.create(
                username=hero['username'],
                first_name=hero['first_name'],
                last_name=hero['last_name'],
                name=hero['name'],
                email=hero['email'],
                bio=hero['bio'],
                team='Team Marvel'
            )
            marvel_users.append(user)
        
        dc_users = []
        for hero in dc_heroes:
            user = User.objects.create(
                username=hero['username'],
                first_name=hero['first_name'],
                last_name=hero['last_name'],
                name=hero['name'],
                email=hero['email'],
                bio=hero['bio'],
                team='Team DC'
            )
            dc_users.append(user)
        
        all_users = marvel_users + dc_users
        
        self.stdout.write('Creating activities...')
        
        # Create activities for each user
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weight Training', 'Yoga', 'Boxing']
        
        for user in all_users:
            # Create 5-10 activities per user
            num_activities = random.randint(5, 10)
            for i in range(num_activities):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)  # 20-120 minutes
                distance = round(random.uniform(1.0, 20.0), 2)  # 1-20 km
                calories = duration * random.randint(5, 15)  # Calories based on duration
                days_ago = random.randint(0, 30)
                
                Activity.objects.create(
                    user_id=str(user._id),
                    activity_type=activity_type,
                    duration=duration,
                    distance=distance,
                    calories=calories,
                    date=datetime.now() - timedelta(days=days_ago)
                )
        
        self.stdout.write('Creating leaderboard entries...')
        
        # Create leaderboard entries
        for rank, user in enumerate(all_users, start=1):
            user_activities = Activity.objects.filter(user_id=str(user._id))
            total_calories = sum(activity.calories for activity in user_activities)
            total_activities = user_activities.count()
            
            Leaderboard.objects.create(
                user_id=str(user._id),
                user_name=user.name,
                team=user.team,
                total_calories=total_calories,
                total_activities=total_activities,
                rank=rank
            )
        
        # Update ranks based on total calories
        leaderboard_entries = Leaderboard.objects.all().order_by('-total_calories')
        for rank, entry in enumerate(leaderboard_entries, start=1):
            entry.rank = rank
            entry.save()
        
        self.stdout.write('Creating workout suggestions...')
        
        # Create workout suggestions for users
        workout_templates = [
            {
                'name': 'Super Strength Training',
                'description': 'Build incredible strength like a superhero',
                'difficulty': 'Hard',
                'exercises': [
                    {'name': 'Bench Press', 'sets': 4, 'reps': 8},
                    {'name': 'Deadlifts', 'sets': 4, 'reps': 6},
                    {'name': 'Squats', 'sets': 4, 'reps': 10}
                ]
            },
            {
                'name': 'Agility and Speed',
                'description': 'Enhance speed and agility',
                'difficulty': 'Medium',
                'exercises': [
                    {'name': 'Sprint Intervals', 'sets': 5, 'reps': 1},
                    {'name': 'Box Jumps', 'sets': 3, 'reps': 15},
                    {'name': 'Ladder Drills', 'sets': 3, 'reps': 1}
                ]
            },
            {
                'name': 'Endurance Builder',
                'description': 'Build stamina for long battles',
                'difficulty': 'Medium',
                'exercises': [
                    {'name': 'Long Distance Run', 'sets': 1, 'reps': 1},
                    {'name': 'Burpees', 'sets': 3, 'reps': 20},
                    {'name': 'Mountain Climbers', 'sets': 3, 'reps': 30}
                ]
            },
            {
                'name': 'Combat Training',
                'description': 'Martial arts and fighting techniques',
                'difficulty': 'Hard',
                'exercises': [
                    {'name': 'Heavy Bag Work', 'sets': 5, 'reps': 3},
                    {'name': 'Shadow Boxing', 'sets': 4, 'reps': 3},
                    {'name': 'Kick Training', 'sets': 3, 'reps': 20}
                ]
            },
        ]
        
        for user in all_users:
            # Give each user 2-3 workout suggestions
            num_workouts = random.randint(2, 3)
            selected_workouts = random.sample(workout_templates, num_workouts)
            
            for workout in selected_workouts:
                Workout.objects.create(
                    user_id=str(user._id),
                    workout_name=workout['name'],
                    description=workout['description'],
                    exercises=workout['exercises'],
                    difficulty=workout['difficulty']
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated the database!'))
        self.stdout.write(f'Created {Team.objects.count()} teams')
        self.stdout.write(f'Created {User.objects.count()} users')
        self.stdout.write(f'Created {Activity.objects.count()} activities')
        self.stdout.write(f'Created {Leaderboard.objects.count()} leaderboard entries')
        self.stdout.write(f'Created {Workout.objects.count()} workout suggestions')
