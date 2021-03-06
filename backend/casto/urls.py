"""casto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
import user.views
import operation.views

urlpatterns = [
    path('/', user.views.index),
    path('', user.views.index),
    path('index/', user.views.index),
    path('admin/', admin.site.urls),
    path('signup/', user.views.signup),
    path('login/', user.views.login),
    path('logout/', user.views.logout),
    path('dashboard/', operation.views.query),
    path('info/', user.views.info),
    path('operation/upload/', operation.views.upload),
    path('operation/<int:net_id>/net/', operation.views.net),
    path('operation/delete/', operation.views.delete),
    path('operation/query/', operation.views.query),
    path('operation/get/', operation.views.get),
    path('admin/dashboard/', operation.views.query_admin),
    path('admin/get/', operation.views.get_admin),
    path('admin/delete/', operation.views.delete_admin),
]
