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
    path('admin/', admin.site.urls),
    path('logon/', user.views.logon),
    path('login/', user.views.login),
    path('logout/', user.views.logout),
    path('operation/upload/', operation.views.upload),
    path('operation/<int:net_id>/net/', operation.views.net),
    path('operation/delete/', operation.views.delete),
    path('operation/query/', operation.views.query),
    path('operation/<int:operation_id>/get/', operation.views.get),
    path('admin/login/', user.views.login),
    path('admin/logout/', user.views.logout),
    path('admin/query/', operation.views.query_admin),
    path('admin/delete/', operation.views.delete_admin),

    # require_login 失败会重定向至该页面
    path('account/login/', user.views.please_login),
]
