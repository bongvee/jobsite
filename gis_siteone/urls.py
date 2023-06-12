from django.contrib import admin
from django.urls import include, path

# login using API
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework_simplejwt.views import TokenRefreshView     # ADDED

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('jobs_app.urls')),
    path('api/', include('account.urls')),

    # login using API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # ADDED
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
