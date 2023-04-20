from django.urls import path
from .views import BlogListView,BlogDetailView,BlogCreateView,BlogUpdateView,BlogDeleteView,SignUpView,BlogHomeView,CommentView

# more update about the uuid 
urlpatterns=[
    path('', BlogHomeView.as_view(), name='index'),
    path('home', BlogListView.as_view(), name='home'),
    path('details/<uuid:pk>/',BlogDetailView.as_view(),name='details'),
    path('create/new/',BlogCreateView.as_view(),name='create'),
    path('post/<uuid:pk>/edit/',BlogUpdateView.as_view(),name='edit'),
    path('post/<uuid:pk>/delete',BlogDeleteView.as_view(),name='delete'),
    path('signup/',SignUpView.as_view(),name='signup'),
    path('comment',CommentView.as_view(),name='make_comment'),
]