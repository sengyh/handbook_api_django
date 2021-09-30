from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import json
from .models import Courses, Degrees
from rest_framework.decorators import api_view
from rest_framework import status
import logging
from .serializers import CourseSerializer, DegreeSerializer
logging.basicConfig(level=logging.INFO)


# Create your views here.

@api_view(['GET'])
def course_request(request, course_code):
  try: 
    course_code = course_code.upper()
    course = Courses.objects.get(pk=course_code) 
  except Courses.DoesNotExist: 
    return JsonResponse({'message': 'The course does not exist'}, status=status.HTTP_404_NOT_FOUND) 

  if request.method == 'GET': 
    course_serialized = CourseSerializer(course)
    return JsonResponse(course_serialized.data, json_dumps_params={'indent': 2}) 
 
@api_view(['GET'])
def degree_request(request, deg_id):
  try: 
    degree = Degrees.objects.get(pk=deg_id) 
  except Degrees.DoesNotExist: 
    return JsonResponse({'message': 'This degree does not exist'}, status=status.HTTP_404_NOT_FOUND) 

  if request.method == 'GET': 
    degree_serialized = DegreeSerializer(degree)
    return JsonResponse(degree_serialized.data, json_dumps_params={'indent': 2}) 