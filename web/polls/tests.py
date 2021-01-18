import datetime

from django.test  import TestCase
from django.utils import timezone
from django.urls  import reverse

from .models import Question, Choice

"""
-------------------------------------------------------------------------------------
直近公開関数のテスト
-------------------------------------------------------------------------------------
"""
class QuestionModelTest(TestCase):
    """
    ---------------------------------------------------------------------
    * テスト対象 *
    models => Question => was_published_recently()
    - 過去１日の間に公開された質問かどうかで真偽値を返す。

    * テスト値 *
    現在から３０日後を公開日に設定した質問

    * 期待値 *
    False
    ---------------------------------------------------------------------
    """
    def test_was_published_recently_with_future_question(self):
        time            = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date = time)

        self.assertIs(future_question.was_published_recently(), False)

    """
    ---------------------------------------------------------------------
    * テスト対象 *
    models => Question => was_published_recently()
    - 過去１日の間に公開された質問かどうかで真偽値を返す。

    * テスト値 *
    現在から１日と１秒前の公開日に設定した質問

    * 期待値 *
    False
    ---------------------------------------------------------------------
    """
    def test_was_published_recently_with_old_question(self):
        time         = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)

        self.assertIs(old_question.was_published_recently(), False)

    """
    ---------------------------------------------------------------------
    * テスト対象 *
    models => Question => was_published_recently()
    - 過去１日の間に公開された質問かどうかで真偽値を返す。

    * テスト値 *
    現在から23:59:59前の公開日に設定した質問

    * 期待値 *
    True
    ---------------------------------------------------------------------
    """
    def test_was_published_recently_with_recent_question(self):
        time            = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)



"""
-------------------------------------------------------------------------------------
テスト用の質問を作成する関数
-------------------------------------------------------------------------------------
"""
def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


"""
-------------------------------------------------------------------------------------
polls/indexビューのテスト
-------------------------------------------------------------------------------------
"""
class QuestionIndexViewTests(TestCase):
    """
    ---------------------------------------------------------------------
    * テスト対象 *
    views => IndexView
    - 現在までに公開されている質問のうち新しいもの５つを表示する。

    * テスト内容 *
    表示する質問がない場合をテスト

    * テストと期待値 *
    status_code         : 200
    response            : "No polls are available."
    latest_question_list: []
    ---------------------------------------------------------------------
    """
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    """
    ---------------------------------------------------------------------
    * テスト対象 *
    views => IndexView
    - 現在までに公開されている質問のうち新しいもの５つを表示する。

    * テスト内容 *
    該当する質問が一つだけの場合をテスト

    * テストと期待値 *
    latest_question_list: ['<Question: Past question.>']
    ---------------------------------------------------------------------
    """
    def test_past_question(self):
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    """
    ---------------------------------------------------------------------
    * テスト対象 *
    views => IndexView
    - 現在までに公開されている質問のうち新しいもの５つを表示する。

    * テスト内容 *
    公開日がきてない質問しかない場合をテスト

    * テストと期待値 *
    latest_question_list: []
    ---------------------------------------------------------------------
    """
    def test_future_question(self):
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    """
    ---------------------------------------------------------------------
    * テスト対象 *
    views => IndexView
    - 現在までに公開されている質問のうち新しいもの５つを表示する。

    * テスト内容 *
    公開日がきてない質問ときている質問の場合をテスト

    * テストと期待値 *
    latest_question_list: ['<Question: Past question.>']
    ---------------------------------------------------------------------
    """
    def test_future_question_and_past_question(self):
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    """
    ---------------------------------------------------------------------
    * テスト対象 *
    views => IndexView
    - 現在までに公開されている質問のうち新しいもの５つを表示する。

    * テスト内容 *
    公開日がきている質問の場合をテスト

    * テストと期待値 *
    latest_question_list: ['<Question: Past question 2.>', '<Question: Past question 1.>']
    ---------------------------------------------------------------------
    """
    def test_two_past_questions(self):
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


"""
-------------------------------------------------------------------------------------
polls/detailビューのテスト
-------------------------------------------------------------------------------------
"""
class QuestionDetailViewTests(TestCase):
    """
    ---------------------------------------------------------------------
    * テスト対象 *
    views => DetailView
    - 指定されたquestion_idの質問の詳細と投票フォームを表示

    * テスト内容 *
    公開日がきてない質問の場合をテスト

    * テストと期待値 *
    status_code: 404
    ---------------------------------------------------------------------
    """
    def test_future_question(self):
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    """
    ---------------------------------------------------------------------
    * テスト対象 *
    views => DetailView
    - 指定されたquestion_idの質問の詳細と投票フォームを表示

    * テスト内容 *
    公開日がきている質問の場合をテスト

    * テストと期待値 *
    response: past_question.question_text(作成した質問)
    ---------------------------------------------------------------------
    """
    def test_past_question(self):
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


"""
-------------------------------------------------------------------------------------
polls/resultビューのテスト
-------------------------------------------------------------------------------------
"""
class QuestionResultViewTests(TestCase):
    """
    ---------------------------------------------------------------------
    * テスト対象 *
    views => ResultView
    - 指定されたquestion_idの質問に該当する選択肢と投票数を出力する。

    * テスト内容 *
    公開日がきてない質問の場合をテスト

    * テストと期待値 *
    status_code: 404
    ---------------------------------------------------------------------
    """
    def test_past_question(self):
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:result', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

"""
-------------------------------------------------------------------------------------
polls/voteビューのテスト
-------------------------------------------------------------------------------------
"""
class QuestionVoteTests(TestCase):
    """
    ---------------------------------------------------------------------
    * テスト対象 *
    views => vote
    - 指定されたquestion_idとPOSTクエリパラメータから投票数をカウントアップする。

    * テスト内容 *
    正しいパラメータが渡ってきた場合のテスト

    * テストと期待値 *
    status_code         : 301
    choice.votesがインクリメントされたかどうか。
    ---------------------------------------------------------------------
    """
    def test_votes(self):
        # 質問を作成
        future_question = create_question(question_text='Future question.', days=5)
        # 質問に該当する選択肢を作成 
        q = Question.objects.get(pk=future_question.id)
        c1 = q.choice_set.create(choice_text='choice01', votes=0)
        c2 = q.choice_set.create(choice_text='choice02', votes=0)
        # c1をPOST
        url = reverse('polls:vote', args=(future_question.id,))
        response = self.client.post(url, { "choice": c1.id, })
        # POST結果を取得
        c_result = Choice.objects.get(pk=c1.id)
        # テスト
        self.assertEqual(response.status_code, 302)
        self.assertIs(c_result.votes, 1)

    """
    ---------------------------------------------------------------------
    * テスト対象 *
    views => vote
    - 指定されたquestion_idとPOSTクエリパラメータから投票数をカウントアップする。

    * テスト内容 *
    question_idが指定されていない場合のテスト

    * テストと期待値 *
    status_code: 404
    ---------------------------------------------------------------------
    """
    def test_no_id_question(self):
        # 質問を作成
        future_question = create_question(question_text='Future question.', days=5)
        # 質問に該当する選択肢を作成 
        q = Question.objects.get(pk=future_question.id)
        c1 = q.choice_set.create(choice_text='choice01', votes=0)
        c2 = q.choice_set.create(choice_text='choice02', votes=0)

        # 存在しないIDを定義
        no_id = future_question.id + 1
        # POST
        url = reverse('polls:vote', args=(no_id,))
        response = self.client.post(url,{ "choice": c1.id })
        # テスト
        self.assertEqual(response.status_code, 404)

    """
    ---------------------------------------------------------------------
    * テスト対象 *
    views => vote
    - 指定されたquestion_idとPOSTクエリパラメータから投票数をカウントアップする。

    * テスト内容 *
    question_idが指定されているがPOSTクエリパラメータが指定されていない場合のテスト

    * テストと期待値 *
    status_code         : 301
    error_message       : "You didn't select a choice."
    ---------------------------------------------------------------------
    """
    def test_no_query_parameter(self):
        # 質問を作成
        future_question = create_question(question_text='Future question.', days=5)
        # 質問に該当する選択肢を作成 
        q = Question.objects.get(pk=future_question.id)
        c1 = q.choice_set.create(choice_text='choice01', votes=0)
        c2 = q.choice_set.create(choice_text='choice02', votes=0)
        # POST
        url = reverse('polls:vote', args=(future_question.id,))
        response = self.client.post(url,{})
        # テスト
        self.assertContains(response, "You didn&#x27;t select a choice.") # 文字列エスケープ注意
        self.assertEqual(response.status_code, 200)