from rest_framework.routers import DefaultRouter
from flavaudio import views

router = DefaultRouter()
router.register('', views.AudioViewSet, basename='audio')

urlpatterns = [

] + router.urls
