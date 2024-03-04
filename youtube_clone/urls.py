"""
URL configuration for youtube_clone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
# from pages.views import home_page
from django.conf import settings
from django.conf.urls.static import static
from pages.views import home_page, signup_page, login_page, create_page, video_page, user_page, logout_view, subscribe_view, like_view, comment_view

urlpatterns = [
    # path("probs/", include("probs.urls")),
    # path("pages/", include("pages")),
    path("", home_page, name="homp_page"),
    path("signup/", signup_page, name="signup_page"),
    path("login/", login_page, name="login_page"),
    path("create/", create_page, name="create_page"),
    path("video/", video_page, name="video_page"),
    path("user/", user_page, name="user_page"),
    path("logout/", logout_view, name="logout_view"),
    path("like/", like_view, name="like_view"),
    path("comment/", comment_view, name="comment_view"),
    path("subscribe/", subscribe_view, name="subscribe_view"),
    path("admin/", admin.site.urls),
]

# urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)