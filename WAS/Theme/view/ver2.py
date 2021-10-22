from django.http.response import HttpResponse
from django.shortcuts import render, redirect


class Ver2:
    def dashboard(request):
        print("VER2")
        page = 'dashboard'
        context = {
            'page': page
        }
        return render(request, './ver2/1_dashboard.html', context)

    def tables(request):
        print("VER2")
        page = 'tables'
        context = {
            'page': page
        }
        return render(request, './ver2/2_tables.html', context)

    def billing(request):
        print("VER2")
        page = 'billing'
        context = {
            'page': page
        }
        return render(request, './ver2/3_billing.html', context)

    def virtual_reality(request):
        print("VER2")
        page = 'virtual_reality'
        context = {
            'page': page
        }
        return render(request, './ver2/4_virtual-reality.html', context)

    def rtl(request):
        print("VER2")
        page = 'rtl'
        context = {
            'page': page
        }
        return render(request, './ver2/5_rtl.html', context)

    def profile(request):
        print("VER2")
        page = 'profile'
        context = {
            'page': page
        }
        return render(request, './ver2/6_profile.html', context)

    def sign_in(request):
        print("VER2")
        page = 'sign_in'
        context = {
            'page': page
        }
        return render(request, './ver2/7_sign-in.html', context)

    def sign_up(request):
        print("VER2")
        page = 'sign_up'
        context = {
            'page': page
        }
        return render(request, './ver2/8_sign-up.html', context)
