from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Category


class HomePageView(ListView):
    model = Post
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('?')[:12]
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['post'] = self.object
        post = get_object_or_404(Post, slug=self.kwargs.get('slug'))
        kwargs['related_posts'] = Post.objects.filter(
                category=self.object.category).order_by('-created').exclude(slug=self.kwargs.get('slug'))
        return super().get_context_data(**kwargs)
    
    
class CategoryArticlesListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'posts'

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return Post.objects.filter(category=category)
    
    
def contact(request):
    return render(request, 'blog/contact.html')