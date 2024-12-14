from django.urls import path
from auapp import views
from django.conf import settings
from django.conf.urls.static import static
from auapp.views import (
    uhome, usignup, uwelcome, ulogout, ucp, dashboard, courses,
    assignments, submit_assignment, grades, announcements, discussion,
    post_comments, profile, user_settings, register_course, unregister_course,
    add_course, assign_grade
)

urlpatterns = [
    path("", uhome, name="uhome"),
    path("usignup/", usignup, name="usignup"),
    path("uwelcome/", uwelcome, name="uwelcome"),
    path("ulogout/", ulogout, name="ulogout"),
    path("ucp/", ucp, name="ucp"),
    path("dashboard/", dashboard, name="dashboard"),
    path("courses/", courses, name="courses"),
    path("register_course/<int:course_id>/", register_course, name="register_course"),
    path("unregister_course/<int:course_id>/", unregister_course, name="unregister_course"),
    path("add_course/", add_course, name="add_course"),
    path("assignments/<int:course_id>/", assignments, name="assignments"),
    path("submit_assignment/<int:assignment_id>/", submit_assignment, name="submit_assignment"),
    path("grades/", grades, name="grades"),
    path("assign_grade/<int:assignment_id>/<int:student_id>/", assign_grade, name="assign_grade"),
    
    path("announcements/", views.announcements, name="announcements"),
    path("discussion/", discussion, name="discussion"),
    path("discussion/<int:post_id>/comments/", post_comments, name="post_comments"),
    path("profile/", profile, name="profile"),
    path("settings/", views.user_settings, name="user_settings"),  # Update name and path
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
