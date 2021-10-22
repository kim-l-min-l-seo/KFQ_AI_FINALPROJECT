"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# view 파일 import
from .view.ver1 import Ver1
from .view.ver2 import Ver2

theme = "ver2"

if theme == "ver1":
    switch = Ver1
else:
    switch = Ver2

urlpatterns = [
    
    #------------------------------ | ************ Theme ************ | ------------------------------#
    # Theme Ver 1
    path('ver1/dashboard/index=<num>',      Ver1.dashboard,                 name='Ver1_dashboard'),
    path('ver1/apps/<app>/<email>',         Ver1.apps,                      name='Ver1_dashboard'),
    path('ver1/charts/<chart>',             Ver1.chart,                     name='Ver1_dashboard'),
    path('ver1/bootstrap/<bootstrap>',      Ver1.bootstrap,                 name='Ver1_dashboard'),
    path('ver1/plugins/<plugin>',           Ver1.plugins,                   name='Ver1_dashboard'),
    path('ver1/widget',                     Ver1.widget,                    name='Ver1_dashboard'),
    path('ver1/form/<form>',                Ver1.form,                      name='Ver1_dashboard'),
    path('ver1/table/<table>',              Ver1.table,                     name='Ver1_dashboard'),
    path('ver1/page/<pageData>',            Ver1.page,                      name='Ver1_dashboard'),

    # Theme Ver 2
    path('ver2/dashboard/',                 Ver2.dashboard,                 name='Ver2_dashboard'),
    path('ver2/tables/',                    Ver2.tables,                    name='Ver2_tables'),
    path('ver2/billing/',                   Ver2.billing,                   name='Ver2_billing'),
    path('ver2/virtual_reality/',           Ver2.virtual_reality,           name='Ver2_virtual_reality'),
    path('ver2/rtl/',                       Ver2.rtl,                       name='Ver2_rtl'),
    path('ver2/profile/',                   Ver2.profile,                   name='Ver2_dashboard'),
    path('ver2/sign_in/',                   Ver2.sign_in,                   name='Ver2_sign_in'),
    path('ver2/sign_up/',                   Ver2.sign_up,                   name='Ver2_sign_up'),
]
