from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'team', 'created_at')
    search_fields = ('name', 'email', 'team')
    list_filter = ('team', 'created_at')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'activity_type', 'duration', 'distance', 'calories', 'date')
    search_fields = ('user_id', 'activity_type')
    list_filter = ('activity_type', 'date', 'created_at')


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('rank', 'user_name', 'team', 'total_calories', 'total_activities', 'updated_at')
    search_fields = ('user_name', 'team')
    list_filter = ('team', 'updated_at')
    ordering = ('rank',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('workout_name', 'user_id', 'difficulty', 'created_at')
    search_fields = ('workout_name', 'user_id', 'description')
    list_filter = ('difficulty', 'created_at')
