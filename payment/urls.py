from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('Transaction', views.TransactionViewSet, 'Transaction')
# router.register('Info', views.InfoViewSet, 'Info')

urlpatterns = router.urls