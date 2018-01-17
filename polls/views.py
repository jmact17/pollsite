from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

# using generic views: ListView (display list of objects) and DetailView (display detail page for particular type of object)

class IndexView(generic.ListView):
    # use specific template instead of default
    template_name = 'polls/index.html'
    # override automatically generate context var
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # return last 5 published questions, not including future
        # returns queryset with Questions whose pub_date is Less Than or Equal to timezone.now
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

"""def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    ### old/long way using loader
    # template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    ### render() shortcut: request object, template name, dictionary (opt)
    return render(request, 'polls/index.html', context)
    # return HttpResponse(template.render(context, request))"""

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        # excludes any questions that aren't yet published
        return Question.objects.filter(pub_date__lte=timezone.now())

"""def detail(request, question_id):
    #try:
        #question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        #raise Http404("Question does not exist")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})"""

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    def get_queryset(self):
        # excludes any questions that aren't yet published
        return Question.objects.filter(pub_date__lte=timezone.now())

"""def results(request, question_id):
   question = get_object_or_404(Question, pk=question_id)
   return render(request, 'polls/results.html', {'question': question})"""

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    # when key (dictionary) is not found
    except (KeyError, Choice.DoesNotExist):
        # redisplay question voting form if choice isn't given
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # always return an HttpResponseRedirect after successfuly dealing with POST data: prevents data from being posted twice if a user hits the Back button
        # name of the view to pass control to, variable portion of URL pattern that points to that view
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

