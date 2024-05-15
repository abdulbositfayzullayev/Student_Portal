from django.urls import path
from .views import home,books,dictionary,homework,todo,youtube,wiki,delete_homework,delete_todo,SignUpView

urlpatterns = [
    path('',home,name='home'),

    path('books/',books,name='books'),

    path('dictionary/',dictionary,name='dictionary'),

    path('homework/',homework,name='homework'),
    path('homework/<int:pk>/delete',delete_homework,name='delete_homework'),

    path('todo/',todo,name='todo'),
    path('todo/<int:pk>/delete',delete_todo,name='delete_todo'),

    path('youtube/',youtube,name='youtube'),
    
    path('wiki/',wiki,name='wiki'),
    path('signup/',SignUpView.as_view(),name='signup'),
]
