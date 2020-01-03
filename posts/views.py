from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import LikeonPost, CommentonPost
from notifications.models import Notification
# Create your views here.


@login_required
def PostDetailView(request, *args, **kwargs):

    post = get_object_or_404(Post, pk = kwargs['pk'])
    follower_find = post.owner.profile.followers.all().filter(user = request.user)
    
    if not request.user == post.owner and not follower_find.exists() :
        return HttpResponseForbidden()

    has_liked = LikeonPost.objects.filter(user = request.user, post = post).exists()
    
    if request.method == 'POST':
        
        if 'like' in request.POST:
            
            if has_liked:
                obj = LikeonPost.objects.filter(user = request.user, post = post).delete()
                post.likecount = post.likecount - 1
                Notification.objects.filter(concerned_user = post.owner, action_user = request.user, notification_type = 'like', post = post).delete()
                post.save()
                has_liked = False

            else:
                obj = LikeonPost.objects.create(user = request.user, post = post)
                Notification.objects.create(concerned_user = post.owner, action_user = request.user, notification_type = 'like', post = post)
                has_liked = True
            
        if 'comment' in request.POST:
            obj = CommentonPost.objects.create(user = request.user, post = post, comment = request.POST['comment'])
            Notification.objects.create(concerned_user = post.owner, action_user = request.user, notification_type = 'comment', post = post)


    return render(request, 'detail.html', {'post' : post, 'has_liked': has_liked})



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['image', 'caption']
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user     
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['image', 'caption']
    template_name = 'post_form.html'

    def form_valid(self, form):
        
        form.instance.owner = self.request.user     
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.owner:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_delete_confirm.html'
    success_url = '/'

    def  test_func(self):
        post = self.get_object()
        if self.request.user == post.owner:
            return True
        return False













