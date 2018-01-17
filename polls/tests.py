import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

class QuestionModelTests(TestCase):

    # test that confirm that Question.was_published_recently() returns correct values for past, recent, and future questions
    def test_was_published_recently_with_future_question(self):
        # was_published_recently() returns False for questions whose pub_date is in the future
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        # was_published_recently() returns False for questions whose pub_date is older than 1 day
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        # was_published_recently() returns True for questions whose pub_date is within the last day
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def create_question(question_text, days):
        # create question with given 'question_text' and published the given number of 'days' offset to now (negative for past, positive for future)
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text=question_text, pub_date=time)


# checking that at every state and for every new change in the state of the system, the expected results are published

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        # if no questions exist, an appropriate message is displayed
        repsonse = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")

self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        # questions with a pub_date in the past are displayed on the index page
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            reponse.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        # questions with a pub_date in the future aren't displayed on the index page
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index')) 
        self.assertContains(response, "No polls are available.")

self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        # Even if both past and future questions exist, only past questions are displayed.
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        # The questions index page may display multiple questions.
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

# check that a Question whose pub_date is in the past can be displayed, and that one with a pub_date in the future is not

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        # detail view of a question with a pub_date in the future returns a 404 not found.
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        # detail view of a question with a pub_date in the past displays the question's text.
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionResultsViewTests(TestCase):
    def test_future_question(self):
        # detail view of a question with a pub_date in the future returns a 404 not found.
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        # detail view of a question with a pub_date in the past displays the question's text.
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

# more tests: views check for and exclude Questions that have no Choices (test create Question without Choices and then test that it’s not published, and create similar Question with Choices, and test that it is published.)
# logged-in admin users should be allowed to see unpublished Questions, but not ordinary visitors