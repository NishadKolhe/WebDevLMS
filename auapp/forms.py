from django import forms
from .models import DiscussionPost, Comment, UserProfile, Course, Assignment

# Form for creating/editing Discussion Posts
class DiscussionPostForm(forms.ModelForm):
    class Meta:
        model = DiscussionPost
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter post title'}),
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your post here'}),
        }

# Form for creating/editing Comments
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here'}),
        }

# Form for updating UserProfile (photo and bio)
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself'}),
        }

# Form for creating/editing Course
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'instructor']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Course Title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Course Description'}),
        }

# Form for creating/editing Assignment
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Assignment Title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Assignment Description'}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
