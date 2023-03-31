from rest_framework_nested import routers
from . import views, signals


router = routers.DefaultRouter()
router.register('profile', views.ProfileViewSet, 'profile')

urlpatterns = router.urls
