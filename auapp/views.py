from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.admin.views.decorators import staff_member_required

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Assignment, Grade, Announcement, DiscussionPost, Comment, UserProfile
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import CourseForm, AssignmentForm
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Avg
from django.http import HttpResponse
from .models import Assignment, Grade, User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.timezone import now

def uhome(request):
	if request.user.is_authenticated:
		return redirect("dashboard")
	else:
		if request.method == "POST":
			un = request.POST.get("un")
			pw = request.POST.get("pw")
			usr = authenticate(username=un,password=pw)
			if usr is None:
				return render(request,"uhome.html",{"msg":"invalid username/password"})
			else:
				login(request,usr)
				return redirect("dashboard")
		else:
			return render(request,"uhome.html")
def usignup(request):
	if request.user.is_authenticated:
		return redirect("uwelcome")
	else:
		if request.method == "POST":
			un = request.POST.get("un")
			pw1 = request.POST.get("pw1")
			pw2 = request.POST.get("pw2")
			if pw1==pw2:
				try:
					usr = User.objects.get(username=un)
					return render(request,"usignup.html",{"msg":"user already registered"})
				except User.DoesNotExist:
					usr = User.objects.create_user(username=un,password=pw1)
					usr.save()
					return redirect("uhome")
			else:
				return render(request,"usignup.html",{"msg":"passwords did not match"})
		else:
			return render(request,"usignup.html")

def uwelcome(request):
	if request.user.is_authenticated:
		return redirect("dashboard")
	else:
		return redirect("uhome")

def ulogout(request):
	logout(request)
	return redirect("uhome")

def ucp(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			pw1 = request.POST.get("pw1")
			pw2 = request.POST.get("pw2")
			if pw1==pw2:
				try:
					usr = User.objects.get(username=request.user.username)
					usr.set_password(pw1)
					usr.save()
					return redirect("uhome")
				except User.DoesNotExist:
					return render(request,"ucp.html",{"msg":"User Does Not Exist"})
			else:
				return render(request,"ucp.html",{"msg":"passwords did not match"})
		else:
			return render(request,"ucp.html")
	else:
		return redirect("uhome")


@login_required
def dashboard(request):
    courses = Course.objects.filter(students=request.user)
    return render(request, 'dashboard.html', {'courses': courses})

# Ensure only prof can access this view
def is_prof(user):
    return user.username == 'prof'

@user_passes_test(is_prof)
def add_course(request):
    if request.method == "POST":
        course_form = CourseForm(request.POST)
        assignment_form_1 = AssignmentForm(request.POST, prefix='assignment1')
        assignment_form_2 = AssignmentForm(request.POST, prefix='assignment2')
        assignment_form_3 = AssignmentForm(request.POST, prefix='assignment3')

        if course_form.is_valid() and assignment_form_1.is_valid() and assignment_form_2.is_valid() and assignment_form_3.is_valid():
            course = course_form.save()

            # Save assignments
            assignment1 = assignment_form_1.save(commit=False)
            assignment1.course = course
            assignment1.save()

            assignment2 = assignment_form_2.save(commit=False)
            assignment2.course = course
            assignment2.save()

            assignment3 = assignment_form_3.save(commit=False)
            assignment3.course = course
            assignment3.save()

            return redirect('courses')
    else:
        course_form = CourseForm()
        assignment_form_1 = AssignmentForm(prefix='assignment1')
        assignment_form_2 = AssignmentForm(prefix='assignment2')
        assignment_form_3 = AssignmentForm(prefix='assignment3')

    return render(request, 'add_course.html', {
        'course_form': course_form,
        'assignment_form_1': assignment_form_1,
        'assignment_form_2': assignment_form_2,
        'assignment_form_3': assignment_form_3,
    })

@login_required
def courses(request):
    courses = Course.objects.all()  # Get all courses
    my_courses = request.user.registered_courses.all()  # Get courses registered by the user

    # For prof user, show all courses, and for students, show only registered courses
    return render(request, 'courses.html', {'courses': courses, 'my_courses': my_courses})

@login_required
def register_course(request, course_id):
    # Get the course object based on the provided course_id
    course = get_object_or_404(Course, id=course_id)

    # Check if the user is already registered for the course
    if request.user in course.students.all():
        # If the user is already registered, return a message or just redirect them
        return redirect('courses')  # or you can render a message like 'Already registered'

    # If the user is not registered, add the user to the course's students list
    course.students.add(request.user)

    # Redirect to the courses page after successful registration
    return redirect('courses')  # Adjust this if you want to redirect elsewhere

@login_required
def unregister_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.students.remove(request.user)
    return redirect('courses')  

@login_required
def courses(request):
    # Fetch all available courses
    all_courses = Course.objects.all()
    
    # Fetch the courses the current user is registered for
    my_courses = Course.objects.filter(students=request.user)

    return render(request, 'courses.html', {'courses': all_courses, 'my_courses': my_courses})


@login_required
def assignments(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    assignments = Assignment.objects.filter(course=course)
    return render(request, 'assignments.html', {'assignments': assignments, 'course': course})

@login_required
def assign_grade(request, assignment_id, student_id):
    if request.user.username != 'prof':
        return HttpResponseRedirect(reverse('dashboard'))

    if request.method == 'POST':
        marks = request.POST.get('grade')
        if marks and 1 <= int(marks) <= 10:
            assignment = get_object_or_404(Assignment, id=assignment_id)
            student = get_object_or_404(User, id=student_id)
            Grade.objects.update_or_create(
                assignment=assignment, student=student, defaults={'marks': marks}
            )
            return HttpResponseRedirect(reverse('grades'))
    return HttpResponseRedirect(reverse('grades'))

@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    assignment.submitted = True
    assignment.save()
    return redirect('assignments', course_id=assignment.course.id)

@login_required
def grades(request):
    if request.user.username == 'prof':
        # Ensure this block is only for professors
        students = User.objects.filter(
            registered_courses__instructor=request.user
        ).exclude(username='prof').distinct()

        student_assignments = {}
        for student in students:
            registered_courses = student.registered_courses.filter(instructor=request.user)
            assignments = Assignment.objects.filter(course__in=registered_courses)
            student_assignments[student] = assignments

        return render(request, 'grades.html', {
            'is_prof': True,
            'students': students,
            'student_assignments': student_assignments,
        })

    elif request.user.is_authenticated:
        # Ensure this block is for students
        registered_courses = request.user.registered_courses.all()
        assignments = Assignment.objects.filter(course__in=registered_courses)
        grades = Grade.objects.filter(student=request.user)

        if grades.exists():
            total_marks = sum(grade.marks for grade in grades if grade.marks is not None)
            overall_grade = total_marks / grades.count()
        else:
            overall_grade = None

        return render(request, 'grades.html', {
            'is_prof': False,
            'assignments': assignments,
            'grades': grades,
            'overall_grade': overall_grade,
        })

    else:
        # Redirect unauthenticated users to the login page
        return redirect('login')

@login_required
def announcements(request):
    if request.user.username == 'prof':
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            if title and description:
                Announcement.objects.create(title=title, description=description)
                return redirect('announcements')

        all_announcements = Announcement.objects.all()
        return render(request, 'announcements.html', {
            'is_prof': True,
            'announcements': all_announcements
        })

    # Student account: Only view announcements
    all_announcements = Announcement.objects.all()
    return render(request, 'announcements.html', {
        'is_prof': False,
        'announcements': all_announcements
    })

@login_required
def discussion(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        DiscussionPost.objects.create(title=title, content=content, author=request.user)
        return redirect('discussion')
    posts = DiscussionPost.objects.all()
    return render(request, 'discussion.html', {'posts': posts})

@login_required
def post_comments(request, post_id):
    post = get_object_or_404(DiscussionPost, id=post_id)
    if request.method == "POST":
        content = request.POST.get("content")
        Comment.objects.create(content=content, author=request.user, post=post)
        return redirect('discussion')
    comments = Comment.objects.filter(post=post)
    return render(request, 'comments.html', {'post': post, 'comments': comments})

@login_required
def profile(request):
    # Get or create the user's profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # Get updated fields from the request
        bio = request.POST.get("bio", "")
        photo = request.FILES.get("photo")
        age = request.POST.get("age")
        major = request.POST.get("major")
        phone = request.POST.get("phone")
        email = request.POST.get("email")

        # Update the profile fields
        user_profile.bio = bio
        if photo:
            user_profile.photo = photo
        user_profile.age = age if age else None
        user_profile.major = major
        user_profile.phone = phone
        user_profile.email = email

        # Save the updated profile
        user_profile.save()

        # Redirect to the profile page after saving
        return redirect("profile")

    # If it's a GET request, render the profile page
    return render(request, "profile.html", {"profile": user_profile})


@login_required
def user_settings(request):  # Rename from 'settings' to 'user_settings'
    if request.method == "POST":
        new_name = request.POST.get("name")
        request.user.username = new_name
        request.user.save()
        return redirect('user_settings')  # Update the redirect name as well
    return render(request, 'settings.html')