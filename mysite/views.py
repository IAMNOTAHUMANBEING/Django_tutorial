from django.views.generic.base import TemplateView
from django.apps import apps

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['app_list'] = ['polls', 'books'] # app.py 활용하여 아래 5줄로 하드코딩을 대체
        dictVerbose = {}
        for app in apps.get_app_configs():  # setting.py의 INSTALLED_APPS에 등록된 각 앱의 설정클래스들을 담은 리스트 반환
            if 'site-packages' not in app.path: # 물리적 경로 중에 site-packages가 있으면 외부 앱이므로 제외
                dictVerbose[app.label] = app.verbose_name # ex. 'books': 'Book-Author-Publisher App'
        context['verbose_dict'] = dictVerbose
        return context
