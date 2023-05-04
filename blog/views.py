from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import ListView, DetailView,TemplateView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
#from accounts.models import Profile
from django.core.paginator import Paginator,EmptyPage
from django.db.models import Q
#from django.http import response
#from django.contrib import messages 
from .forms import PostForm, CommentForm
from .models import Post , Comment , Category

# Create your views here.
class BlogHomeView(TemplateView):
    template_name='index.html'
    #model = Profile
    #def get_context_data(self, **kwargs):
        #context = super().get_context_data(**kwargs)
        #context['user_id'] = self.request.user.id
        #return context

#@login_required
#def profile(request):
    #if request.method == 'POST':
        #profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        #if profile_form.is_valid():
            #profile_form.save()
            #messages.success(request, 'Your profile is updated successfully')
            #return redirect(to='index')
        #else:
            #profile_form = UpdateProfileForm(instance=request.user.profile)
    #profile_form = UpdateProfileForm(instance=request.user.profile)
    
    #return render(request, 'profile.html', {'profile_form': profile_form ,'profile' : profile })


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
#oedering show how to list the post
class BlogListView(ListView):
    model=Post
    context_object_name = 'post_list'
    template_name='home.html'
    ordering = ['date']
    paginate_by = 4
    paginator_class = MyPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page',1)
        posts = Post.objects.all()
        Paginator = self.paginator_class(posts,self.paginate_by)
        posts = Paginator.page(page)

        context['posts']=posts
        return context
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["category_list"] = Category.objects.all()
        return context


#add a permissionrequiedmixin only user allowed can read all post
class BlogDetailView(LoginRequiredMixin,DetailView):
    model=Post
    form_class = CommentForm
    context_object_name = 'post'
    template_name='details.html'
    permission_required = 'blog.special_status'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["category_list"] = Category.objects.all()
        return context
    

class BlogCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model=Post
    template_name='create_new.html'
    form_class = PostForm
    success_url=reverse_lazy('home')
    success_message = "Your post has been created successfully"
    
    #this give the createview to automatically add the author as the user logged in
    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
class CategoryCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model= Category
    template_name='create_category.html'
    fields = '__all__'
    success_url=reverse_lazy('home')
    success_message = "Your category has been added"

def CategoryView(request ,cats):
    category_posts = Post.objects.filter(category=cats)
    return render(request, 'categories.html',{'cats':cats.title(), 'category_posts': category_posts})

    
#userpassestestmixin give an authorization to only the owner of the content 
class BlogUpdateView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,UpdateView):
    model=Post
    template_name='edit_post.html'
    fields=['title','body']
    success_message = "Your post has been updated successfully"
    #only the user of the post can delete or update the post
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
    
class BlogDeleteView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,DeleteView):
    model=Post
    template_name='delete_post.html'
    success_url=reverse_lazy('home')
    success_message = "Your post has been deleted successfully"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
    
@login_required
def postlikes(request,pk):
    post = get_object_or_404(Post,id=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('details',pk=post.pk)

    
class SearchResultListView(ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'search_results.html'
    #this one under my comment filter microsft from title using icontain to ignore case sensitive
    #queryset = Post.objects.filter(title__icontains='microsoft')

    #this function query the model with the user input q and filter from title or date
    def get_queryset(self):
        query = self.request.GET.get('q')
        return Post.objects.filter(Q(title__icontains=query)| Q(date__icontains=query))
    
class CommentCreateView(LoginRequiredMixin,CreateView):
    model = Comment
    form_class = CommentForm
    template_name='details.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


