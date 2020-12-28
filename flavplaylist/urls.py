from rest_framework.routers import DefaultRouter
from flavplaylist import views

router = DefaultRouter()
router.register('', views.PlayListViewSet, basename="playlist")


urlpatterns = [

] + router.urls
