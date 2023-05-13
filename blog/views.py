from typing import Any, Dict, Optional
from taggit.models import Tag
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import ListView, DetailView,TemplateView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormMixin
from django.urls import reverse_lazy
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
#from accounts.models import Profile
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
#from django.http import response
#from django.contrib import messages 
from .forms import PostForm, CommentForm
from .models import Post , Comment , PopularPost ,PopularPostManager

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
        except PageNotAnInteger:
            return self.num_pages
#loginrequiredmixin redirect user that's not login, paginate_by give how many object i want to display per page
#ordering show how to list the post
#we specify a context_object_name if we dont set a default varible is object_list by generic 
#we also have queryset by defualt which is model_name.objects.all for listview
class BlogListView(ListView):
    model=Post
    context_object_name = 'post_list'
    template_name='home.html'
    ordering = ['date']
    paginate_by = 4
    paginator_class = MyPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = Tag.objects.all()
        #the method below retrieve page number parameter it contain the requested page number if thr page parameter is not in the get parameters of the request we use the default value 1 to load the first page of results
        page = self.request.GET.get('page',1)
        posts = Post.objects.get_queryset().order_by('pk')
        Paginator = self.paginator_class(posts,self.paginate_by)
        posts = Paginator.page(page)
        context['tags']=tags
        context['posts']=posts
        return context

 
 #this function take in a request and tag_slug the post_list get all objects in our post model 
 #we give tag a default value which is none if tag_slug exist we get the object of the tag_slug we take in from the url
 #from the Tag model we make another varible of post_list and filter tags in the object tag we get from our initial post_list which 
# is the objects of all post model we then return render the template and context
   
def post_list(request,tag_slug=None):
    post_list = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list,1)
    page_number = request.GET.get('page',1 )
    try:
        post_list = paginator.page(page_number)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    return render(request,'home.html',{'post_list': post_list, 'tag': 'tag'})
 
#add a permissionrequiedmixin only user allowed can read all post
class BlogDetailView(LoginRequiredMixin,DetailView):
    model=Post
    context_object_name = 'post'
    template_name='details.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        post = Comment.objects.filter(post=self.get_object()).order_by('-timestamp')
        # Add in a QuerySet of all the books
        context["comments"] = post

        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm(instance=self.request.user)

        return context
    
    def post(self,request,*args,**kwargs):
        new_comment = Comment(comment=request.POST.get('comment'),author=self.request.user,post=self.get_object())
        new_comment.save()
        return self.get(self,request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context

        context = super().get_context_data(**kwargs)
        try:
            #this function below get all objects of the model
            post = self.get_object()
            post_tags_ids = post.tags.values_list('pk',flat=True)
            similar_posts = Post.objects.filter(tags__in=post_tags_ids)\
                                        .exclude(pk=post.pk)
            similar_posts = similar_posts.annotate(same_tags_in_post=Count('tags'))\
                                        .order_by('-same_tags_in_post',)[:4]
            
        except Post.DoesNotExist:
            raise Http404("No post found.")
        # Add in a QuerySet of all the books
        context["similar_posts"] = similar_posts
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
    #or how to make only the user of the post can edit and update the post
   # def get_queryset(self):
        #return self.model.objects.filter(author=self.request.user)
    
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

@require_POST
def post_comment(request ,pk):
    post = get_object_or_404(Post,pk=pk)
    comment = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('details',pk=post.pk)
    else:
        form = CommentForm()
    return render(request , 'comment.html',{'post': post,'form': form ,'comment': comment})

    
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
    model = Post
    form_class = CommentForm
    template_name='details.html'

    #def form_valid(self, form):
        #form.instance.author = self.request.user
        #form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        #return super().form_valid(form)


