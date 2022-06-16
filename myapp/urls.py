from django.urls import path
from .views import*

urlpatterns = [
    path('',index,name='index'),
    path('create/',Createuser.as_view()),
    path('login/',LoginAPI.as_view()),
    path('hr-list/',HrlistView.as_view()),
    path('edit-hr/<int:pk>',EditView.as_view()),
    path('delete-hr/<int:pk>',DeleteView.as_view()),
    path('edit-user/<int:pk>',UserProfileView.as_view()),
    path('add-job/',PostjobView.as_view()),
    path('my-job/',JobViewAPI.as_view()),
    path('edit-post/<int:pk>',Editjobview.as_view()),
    path('delete-post/<int:pk>',Deletejobview.as_view()),
    path('apply/',ApplicationView.as_view()),
    path('mypostapplication/<int:pk>',MyPostApplicationView.as_view())
    
    
    
    
    
]
    
