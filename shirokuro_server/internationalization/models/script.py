from django.db import models

from internationalization.models.abstract.subtag import Subtag


class Script(Subtag):
    preferred_value_script = models.ForeignKey('self', on_delete=models.RESTRICT, null=True)
    comments = models.TextField(null=True)
