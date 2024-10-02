from django.contrib import admin
from .models import Lesson, Module,UserCourseProgress

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'duration', 'video_url', 'pdf_file')  # Display more fields for Lesson
    list_filter = ('module', 'duration')  # Filter by module and duration
    search_fields = ('title', 'description')  # Search by title and description

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')  # Display more fields for Module
    list_filter = ('course',)  # Add filters for course and completion status
    search_fields = ('title', 'description')  # Search by title and description

class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'total_completed_lessons')  # Display user, course, and a count of completed lessons
    list_filter = ('course', 'user')  # Add filters for course and user
    search_fields = ('user__email', 'course__title')  # Allow searching by user and course title
    filter_horizontal = ('completed_lessons',)  # Use a multi-select widget for completed lessons
    
    def total_completed_lessons(self, obj):
        return obj.completed_lessons.count()  # Custom method to display the total number of completed lessons
    total_completed_lessons.short_description = 'Completed Lessons'  # Display name in admin interface

admin.site.register(UserCourseProgress, CourseProgressAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Module, ModuleAdmin)
