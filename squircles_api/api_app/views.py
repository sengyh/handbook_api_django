import json
from django.db.models.query_utils import subclasses
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import CourseTerms, Courses, Degrees, Specialisations, Subjects
from rest_framework.decorators import api_view
from rest_framework import status
import logging
from .serializers import CourseSerializer, CourseGraphSerializer, DegreeSerializer, SpecialisationSerializer, SubjectSerializer
logging.basicConfig(level=logging.INFO)
import re
from .input_checkers import course_code_check, level_check, spec_code_check, deg_code_check, subject_check


# Create your views here.

@api_view(['GET'])
def get_all_courses(request):
  try: 
    courses = Courses.objects.all().values('code', 'name')
  except Courses.DoesNotExist: 
    return JsonResponse({'error': 'There are no courses to be found'}, status=status.HTTP_404_NOT_FOUND) 

  if request.method == 'GET':
    all_courses = {}
    for course in courses:
      all_courses[course['code']] = course['name']
    return JsonResponse(all_courses, json_dumps_params={'indent': 2}) 


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
def get_all_specialisations(request):
  try: 
    specs = Specialisations.objects.all().values('code', 'name')
  except Specialisations.DoesNotExist: 
    return JsonResponse({'message': 'This specialisation does not exist'}, status=status.HTTP_404_NOT_FOUND) 
  
  if request.method == 'GET':
    all_specialisations = {}
    for spec in specs:
      all_specialisations[spec['code']] = spec['name'] 
    return JsonResponse(all_specialisations, json_dumps_params={'indent': 2})

@api_view(['GET'])
def get_specialisation(request, spec_id):
  if not spec_code_check(spec_id):
    return JsonResponse({'error': 'Invalid code. Specialisation code must match the pattern [A-Z]{5}[12H]'}, status=status.HTTP_400_BAD_REQUEST) 

  try: 
    spec_id = spec_id.upper()
    spec = Specialisations.objects.get(pk=spec_id) 
  except Specialisations.DoesNotExist: 
    return JsonResponse({'message': 'This specialisation does not exist'}, status=status.HTTP_404_NOT_FOUND) 
  
  if request.method == 'GET':
    spec_serialized = SpecialisationSerializer(spec)
    return JsonResponse(spec_serialized.data, json_dumps_params={'indent': 2})


@api_view(['GET'])
def get_all_degrees(request):
  try: 
    degrees = Degrees.objects.all().values('code', 'name')
  except Degrees.DoesNotExist: 
    return JsonResponse({'message': 'This degree does not exist'}, status=status.HTTP_404_NOT_FOUND) 

  if request.method == 'GET': 
    all_degrees = {}
    for degree in degrees:
      all_degrees[degree['code']] = degree['name']
    return JsonResponse(all_degrees, json_dumps_params={'indent': 2}) 


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


@api_view(['GET'])
def get_all_subjects(request):
  if request.method == 'GET':
    subjects = Subjects.objects.all()
    all_subs = {}
    for sub in subjects:
      all_subs[sub.code] = sub.name
    return JsonResponse(all_subs, json_dumps_params={'indent': 2})


@api_view(['GET'])
def get_all_subject_courses(request, sub_code):
  if not subject_check(sub_code):
    return JsonResponse({'error': 'Invalid code. Subject code must match the pattern [A-Z]{4}'}, status=status.HTTP_400_BAD_REQUEST)

  try: 
    sub_code = sub_code.upper()
    subject = Subjects.objects.get(pk=sub_code)
  except Subjects.DoesNotExist:
     return JsonResponse({'message': 'This subject does not exist'}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    sub_courses = SubjectSerializer(subject).data 
    sub_code = sub_courses['code']
    courses_qobj = Courses.objects.filter(subject=sub_code).values('code')
    all_sub_courses = []
    for course_q in courses_qobj:
      all_sub_courses.append(course_q['code'])
    sub_courses['courses'] = sorted(all_sub_courses)
    return JsonResponse(sub_courses, json_dumps_params={'indent': 2})
  

@api_view(['GET'])
def get_all_subject_courses_level(request, sub_code, level):
  if not subject_check(sub_code) or not level_check(level):
    return JsonResponse({'error': 'Invalid code. Subject code must match the pattern [A-Z]{4} and level must be between 1-9'}, status=status.HTTP_400_BAD_REQUEST)

  try: 
    sub_code = sub_code.upper()
    subject = Subjects.objects.get(pk=sub_code)
  except Subjects.DoesNotExist:
     return JsonResponse({'message': 'This subject does not exist'}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    sub_courses = SubjectSerializer(subject).data 
    sub_code = sub_courses['code']
    courses_qobj = Courses.objects.filter(subject=sub_code, level=level).values('code')
    all_sub_courses = []
    for course_q in courses_qobj:
      all_sub_courses.append(course_q['code'])
    sub_courses['courses'] = sorted(all_sub_courses)
    return JsonResponse(sub_courses, json_dumps_params={'indent': 2})
  

