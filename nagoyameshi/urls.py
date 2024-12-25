import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from accounts import views  # 20241127 ChatGPT指示

# from accounts import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("restaurant.urls")),
    path(
        "accounts/login/", views.CustomLoginView.as_view(), name="login"
    ),  # 20241127 ChatGPT指示
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("accounts.urls")),
]

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

# 開発サーバーでメディアを配信できるようにする設定
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
