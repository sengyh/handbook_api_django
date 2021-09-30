from .models import Courses, Degrees
from rest_framework import serializers

class CourseSerializer(serializers.ModelSerializer):
  class Meta:
    model = Courses
    fields = ('code',
              'name',
              'overview',
              'subject',
              'level',
              'school',
              'credits',
              'equivalent_courses',
              'exclusion_courses',
              'unlocked_by',
              'unlocks',
              'other_requirements',
              'is_gen_ed',
              'is_intro',
              'is_multi_term',
              )

class DegreeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Degrees
    fields = '__all__'