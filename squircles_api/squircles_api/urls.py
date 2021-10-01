"""squircles_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from api_app import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/<str:course_code>', views.get_course_full),
    path('courses/<str:course_code>/node', views.get_course_node),
    path('specialisations/<str:spec_id>', views.get_specialisation),
    path('degrees/<str:deg_id>', views.get_degree),
    path('subjects/', views.get_all_subjects),
    path('subjects/<str:sub_code>', views.get_all_subject_courses),
    path('subjects/<str:sub_code>/level/<str:level>', views.get_all_subject_courses_level)
]
