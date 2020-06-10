from django.http import HttpResponseForbidden
from django.utils import timezone
from .models import Post, Comment
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, CommentForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import (ListView, DetailView, DeleteView, CreateView, UpdateView)

from django.views.generic import TemplateView




class PostList(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    queryset = Post.objects.order_by('-published_date')
    context_object_name = 'posts'
    paginate_by = 3


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'text']
    template_name = 'blog/post_edit.html'
    login_url = '/login'

    def test_func(self):
        if not self.request.user.profile.banned:
            return True
        return False

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'text']
    template_name = 'blog/post_edit.html'
    login_url = '/login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if not self.request.user.profile.banned:
            post = self.get_object()
            group = Group.objects.get(name='moder')
            if self.request.user == post.author or group in self.request.user.groups.all():
                return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        if not self.request.user.profile.banned:
            post = self.get_object()
            group = Group.objects.get(name='moder')
            if self.request.user == post.author or group in self.request.user.groups.all():
                return True
        return False


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    form = CommentForm()
    if request.method == 'POST':
        print('fdfd')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
        else:
            form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'form': form
    }
    return render(request, 'blog/post_detail.html', context)


def delete_comment(request, pk, id):
    comment = get_object_or_404(Comment, id=id)
    post = get_object_or_404(Post, pk=pk)
    group = Group.objects.get(name='moder')
    if request.user.username == comment.author or group in request.user.groups.all():
        if request.method == 'POST':
            comment.delete()
            return redirect('/')
    else:
        return redirect('forbidden')
    context = {'comment': comment,
               'post': post}
    return render(request, 'blog/delete_comment.html', context)


def update_comment(request, pk, id):
    comment = get_object_or_404(Comment, id=id)
    post = get_object_or_404(Post, pk=pk)
    group = Group.objects.get(name='moder')
    if request.user.username == comment.author or group in request.user.groups.all():
        form = CommentForm(instance=comment)
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user.username
                comment.published_date = timezone.now()
                comment.save()
                return redirect('post_detail', pk=post.pk)
    else:
        return redirect('forbidden')
    return render(request, 'blog/update_comment.html', {'form': form})


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def forbidden(request):
    return HttpResponseForbidden('<h1 align="center">Forbidden 403</h1>')

# Create your views here.
