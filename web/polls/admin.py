from django.contrib import admin

from .models import Question
from .models import Choice

# 管理者ページで管理するモデル
admin.site.register(Question)
admin.site.register(Choice)