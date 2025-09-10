from django.shortcuts import render
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from followers.models import Follower
from django.db.models import Q

# Create your views here.
class HomePageView(TemplateView):
    http_method_names = ['get']
    template_name = "feed/homepage.html" 

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        if self.request.user.is_authenticated:
            # Get list of users that the current user is following
            following = list(
                Follower.objects.filter(followed_by=self.request.user).values_list("following", flat=True)
            )
            
            if not following:
                # If user isn't following anyone, show all posts as non-followed
                followed_posts = Post.objects.none()
                non_followed_posts = Post.objects.all().order_by('-id')[0:30]
            else:
                # Posts from followed users
                followed_posts = Post.objects.filter(author__in=following).order_by('-id')[0:60]
                
                # Posts from non-followed users (excluding current user's own posts and followed users)
                non_followed_posts = Post.objects.exclude(
                    Q(author__in=following) | Q(author=self.request.user)
                ).order_by('-id')[0:30]
        else:
            # For anonymous users, all posts are considered non-followed
            followed_posts = Post.objects.none()
            non_followed_posts = Post.objects.all().order_by('-id')[0:30]
        
        context['followed_posts'] = followed_posts
        context['non_followed_posts'] = non_followed_posts
        return context

class PostDetailView(DetailView):
    http_method_names=['get']
    template_name="feed/detail.html"
    model= Post
    context_object_name='post'
    
class PostCreateView(LoginRequiredMixin, CreateView):
    template_name='feed/create.html'
    model= Post
    fields=['text']
    success_url='/'
    
    def dispatch(self, request, *args, **kwargs):
        self.request=request
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        obj=form.save(commit=False)
        obj.author=self.request.user
        obj.save()
        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        # TODO: There is a bug here when you go to /new/ to create a post.
        # You must figure out how to determine if this is an Ajax request (or not an ajax request).
        post = Post.objects.create(
            text=request.POST.get("text"),
            author=request.user,
        )

        return render(
            request,
            "includes/post.html",
            {
                "post": post,
                "show_detail_link": True,
            },
            content_type="application/html"
        )