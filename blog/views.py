from django.shortcuts import render
from django.views.generic import ListView, DetailView # new
from django.views.generic.edit import CreateView, UpdateView, DeleteView  # new
from django.urls import reverse_lazy # new

from .models import Post, Comment
from .forms import CommentForm


def add_comment(View):
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = Post.filter(request.post)
            # Save the comment to the database
            new_comment.save()

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/templates/home.html',
                  {'page': page,
                   'posts': posts})


class BlogListView(ListView):
    paginate_by = 3
    model = Post
    template_name = "home.html"


class BlogDetailView(DetailView): # new
    model = Post
    template_name = "post_detail.html"


class BlogCreateView(CreateView): # new
    model = Post
    template_name = "post_new.html"
    fields = ["title", "author", "body"]


class BlogUpdateView(UpdateView): # new
    model = Post
    template_name = "post_edit.html"
    fields = ["title", "body"]


class BlogDeleteView(DeleteView): # new
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("home")


class BlogCommentView(CreateView): # new
    model = Comment
    template_name = "post_comment.html"
    fields = ["title", "author", "body"]

