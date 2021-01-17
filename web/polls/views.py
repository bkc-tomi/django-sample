from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic


# モデルのインポート
from .models import Choice, Question

"""
---------------------------------------------------------------------
質問一覧
---------------------------------------------------------------------
"""
class IndexView(generic.ListView):
    template_name       = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]
"""
---------------------------------------------------------------------
質問詳細
---------------------------------------------------------------------
"""
class DetailView(generic.DetailView):
    model         = Question
    template_name = 'polls/detail.html'

"""
---------------------------------------------------------------------
投票結果
---------------------------------------------------------------------
"""
class ResultsView(generic.DetailView):
    model         = Question
    template_name = 'polls/result.html'

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