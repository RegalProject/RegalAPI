from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('profile', views.ProfileViewSet, 'profile')
router.register('users', views.UserListView, 'users')
router.register('userEdit', views.CustomUserEditViewSet, 'userEdit')

urlpatterns = router.urls
