from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice


def index(request):
    questions = Question.objects.all()
    return render(request, 'polls/index.html', {'questions': questions})


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return redirect('results', question_id=question.id)


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    total_votes = sum(choice.votes for choice in question.choice_set.all())

    choices_with_percent = []
    for choice in question.choice_set.all():
        if total_votes == 0:
            percent = 0
        else:
            percent = int((choice.votes / total_votes) * 100)

        choices_with_percent.append({
            'choice': choice,
            'percent': percent
        })

    context = {
        'question': question,
        'choices_with_percent': choices_with_percent,
        'total_votes': total_votes,
    }
    return render(request, 'polls/results.html', context)