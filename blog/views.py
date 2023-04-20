from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin,PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView,TemplateView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy,reverse
from .models import Post , Comment
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage

# Create your views here.
class BlogHomeView(TemplateView):
    template_name='index.html'

#subclass that return the first page if the number is less then 1 and return last page if the number exceed the number of pages available
class MyPaginator(Paginator):
    def validate_number(self, number):
        try:   
            return super().validate_number(number)
        except EmptyPage:
            if int(number) >1 :
                return self.num_pages
            elif int(number) <1 :
                return 1
            else:
                raise
#loginrequiredmixin redirect user back to login to have access to that view or template
#paginate_by give how many object i want to display per page
class BlogListView(LoginRequiredMixin, ListView):
    model=Post
    template_name='home.html'
    paginate_by = 3
    paginator_class = MyPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page',1)
        posts = Post.objects.all()
        Paginator = self.paginator_class(posts,self.paginate_by)
        posts = Paginator.page(page)

        context['posts']=posts
        return context
        
        

#add a permissionrequiedmixin only user allowed can read all post
class BlogDetailView(LoginRequiredMixin,PermissionRequiredMixin, DetailView):
    model=Post
    template_name='details.html'
    permission_required = 'blog.special_status'

class BlogCreateView(LoginRequiredMixin,CreateView):
    model=Post
    template_name='create_new.html'
    fields=['title','body','picture']
    
    #this give the createview to automatically add the author as the user logged in
    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
#userpassestestmixin give an authorization to only the owner of the content 
class BlogUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    template_name='edit_post.html'
    fields=['title','body']
    #only the user of the post can delete or update the post
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
    


class BlogDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    template_name='delete_post.html'
    success_url=reverse_lazy('home')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class SignUpView( CreateView):
    form_class=CustomUserCreationForm
    success_url=reverse_lazy('login')
    template_name='registration/signup.html'

class CommentView(CreateView):
    model = Comment
    template_name = 'make_comment.html'
    fields = ['comment','post']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
    



