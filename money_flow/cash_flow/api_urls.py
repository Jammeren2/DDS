from rest_framework.routers import DefaultRouter
from .api import (
    StatusViewSet, TypeViewSet, CategoryViewSet,
    SubcategoryViewSet, CashFlowViewSet
)

router = DefaultRouter()
router.register(r'statuses', StatusViewSet)
router.register(r'types', TypeViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'cashflows', CashFlowViewSet)

urlpatterns = router.urls
