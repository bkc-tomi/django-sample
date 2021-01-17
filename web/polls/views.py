from django.http      import Http404
from django.shortcuts import render
from django.http      import HttpResponse, HttpResponseRedirect
from django.template  import loader
from django.urls      import reverse

# モデルのインポート
from .models import Choice, Question

"""
---------------------------------------------------------------------
質問一覧
---------------------------------------------------------------------
"""
def index(request):
    try:
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
    
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)


"""
---------------------------------------------------------------------
質問詳細
---------------------------------------------------------------------
"""
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)

    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    return render(request, 'polls/detail.html', {'question': question})

"""
---------------------------------------------------------------------
投票結果
---------------------------------------------------------------------
"""
def result(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    return render(request, 'polls/result.html', {'question': question})


"""
---------------------------------------------------------------------
投票
---------------------------------------------------------------------
"""
def vote(request, question_id):
    # 質問の取得
    try:
        question = Question.objects.get(pk=question_id)

    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    # POSTされた選択肢の取得
    try:
        choice_key = request.POST['choice']
        selected_choice = question.choice_set.get(pk=choice_key)

    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            'polls/detail.html',
            {
                'question': question,
                'error_message': "You didn't select a choice.",
            }
        )
    
    # 投票数の変更
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:result', args=(question_id, )))