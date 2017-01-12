"""reactivos_update URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from compounds_update_app import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.RedirectToLoginView.as_view() ,name="login_redirect"),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^listado_reactivos/(?P<id>[0-9]+)/', login_required(views.ListaReactivosView.as_view()),
        name="listado_reactivos"),
    url(r'^reactivo/add/', views.create_reactivo_view, name="add_reactivo"),
    url(r'^login/', views.LoginView.as_view(), name="login"),
    url(r'^logout/', views.logout_view, name="logout"),
    url(r'reactivo/(?P<pk>[0-9]+)/', views.UpdateReactivoView.as_view(), name='update_reactivo'),
]
