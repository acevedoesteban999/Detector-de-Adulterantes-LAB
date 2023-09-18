import sys
def is_at_migrations():
    return ('makemigrations' in sys.argv or 'migrate' in sys.argv)
          