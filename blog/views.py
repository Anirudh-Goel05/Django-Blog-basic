from django.shortcuts import render,redirect,get_object_or_404
from .models import Post,Comment
from django.views.generic import TemplateView,ListView,DetailView,FormView,UpdateView,DeleteView,CreateView
from .forms import PostCreateForm,CommentCreateForm
from django.urls import reverse,reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.decorators import login_required
# Create your views here.

class Index(TemplateView):
    template_name = 'blog/index.html'

class PostListView(ListView):
    model = Post
    context_object_name = 'post_list'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

# @login_required
class PostCreateView(LoginRequiredMixin,FormView):
    login_url = '/admin/login/'
    # redirect_field_name = 'blog:posts_list'

    template_name = 'blog/post_create.html'
    form_class = PostCreateForm
    success_url = 'blog:posts_list'

    def form_valid(self,form):
        post = form.save(commit=False)
        post.author = self.request.user
        # post.publish()
        post.save()
        return redirect('blog:post_publish_confirm',pk=post.pk)

def PostPublishConfirm(request,pk):
    post = get_object_or_404(Post,pk=pk)

    if request.method == 'POST':
        post.publish()
        post.save()
        return redirect('blog:post_detail',pk=post.pk)

    form = PostCreateForm(instance=post)
    for key in form.fields.keys():
            form.fields[key].widget.attrs['readonly'] = True
    return render(request,'blog/post_confirm_publish.html',context={'form':form})


class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/admin/login/'

    model = Post
    fields =['title','text',]
    template_name_suffix = '_update_form'

class PostDeleteView(LoginRequiredMixin,DeleteView):
    login_url = 'admin/login/'

    model = Post
    success_url = reverse_lazy('blog:posts_list')
    template_name_suffix = '_confirm_delete'


#####################################

@login_required(login_url='/admin/login')
def add_comment_to_post(request,pk):
    form=CommentCreateForm()
    post=get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        comment=form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return redirect('blog:post_detail',pk=post.pk)
    return render(request,'blog/add_comment.html',context={'form':form})

@login_required(login_url='/admin/login')
def delete_comment_from_post(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail',pk=post_pk)
    else:
        return render(request,'blog/delete_comment.html',context={'comment':comment})
