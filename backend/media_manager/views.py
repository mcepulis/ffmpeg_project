from rest_framework import generics
from .serializers import VideoSerializer, AudioSerializer
import os
import subprocess
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Video, Audio
import datetime


class VideoUploadView(generics.CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class AudioUploadView(generics.CreateAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer


@csrf_exempt
def upload_and_merge_files(request):
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y%m%d%H%M%S')
    video_file_name = f'video_{timestamp}.mp4'

    if request.method == 'POST':
        video_file = request.FILES.get('video')
        audio_file = request.FILES.get('audio')

        if not video_file or not audio_file:
            return JsonResponse({'error': 'Both video and audio files are required.'}, status=400)
        
        if not video_file.name.endswith('.mp4') or not audio_file.name.endswith('.mp4'):
            return JsonResponse({'error': 'Both video and audio files must be in MP4 format.'}, status=400)
        
        video_path = os.path.join(settings.MEDIA_ROOT, video_file.name)
        audio_path = os.path.join(settings.MEDIA_ROOT, audio_file.name)
        with open(video_path, 'wb') as f:
            for chunk in video_file.chunks():
                f.write(chunk)

        with open(audio_path, 'wb') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)

          # Define the output file path with timestamp in the name
        output_file = os.path.join(settings.MEDIA_ROOT, f'output_{timestamp}.mp4')
        
        # Call FFmpeg with the corrected command
        command = [r'C:\ffmpeg\bin\ffmpeg.exe', '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'aac', output_file]
        subprocess.run(command, check=True)

        # Return the URL to the output file
        output_url = os.path.join(settings.MEDIA_URL, f'output_{timestamp}.mp4')
        subprocess.run(command, check=True)

        output_url = os.path.join(settings.MEDIA_URL, 'output.mp4')

        return JsonResponse({'message': 'Files uploaded and merged successfully', 'output_url': output_url}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)