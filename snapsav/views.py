import os
import uuid
import yt_dlp
import threading

from django.shortcuts import render
from django.http import FileResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

# Pages
def index(request):
    return render(request, 'index.html')

def facebook_page(request):
    return render(request, 'facebook.html')

def tiktok_page(request):
    return render(request, 'tiktok.html')

# Download Handlers
@csrf_exempt
def download_video(request):
    return handle_download(request, source="instagram")

@csrf_exempt
def facebook_download(request):
    return handle_download(request, source="facebook")

@csrf_exempt
def tiktok_download(request):
    return handle_download(request, source="tiktok")

# Common downloader logic
def handle_download(request, source="generic"):
    if request.method == 'POST':
        url = request.POST.get('url')
        if not url:
            return HttpResponseBadRequest('No URL provided')

        try:
            filename = f"{uuid.uuid4()}.mp4"
            output_path = f"/tmp/{filename}"

            ydl_opts = {
                'outtmpl': output_path,
                'format': 'mp4',
                'quiet': True,
                'noplaylist': True,
                'merge_output_format': 'mp4',
                'nocheckcertificate': True,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                },
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            response = FileResponse(open(output_path, 'rb'), as_attachment=True, filename=f"{source}_video.mp4")
            threading.Timer(5.0, lambda: os.remove(output_path)).start()

            return response

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return HttpResponseBadRequest('Invalid request method')
