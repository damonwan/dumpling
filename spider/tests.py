import datetime
from django.utils import timezone
from django.test import TestCase
from .models import Question
from django.urls import reverse

class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        在将来发布的问卷应该返回False
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        日期超过1天的将返回False。这里创建了一个30天前发布的实例。
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)
    
    
    def test_was_published_recently_with_recent_question(self):
        """
        最近一天内的将返回True。这里创建了一个1小时内发布的实例。
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    """
    2个参数，一个是问卷的文本内容，另外一个是当前时间的偏移天数，负值表示发布日期在过去，正值表示发布日期在将来。
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
    
    
class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """
        如果问卷不存在，给出相应的提示。
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """
        发布日期在过去的问卷将在index页面显示。
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
        response.context['latest_question_list'],
        ['<Question: Past question.>']
        )
        
    def test_index_view_with_a_future_question(self):
        """
        发布日期在将来的问卷不会在index页面显示
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        """
        即使同时存在过去和将来的问卷，也只有过去的问卷会被显示。
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
        response.context['latest_question_list'],
        ['<Question: Past question.>']
        )

    def test_index_view_with_two_past_questions(self):
        """
        index页面可以同时显示多个问卷。
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
        response.context['latest_question_list'],
        ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )