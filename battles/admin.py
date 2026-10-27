from django.contrib import admin
from .models import Answer, Topic, Vote

admin.site.register(Topic)
admin.site.register(Answer)
admin.site.register(Vote)