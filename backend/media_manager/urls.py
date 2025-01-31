from django.urls import path
from .views import VideoUploadView, AudioUploadView, upload_and_merge_files

urlpatterns = [
    path('upload/video', VideoUploadView.as_view(), name='upload-video'),
    path('upload/audio', AudioUploadView.as_view(), name='upload-audio'),
    path('upload-and-merge/', upload_and_merge_files, name='upload-and-merge'),
]


