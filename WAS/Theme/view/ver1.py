from django.http.response import HttpResponse
from django.shortcuts import render, redirect


class Ver1:
    def dashboard(request, num):
        print("VER1", num)
        page = 'dashboard'
        context = {
            'page': page
        }
        if num == "1":
            return render(request, './ver1/1_Dashboard/index.html', context)
        else:
            return render(request, './ver1/1_Dashboard/index2.html', context)

    def apps(request, app, email):
        print("app", app)
        print("email", email)
        page = 'app'
        context = {
            'page': page
        }
        if app == "profile" and email == "x":
            return render(request, './ver1/2_Apps/1_app-profile.html', context)
        elif app == "email":
            if email == "compose":
                return render(request, './ver1/2_Apps/Email/email-compose.html', context)
            elif email == "inbox":
                return render(request, './ver1/2_Apps/Email/email-inbox.html', context)
            elif email == "read":
                return render(request, './ver1/2_Apps/Email/email-read.html', context)
        elif app == "calender" and email == "x":
            return render(request, './ver1/2_Apps/3_app-calender.html', context)
    
    def chart(request, chart):
        print("chart", chart)
        page = 'chart'
        context = {
            'page': page
        }
        if chart == "flot" :
            return render(request, './ver1/3_Charts/1_chart-flot.html', context)
        elif chart == "morris":
            return render(request, './ver1/3_Charts/2_chart-morris.html', context)
        elif chart == "chartjs":
            return render(request, './ver1/3_Charts/3_chart-chartjs.html', context)
        elif chart == "chartist":
            return render(request, './ver1/3_Charts/4_chart-flot.html', context)
        elif chart == "sparkline":
            return render(request, './ver1/3_Charts/5_chart-flot.html', context)
        elif chart == "peity":
            return render(request, './ver1/3_Charts/6_chart-flot.html', context)
 
    def bootstrap(request, bootstrap):
        print("bootstrap", bootstrap)
        page = 'bootstrap'
        context = {
            'page': page
        }
        if bootstrap == "flot":
            return render(request, './ver1/3_Charts/1_chart-flot.html', context)
