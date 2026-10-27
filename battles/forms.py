from django import forms
from .models import Answer, Topic


class TopicForm(forms.ModelForm):
  """お題投稿用フォーム"""

  class Meta:
    model = Topic
    fields = ["title"]
    widgets = {
        "title": forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "例：こんなプログラマーは嫌だ、どんなの？",
            }
        ),
    }


class AnswerForm(forms.ModelForm):
  """回答（ボケ）投稿用フォーム"""

  class Meta:
    model = Answer
    fields = ["body"]
    widgets = {
        "body": forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "ここにおもろい回答（ボケ）を入力...",
            }
        ),
    }