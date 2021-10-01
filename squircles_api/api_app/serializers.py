from .models import CourseTerms, Courses, Degrees, Specialisations, Subjects
from rest_framework import serializers

class CourseSerializer(serializers.ModelSerializer):
  class Meta:
    model = Courses
    fields = '__all__'

class CourseGraphSerializer(serializers.ModelSerializer):
  class Meta:
    model = Courses
    fields = ('code',
              'name',
              'equivalent_courses',
              'exclusion_courses',
              'unlocked_by',
              'unlocks',
              'other_requirements',
              )

class CourseTermSerializer(serializers.ModelSerializer):
  class Meta:
    model = CourseTerms
    fields = ('term',)

class SpecialisationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Specialisations
    fields = '__all__'

class DegreeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Degrees
    fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
  class Meta:
    model = Subjects
    fields = '__all__'
