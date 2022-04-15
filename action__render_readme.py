from app import *
from engine__documentation import *
from engine__markdown import *

githubflavoredmarkdown([(str(rule), rule.endpoint) for rule in app.url_map.iter_rules() if rule.endpoint != 'static'])