from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def theme (request):
    print("Theme choice")
    print("Start Project")
    context = {
        
    }
    return render(request, '/StartProject.html', context)
    # return HttpResponse(
    #     "<a href=\"/theme/ver1/dashboard/index=1\">Var 1 Dashboard index = 1</a> <br>"
    #     "<a href=\"/theme/ver1/dashboard/index=2\">Var 1 Dashboard index = 2</a> <br>"
    #     "<a href=\"/theme/ver2/dashboard/\">Var 2 Dashboard</a> <br>"
    #     )
