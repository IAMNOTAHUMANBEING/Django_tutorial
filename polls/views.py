from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
from django.shortcuts import render, get_object_or_404
from django.views import generic

# 제네릭 뷰
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    # 자동으로 ListView는 context 변수로 question_list를 제공, 템플릿에 사용한 것과 같게 수정

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])    # POST로 전달받은 값 중에 choice 항목의 value 반환
    except (KeyError, Choice.DoesNotExist):                                     # ex. request_POST = { 'choice' : 1}
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()  # 계산하고 저장도 따로 해줘야 함
        # POST를 성공적으로 전달 받고 나면 리다이렉트를 항상 해주어야 함
        # 사용자가 뒤로 가기 버튼을 눌러서 data가 두번 POST 되는 일을 막아줌
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return render(request, 'polls/index.html', context) # view 내용을 html에 렌더링 하는 방법
#
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)  # 조건에 맞는 객체를 가져오거나 없으면 404 띄우기
#     return render(request, 'polls/detail.html', {'question': question})
#
# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)
#
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])    # POST로 전달받은 값 중에 choice 항목의 value 반환
#     except (KeyError, Choice.DoesNotExist):                                     # ex. request_POST = { 'choice' : 1}
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()  # 계산하고 저장도 따로 해줘야 함
#         # POST를 성공적으로 전달 받고 나면 리다이렉트를 항상 해주어야 함
#         # 사용자가 뒤로 가기 버튼을 눌러서 data가 두번 POST 되는 일을 막아줌
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
# # 우리의 vote() 뷰에는 작은 문제가 있습니다. 먼저 데이터베이스에서 selected_choice 객체를 가져온 다음, votes 의 새 값을 계산하고 나서, 데이터베이스에 다시 저장합니다.
# # 만약 여러분의 웹사이트에 두 명의 사용자가 정확하게 같은 시간 에 투표를 할려고 시도할 경우, 잘못될 수 있습니다.
# # votes 의 조회값이 42라고 할 경우, 두 명의 사용자에게 새로운 값인 43이 계산 되고, 저장됩니다. 그러나 44가 되야되겠죠.
# # https://docs.djangoproject.com/ko/4.0/ref/models/expressions/#avoiding-race-conditions-using-f