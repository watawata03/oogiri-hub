from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import AnswerForm, TopicForm
from .models import Answer, Topic, Vote  
from django.db import IntegrityError  


def topic_list(request):
  """お題一覧表示"""
  topics = Topic.objects.all().order_by("-created_at")
  context = {"topics": topics}
  return render(request, "battles/topic_list.html", context)


@login_required  # ログインしているユーザーだけが投稿できるようにする
def topic_create(request):
  """お題投稿ビュー"""
  if request.method == "POST":
    form = TopicForm(request.POST)
    if form.is_valid():
      topic = form.save(commit=False)
      topic.creator = request.user  # ログイン中のユーザーを投稿者に設定
      topic.save()
      return redirect("battles:topic_list")  # 投稿後は一覧ページへリダイレクト
  else:
    form = TopicForm()

  context = {"form": form}
  return render(request, "battles/topic_form.html", context)


def topic_detail(request, pk):
  """お題詳細 ＆ 回答一覧・投稿ビュー"""
  topic = get_object_or_404(Topic, pk=pk)
  # このお題に対する回答を新しい順に取得
  answers = topic.answers.all().order_by("-created_at")

  if request.method == "POST":
    # ログインしていない場合はログイン画面へ
    if not request.user.is_authenticated:
      return redirect("admin:login")

    form = AnswerForm(request.POST)
    if form.is_valid():
      answer = form.save(commit=False)
      answer.topic = topic  # どのお題に対する回答か紐づける
      answer.author = request.user  # 投稿者を設定
      answer.save()
      return redirect("battles:topic_detail", pk=topic.pk)
  else:
    form = AnswerForm()

  context = {
      "topic": topic,
      "answers": answers,
      "form": form,
  }
  return render(request, "battles/topic_detail.html", context)


def vote_answer(request, answer_pk):
  """投票（おもろい！）処理ビュー"""
  answer = get_object_or_404(Answer, pk=answer_pk)

  try:
    # 投票を作成する（まだ投票していなければ成功する）
    Vote.objects.create(answer=answer, user=request.user)
  except IntegrityError:
    # すでに投票している場合は、モデルのユニーク制約に引っかかるため
    # 「投票済み」とみなして投票を削除する（取り消し機能）
    Vote.objects.filter(answer=answer, user=request.user).delete()

  # お馴染みのお題詳細ページへリダイレクト
  return redirect("battles:topic_detail", pk=answer.topic.pk)