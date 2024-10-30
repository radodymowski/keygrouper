from django.urls import path, include
from rest_framework.routers import DefaultRouter

from names.views import NameGroupViewSet, NameEntityMoveView

router = DefaultRouter()
router.register(r"", NameGroupViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("<int:pk>/move/", NameEntityMoveView.as_view(), name="nameentity-move")
]
