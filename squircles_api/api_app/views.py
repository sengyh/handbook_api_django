from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import CourseTerms, Courses, Degrees, Specialisations
from rest_framework.decorators import api_view
from rest_framework import status
import logging
from .serializers import CourseSerializer, CourseGraphSerializer, DegreeSerializer, SpecialisationSerializer
logging.basicConfig(level=logging.INFO)
import re
from .input_checkers import course_code_check, spec_code_check, deg_code_check


# Create your views here.

@api_view(['GET'])
def get_course_full(request, course_code):
  if not course_code_check(course_code):
    return JsonResponse({'error': 'Invalid code. Course codes must match the pattern [A-Z]{4}[0-9]{4}'}, status=status.HTTP_400_BAD_REQUEST) 
  
  try: 
    course_code = course_code.upper()
    course = Courses.objects.get(pk=course_code)
    course_terms = CourseTerms.objects.filter(course=course_code)
  except Courses.DoesNotExist: 
    return JsonResponse({'error': 'This course does not exist'}, status=status.HTTP_404_NOT_FOUND) 

  if request.method == 'GET':
    course_serialized = CourseSerializer(course)
    terms = []
    for term in list(course_terms):
      terms.append(term.term)
    full_course_info = course_serialized.data
    full_course_info['terms'] = terms
    return JsonResponse(full_course_info, json_dumps_params={'indent': 2}) 

@api_view(['GET'])
def get_course_node(request, course_code):
  if not course_code_check(course_code):
    return JsonResponse({'error': 'Invalid code. Course codes must match the pattern [A-Z]{4}[0-9]{4}'}, status=status.HTTP_400_BAD_REQUEST) 

  try: 
    course_code = course_code.upper()
    course = Courses.objects.get(pk=course_code)
  except Courses.DoesNotExist: 
    return JsonResponse({'error': 'This course does not exist'}, status=status.HTTP_404_NOT_FOUND) 
  if request.method == 'GET':
    course_serialized = CourseGraphSerializer(course)
    full_course_info = course_serialized.data
    return JsonResponse(full_course_info, json_dumps_params={'indent': 2}) 


@api_view(['GET'])
def get_specialisation(request, spec_id):
  if not spec_code_check(spec_id):
    return JsonResponse({'error': 'Invalid code. Specialisation code must match the pattern [A-Z]{5}[12H]{4}'}, status=status.HTTP_400_BAD_REQUEST) 

  try: 
    spec_id = spec_id.upper()
    spec = Specialisations.objects.get(pk=spec_id) 
  except Specialisations.DoesNotExist: 
    return JsonResponse({'message': 'This specialisation does not exist'}, status=status.HTTP_404_NOT_FOUND) 
  
  if request.method == 'GET':
    spec_serialized = SpecialisationSerializer(spec)
    return JsonResponse(spec_serialized.data, json_dumps_params={'indent': 2})

@api_view(['GET'])
def get_degree(request, deg_id):
  if not deg_code_check(deg_id):
    return JsonResponse({'error': 'Invalid code. Degree code must match the pattern [0-9]{4}'}, status=status.HTTP_400_BAD_REQUEST) 
    
  try: 
    degree = Degrees.objects.get(pk=deg_id) 
  except Degrees.DoesNotExist: 
    return JsonResponse({'message': 'This degree does not exist'}, status=status.HTTP_404_NOT_FOUND) 

  if request.method == 'GET': 
    degree_serialized = DegreeSerializer(degree)
    return JsonResponse(degree_serialized.data, json_dumps_params={'indent': 2}) 