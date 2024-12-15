from django.urls import path
from .views import (
    RegisterView, 
    LoginView, 
    LogoutView, 
    MFASetupView, 
    MFAConfirmView,
    FileListView, 
    FileUploadView, 
    FileDownloadView, 
    ShareFileView, 
    AccessShareView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('mfa-setup/', MFASetupView.as_view(), name='mfa-setup'),
    path('mfa-confirm/', MFAConfirmView.as_view(), name='mfa-confirm'),
    path('files/', FileListView.as_view(), name='file-list'),
    path('files/upload/', FileUploadView.as_view(), name='file-upload'),
    path('files/<int:pk>/download/', FileDownloadView.as_view(), name='file-download'),
    path('share/', ShareFileView.as_view(), name='file-share'),
    path('share/<uuid:token>/', AccessShareView.as_view(), name='access-share'),
]
