import sys
PredictionChoices=[
    ('1','100%'),
    ('7','75%'),
    ('5','50%'),
    ('2','25%'),
    ('0','0%'),
    ('N','Ninguna'),
    ('C','CSV'),
    ('M','Multi'),
]
def is_at_migrations():
    return ('makemigrations' in sys.argv or 'migrate' in sys.argv)
          