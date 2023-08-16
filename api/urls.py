
from django.urls import re_path as url
from django.urls import include
from django.contrib import admin
from api import views
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)




urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^test-payment/$', views.test_payment),
    url(r'^save-stripe-info/$', views.save_stripe_info),
    url('api-auth/', include('rest_framework.urls')),
    url('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    url('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url('api/credits/', views.GetCredits.as_view()),
    url('api/priceId/', views.GetCurrentPriceId.as_view()),
    url('api/testing', views.Test.as_view()),
]


router = DefaultRouter()
router.register('user', UserViewSet, basename='user')
urlpatterns += router.urls