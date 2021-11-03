from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
# Create your views here.

def test(request):
    return HttpResponse("Web Page Test SUCCESS")

def start (request):
    print("Theme choice")
    return render(request, './StartProject.html')
    return HttpResponse(
        "<h1>Theme Page</h1> <br>"
        "<a href=\"/theme/ver1/dashboard/index=1\">Var 1 Dashboard index = 1</a> <br>"
        "<a href=\"/theme/ver1/dashboard/index=2\">Var 1 Dashboard index = 2</a> <br>"
        "<a href=\"/theme/ver2/dashboard/\">Var 2 Dashboard</a> <br><br>"
        "<h1>Web Site Page</h1> <br>"
        "<a href=\"/web/dashboard/index=1\">Var 1 Dashboard index = 1</a> <br>"
        )


