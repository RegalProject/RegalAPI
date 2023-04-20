from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('ownedItem', views.OwnedItemViewSet, 'ownedItem')
router.register('publicItem', views.PublicItemViewSet, 'publicItem')
router.register('crawledItem', views.CrawledItemViewSet, 'crawledItem')
router.register('ownedItemByPK', views.OwnedItemByPKViewSet, 'ownedItemByPK')

urlpatterns = router.urls
