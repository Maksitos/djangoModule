"""someMagaz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from myMagaz.views import Main, Registration, LoginPage, Logout, AddProduct, PurchaseProduct
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('magaz-main', Main.as_view()),
    path('registration', Registration.as_view(), name='register'),
    path('login', LoginPage.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('add-product', AddProduct.as_view(), name='add-product'),
    path('pur', PurchaseProduct.as_view(), name='purchase')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

