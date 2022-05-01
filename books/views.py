from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from books.models import Book, Author, Publisher

class BooksModelView(TemplateView):
    template_name = 'books/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_list'] = ['Book', 'Author', 'Publisher']
        return context

class BookList(ListView):
    # 리스트 뷰를 상속하는 경우 객체가 들어있는 컨텍스트 변수를 템플릿으로 넘겨주면 됨
    # 리스트를 테이블에 들어있는 모든 레코드를 가져와 구성하는 경우 model만 지정하면 됨
    model = Book
    # 디폴트로 컨텍스트 변수로 object_list를 사용하고 템플릿 파일로 모델명소문자_list.html 사용

class AuthorList(ListView):
    model = Author

class PublisherList(ListView):
    model = Publisher

class BookDetail(DetailView):
    model = Book
    # 객체 하나를 컨텍스트 변수를 이용해 템플릿으로 넘겨주면 됨
    # 만약 테이블에서 primary key로 조회해서 특정 객체를 가져오는 경우에는 모델만 지정하면 됨
    # 조회 시 사용할 Pk 값은 urlconf에서 추출하여 뷰로 넘어온 파라미터를 사용함

class AuthorDetail(DetailView):
    model = Author

class PublisherDetail(DetailView):
    model = Publisher

