from django.shortcuts import render, get_object_or_404
from .models import Course, CourseQuest

def courses_list(request):
    courses = Course.objects.all()
    return render(request, 'courses_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course_quests = CourseQuest.objects.filter(course=course).select_related('quest').order_by('order')
    return render(request, 'course_detail.html', {
        'course': course,
        'course_quests': course_quests
    })