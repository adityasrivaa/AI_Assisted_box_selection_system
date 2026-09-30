from django.urls import include, path
from rest_framework.routers import DefaultRouter

from box_selection.views import (
    BoxViewSet,
    OrderViewSet,
    ProductViewSet,
    RecommendedBoxView,
)


router = DefaultRouter()

router.register(
    "products",
    ProductViewSet,
    basename="product",
)

router.register(
    "boxes",
    BoxViewSet,
    basename="box",
)

router.register(
    "orders",
    OrderViewSet,
    basename="order",
)


urlpatterns = [
    path(
        "",
        include(router.urls),
    ),
    path(
        "orders/<int:order_id>/recommended-box/",
        RecommendedBoxView.as_view(),
        name="recommended-box",
    ),
]