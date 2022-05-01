from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone
import logging
logger = logging.getLogger(__name__)    # polls.views 로거 객체 취득, __name__은 모듈경로를 담고 있는 파이썬 내장 변수
# view.py 파일의 모듈경로는 polls.views이고 이것이 우리가 사용하고자 하는 로거의 객체의 이름
# 이 로거에서 생산한 로거 레코드는 상위 polls 로거에게 전파되고 polls 로거에서 메세지를 기록합니다.
# 이 동작을 위해 setting.py에 polls 로거를 설정함.

# 제네릭 뷰
class IndexView(generic.ListView):  # 테이블에서 복수의 레코드를 가져와야하므로 ListView 이용
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    # 자동으로 ListView는 context 변수로 question_list를 제공, 템플릿에 사용한 것과 같게 수정

    def get_queryset(self): # 테이블에 들어있는 모든 레코드를 가져오는 경우 model 지정, 그렇지 않은 경우 get_queryset 오버라이딩
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]  
        # 슬라이싱을 사용하면 쿼리셋이 아닌 리스트를 반환함 주의
        # 현재 시점보다 생성일자가 작거나 같은 오브젝트 5개
        # 쿼리셋: DB에서 꺼내 온 객체의 모음, filter, exclude 기능 가지고 쿼리셋으로 반환함
        # object 객체는 테이블 정보를 갖고있는 객체로 쿼리셋을 얻어올 때 사용

class DetailView(generic.DetailView):   # 테이블에서 특정 한 개의 레코드를 가져와야하므로 DetailView 이용
    model = Question    # 모델 지정하면 url에서 받은 pk로 알아서 특정 객체를 템플릿으로 넘겨줌
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    logger.debug("vote().question_id: %s" % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])    # POST로 전달받은 값 중에 choice 항목의 value 반환 ex. request_POST = { 'choice' : 1}
    except (KeyError, Choice.DoesNotExist):     # 키가 없는 경우와 검색 조건에 맞는 객체가 없는 경우
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()  # 계산하고 저장도 따로 해줘야 함
        # POST를 성공적으로 전달 받고 나면 리다이렉트를 항상 해주어야 함
        # 사용자가 뒤로 가기 버튼을 눌러서 data가 두번 POST 되는 일을 막아줌
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))  # URL 패턴: URL 스트링 <-> 뷰, 리버스: 패턴으로부터 스트링을 구함

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