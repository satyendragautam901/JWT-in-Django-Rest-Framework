from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import StudentViewset

router = DefaultRouter()

router.register('student',StudentViewset,basename='basicauth')

urlpatterns = router.urls