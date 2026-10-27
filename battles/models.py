from django.contrib.auth.models import User
from django.db import models


class Topic(models.Model):
  """お題モデル"""

  title = models.CharField(max_length=200, verbose_name="お題")
  creator = models.ForeignKey(
      User, on_delete=models.CASCADE, verbose_name="投稿者"
  )
  created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")

  def __str__(self):
    return self.title


class Answer(models.Model):
  """回答（ボケ）モデル"""

  topic = models.ForeignKey(
      Topic,
      on_delete=models.CASCADE,
      related_name="answers",
      verbose_name="お題",
  )
  author = models.ForeignKey(
      User, on_delete=models.CASCADE, verbose_name="回答者"
  )
  body = models.TextField(verbose_name="回答（ボケ）")
  created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")

  def __str__(self):
    return f"{self.body[:20]}... (by {self.author.username})"


class Vote(models.Model):
  """投票（「おもろい！」）モデル"""

  answer = models.ForeignKey(
      Answer, on_delete=models.CASCADE, related_name="votes", verbose_name="回答"
  )
  user = models.ForeignKey(
      User, on_delete=models.CASCADE, verbose_name="投票者"
  )
  created_at = models.DateTimeField(auto_now_add=True, verbose_name="投票日時")

  class Meta:
    # 同一ユーザーが同じ回答に複数回投票できないようにする制約
    constraints = [
        models.UniqueConstraint(
            fields=["answer", "user"], name="unique_vote_per_user"
        )
    ]

  def __str__(self):
    return f"{self.user.username} voted for Answer #{self.answer.id}"