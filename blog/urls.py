from django.urls import path
from .views import BlogListView,BlogDetailView,BlogCreateView,BlogUpdateView,BlogDeleteView,BlogHomeView,SearchResultListView,CategoryCreateView,CategoryView,postlikes,CommentCreateView
#from .views import profile
# more update about the uuid 
urlpatterns=[
    path('', BlogHomeView.as_view(), name='index'),
    path('home/', BlogListView.as_view(), name='home'),
    path('details/<uuid:pk>/',BlogDetailView.as_view(),name='details'),
    path('create/new/',BlogCreateView.as_view(),name='create'),
    path('post/<uuid:pk>/edit/',BlogUpdateView.as_view(),name='edit'),
    path('post/<uuid:pk>/delete/',BlogDeleteView.as_view(),name='delete'),
    path('post/<uuid:pk>/comment/',CommentCreateView.as_view(),name='make_comment'),
    path('search/',SearchResultListView.as_view(),name = 'search_results'),
    path('create/category/',CategoryCreateView.as_view(),name='category'),
    path('category/<str:cats>/',CategoryView, name='category_list'),
    path('post/<uuid:pk>/like/',postlikes,name='like_post'),
]