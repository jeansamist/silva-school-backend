import random
import string


def random_string(length=8):
  letters = string.ascii_letters
  result_str = ''.join(random.choice(letters) for i in range(length))
  return result_str


def random_filename(ext):
  return random_string(100) + ext
