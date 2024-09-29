from django.contrib import admin
from .models import Category, Course

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the category name
    search_fields = ('name',)  # Allow searching by category name

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'creation_date', 'video_url')  # Display title, price, creation date, and video URL
    list_filter = ('price', 'creation_date')  # Filter by price and creation date
    search_fields = ('title', 'description')  # Search by title and description

# class CourseReviewAdmin(admin.ModelAdmin):
#     list_display = ('course', 'user', 'rating', 'comment')  # Display course, user, rating, and comment
#     list_filter = ('rating', 'course')  # Filter by rating and course
#     search_fields = ('course__title', 'user__username', 'comment')  # Search by course title, user, and comment

# Register the models with their respective admin classes
admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
# admin.site.register(CourseReview, CourseReviewAdmin)
