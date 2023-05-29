from django.views.generic import TemplateView
from .models import Post

class Home(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_blogs'] = Post.objects.all().order_by('-creation_datetime')[:5]
        
        return context