import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tutorial.settings")# project_name 项目名称
django.setup()


from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

snippet = Snippet(code='foo = "bar"\n')
snippet.save()

snippet = Snippet(code='print("hello, world")\n')
snippet.save()