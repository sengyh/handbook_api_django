import re

def course_code_check(code):
  course_match = re.match(r'[a-zA-Z]{4}\d{4}', code)
  if course_match:
    return True
  return False

def spec_code_check(code):
  spec_match = re.match(r'[a-zA-Z]{5}[hH12]', code)
  if spec_match:
    return True
  return False

def deg_code_check(code):
  spec_match = re.match(r'\d{4}', code)
  if spec_match:
    return True
  return False