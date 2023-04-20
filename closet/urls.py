from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('ownedItem', views.OwnedItemViewSet, 'ownedItem')

urlpatterns = router.urls