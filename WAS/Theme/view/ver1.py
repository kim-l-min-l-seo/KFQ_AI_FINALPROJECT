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
        if bootstrap == "accordion":
            return render(request, './ver1/4_Bootstrap/01_ui-accordion.html', context)
        elif bootstrap == "alert":
            return render(request, './ver1/4_Bootstrap/02_ui-alert.html', context)
        elif bootstrap == "badge":
            return render(request, './ver1/4_Bootstrap/03_ui-badge.html', context)
        elif bootstrap == "button":
            return render(request, './ver1/4_Bootstrap/04_ui-button.html', context)
        elif bootstrap == "modal":
            return render(request, './ver1/4_Bootstrap/05_ui-modal.html', context)
        elif bootstrap == "button-group":
            return render(request, './ver1/4_Bootstrap/06_ui-button-group.html', context)
        elif bootstrap == "list-group":
            return render(request, './ver1/4_Bootstrap/07_ui-list-group.html', context)
        elif bootstrap == "media-object":
            return render(request, './ver1/4_Bootstrap/08_ui-media-object.html', context)
        elif bootstrap == "card":
            return render(request, './ver1/4_Bootstrap/09_ui-card.html', context)
        elif bootstrap == "carousel":
            return render(request, './ver1/4_Bootstrap/10_ui-carousel.html', context)
        elif bootstrap == "dropdown":
            return render(request, './ver1/4_Bootstrap/11_ui-dropdown.html', context)
        elif bootstrap == "popover":
            return render(request, './ver1/4_Bootstrap/12_ui-popover.html', context)
        elif bootstrap == "progressbar":
            return render(request, './ver1/4_Bootstrap/13_ui-progressbar.html', context)
        elif bootstrap == "tab":
            return render(request, './ver1/4_Bootstrap/14_ui-tab.html', context)
        elif bootstrap == "typography":
            return render(request, './ver1/4_Bootstrap/15_ui-typography.html', context)
        elif bootstrap == "pagination":
            return render(request, './ver1/4_Bootstrap/16_ui-pagination.html', context)
        elif bootstrap == "grid":
            return render(request, './ver1/4_Bootstrap/17_ui-grid.html', context)
        elif bootstrap == "label":
            return render(request, './ver1/4_Bootstrap/18_ui-label.html', context)
        elif bootstrap == "tooltip":
            return render(request, './ver1/4_Bootstrap/19_ui-tooltip.html', context)
        
    def plugins(request, plugin):
        print("plugins", plugin)
        page = 'plugins'
        context = {
            'page': page
        }
        if plugin == "select2":
            return render(request, './ver1/5_Plugins/1_uc-select2.html', context)
        elif plugin == "nestable":
            return render(request, './ver1/5_Plugins/2_uc-nestable.html', context)
        elif plugin == "noui-slider1":
            return render(request, './ver1/5_Plugins/3_uc-noui-slider.html', context)
        elif plugin == "sweetalert":
            return render(request, './ver1/5_Plugins/4_uc-sweetalert.html', context)
        elif plugin == "toastr":
            return render(request, './ver1/5_Plugins/5_uc-toastr.html', context)
        elif plugin == "map-jqvmap":
            return render(request, './ver1/5_Plugins/6_map-jqvmap.html', context)

    def widget(request):
        print("widget")
        page = 'widget-basic'
        context = {
            'page': page
        }
        return render(request, './ver1/widget-basic.html', context)
