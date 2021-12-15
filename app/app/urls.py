"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.views.generic.base import RedirectView


from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('ping', views.ping, name='ping'),
    path('presentations/<str:pk>/polls', views.polls, name='polls'),
    path('templates', views.templates, name='templates'),
    path('presentations', views.presentations, name='presentations'),
    path('ping', RedirectView.as_view(url='https://infra.devskills.app/api/interactive-presentation/ping', permanent=True), name='ping'),
    #path('templates', RedirectView.as_view(url='https://infra.devskills.app/api/interactive-presentation/templates', permanent=True), name='ping'),
    #path('presentations', RedirectView.as_view(url='https://infra.devskills.app/api/interactive-presentation/presentations', permanent=True), name='ping'),
]
