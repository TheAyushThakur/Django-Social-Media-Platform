from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .models import Post

# Create your views here.
class HomePageView(ListView):
    http_method_names= ['get']
    template_name="feed/homepage.html"
    model= Post
    context_object_name='posts'
    queryset= Post.objects.all().order_by('-id')[0:30]

class PostDetailView(DetailView):
    http_method_names=['get']
    template_name="feed/detail.html"
    model= Post
    context_object_name='post'
    
class PostCreateView(CreateView):
    template_name='feed/create.html'
    model= Post
    fields=['text']
    ## TODO: Add an image section to create a dynamic post like structure