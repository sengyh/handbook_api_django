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
from django.urls import path, re_path, include
from rest_framework import permissions
from django.conf.urls import url
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
    openapi.Info(
        title="UNSW Handbook API - 2021",
        default_version='v1',
        description="A pretty complete version of the UNSW Handbook for Undergrads",
        contact=openapi.Contact(email="sengyh.dev@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    #path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('subjects/', views.get_all_subjects),
    path('subjects/<str:sub_code>', views.get_all_subject_courses),
    path('subjects/<str:sub_code>/level/<str:level>', views.get_all_subject_courses_level),
    path('courses/', views.get_all_courses),
    path('courses/<str:course_code>', views.get_course_full),
    path('courses/<str:course_code>/node', views.get_course_node),
    path('specialisations/', views.get_all_specialisations),
    path('specialisations/<str:spec_id>', views.get_specialisation),
    path('degrees/', views.get_all_degrees),
    path('degrees/<str:deg_id>', views.get_degree)
]
