# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db.models.fields import TextField


class Faculties(models.Model):
    code = models.TextField(primary_key=True)
    name = models.TextField(unique=True)
    overview = models.TextField()

    class Meta:
        managed = False
        db_table = 'faculties'


class Schools(models.Model):
    name = models.TextField(primary_key=True)
    faculty = models.ForeignKey(Faculties, models.DO_NOTHING, db_column='faculty')

    class Meta:
        managed = False
        db_table = 'schools'


class Subjects(models.Model):
    code = models.TextField(primary_key=True)
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'subjects'


class SchoolsToSubjects(models.Model):
    school = models.OneToOneField(Schools, models.DO_NOTHING, db_column='school', primary_key=True)
    subject = models.ForeignKey('Subjects', models.DO_NOTHING, db_column='subject')

    class Meta:
        managed = False
        db_table = 'schools_to_subjects'
        unique_together = (('school', 'subject'),)


class Courses(models.Model):
    code = models.TextField(primary_key=True)
    name = models.TextField()
    overview = models.TextField()
    subject = models.ForeignKey('Subjects', models.DO_NOTHING, db_column='subject')
    level = models.IntegerField()
    school = models.ForeignKey('Schools', models.DO_NOTHING, db_column='school')
    credits = models.IntegerField()
    equivalent_courses = ArrayField(models.TextField())
    exclusion_courses = ArrayField(models.TextField())
    unlocked_by = ArrayField(models.TextField())
    unlocks = ArrayField(models.TextField())
    other_requirements = models.JSONField()
    is_gen_ed = models.BooleanField()
    is_intro = models.BooleanField()
    is_multi_term = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'courses'

class CourseTerms(models.Model):
    course = models.OneToOneField('Courses', models.DO_NOTHING, db_column='course', primary_key=True)
    term = models.TextField()

    class Meta:
        managed = False
        db_table = 'course_terms'
        unique_together = (('course', 'term'),)


class Specialisations(models.Model):
    code = models.TextField(primary_key=True)
    name = models.TextField()
    overview = models.TextField()
    type = models.TextField()
    credits = models.IntegerField()
    course_structure = ArrayField(models.JSONField())
    more_information = ArrayField(models.JSONField())
    school = models.ForeignKey(Schools, models.DO_NOTHING, db_column='school')

    class Meta:
        managed = False
        db_table = 'specialisations'


class Degrees(models.Model):
    code = models.TextField(primary_key=True)
    name = models.TextField()
    credits = models.IntegerField()
    overview = models.TextField()
    duration = models.IntegerField()
    structure_overview = models.TextField()
    core_structure_uoc = models.IntegerField()
    core_structure_desc = models.TextField()
    core_specialisations = ArrayField(models.JSONField())
    optional_specialisations = ArrayField(models.JSONField())
    core_course_components = ArrayField(models.JSONField())
    misc_course_components = ArrayField(models.JSONField())
    more_information = ArrayField(models.JSONField())
    faculty = models.ForeignKey('Faculties', models.DO_NOTHING, db_column='faculty')
    intake_period = ArrayField(models.TextField())
    academic_calendar = models.TextField()
    award = models.TextField()
    award_type = models.TextField()

    class Meta:
        managed = False
        db_table = 'degrees'

