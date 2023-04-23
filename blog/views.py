from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView,TemplateView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy,reverse
from .models import Post , Comment, Profile
from django.views.generic import CreateView
from .forms import CustomUserCreationForm,LoginForm,UpdateUserForm,UpdateProfileForm
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage
from django.db.models import Q
from django.http import response
from django.contrib import messages 
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

# Create your views here.
class BlogHomeView(TemplateView):
    template_name='index.html'
    #def get_context_data(self, **kwargs):
        #context = super().get_context_data(**kwargs)
        #context['user_id'] = self.request.user.id
        #return context

class SignUpView(SuccessMessageMixin,CreateView):
    form_class=CustomUserCreationForm
    success_url=reverse_lazy('login')
    template_name='registration/signup.html'
    success_message = "Account successfully created!"

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(CustomLoginView, self).form_valid(form)
    
class UpdateUserView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    form_class = UpdateUserForm
    template_name='registration/update_user.html'
    success_message = "Your user account is updated successfully"
    context_object_name = 'profile'

@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        profile_form = UpdateProfileForm(instance=request.user.profile)

        return render(request, 'profile.html', {'profile_form': profile_form})




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
class BlogListView(ListView):
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



class CommentView(CreateView):
    model = Comment
    template_name = 'make_comment.html'
    fields = ['comment','post']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
class SearchResultListView(ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'search_results.html'

    #queryset = Post.objects.filter(title__icontains='microsoft')

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Post.objects.filter(Q(title__icontains=query)| Q(date__icontains=query))
    




