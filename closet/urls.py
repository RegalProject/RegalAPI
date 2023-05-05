from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('ownedItem', views.OwnedItemViewSet, 'ownedItem')
router.register('ownedItemByPK', views.OwnedItemByPKViewSet, 'ownedItemByPK')
router.register('publicItem', views.PublicItemViewSet, 'publicItem')
router.register('crawledItem', views.CrawledItemViewSet, 'crawledItem')
router.register('recommendedItem', views.RecommendedItemViewSet, 'recommendedItem')
router.register('recommendedItemByPK', views.RecommendedItemByPKViewSet, 'recommendedItemByPK')
router.register('wishlist', views.WishlistViewSet, 'wishlist')
router.register('wishlistByPK', views.WishlistByPKViewSet, 'wishlistByPK')
router.register('addByLink', views.AddByLinkViewSet, 'addByLink')

urlpatterns = router.urls
