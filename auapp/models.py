from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instructor_courses')
    students = models.ManyToManyField(User, related_name='registered_courses', blank=True)

    def __str__(self):
        return self.title

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()

class Grade(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='grades')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades')
    marks = models.IntegerField(null=True, blank=True)
    graded_on = models.DateTimeField(null=True, blank=True)  # Add this field to track when the grade was given

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title} - {self.marks}"

class Announcement(models.Model):
    title = models.CharField(max_length=100, default="Untitled Announcement")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class DiscussionPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(DiscussionPost, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    photo = models.ImageField(upload_to="profile_photos", null=True, blank=True)
    bio = models.TextField(blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)  # New field
    major = models.CharField(max_length=100, null=True, blank=True)  # New field
    phone = models.CharField(max_length=15, null=True, blank=True)  # New field
    email = models.EmailField(null=True, blank=True)  # New field

    def __str__(self):
        return self.user.username
