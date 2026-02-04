from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'name', 'email', 'bio', 'team', 'date_joined', 'created_at']

    def get_id(self, obj):
        return str(obj._id) if obj._id else None


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_at', 'member_count']

    def get_id(self, obj):
        return str(obj._id) if obj._id else None

    def get_member_count(self, obj):
        return User.objects.filter(team=obj.name).count()


class ActivitySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ['id', 'user_id', 'activity_type', 'duration', 'distance', 'calories', 'date', 'created_at']

    def get_id(self, obj):
        return str(obj._id) if obj._id else None


class LeaderboardSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Leaderboard
        fields = ['id', 'user_id', 'user_name', 'team', 'total_calories', 'total_activities', 'rank', 'updated_at']

    def get_id(self, obj):
        return str(obj._id) if obj._id else None


class WorkoutSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Workout
        fields = ['id', 'user_id', 'workout_name', 'description', 'exercises', 'difficulty', 'created_at']

    def get_id(self, obj):
        return str(obj._id) if obj._id else None
