from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView,TemplateView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from blog.models import Post
from .models import Profile
from .forms import CustomUserCreationForm,LoginForm,UpdateUserForm,UpdateProfileForm
# Create your views here.
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
    context_object_name = 'user'

class UpdateProfileView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    form_class = UpdateProfileForm
    model = Profile
    template_name='profile.html'
    #context_object_name = 'profile'
    success_message = "Your profile account is updated successfully"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["post"] = Post.objects.filter(author=self.request.user)
        return context