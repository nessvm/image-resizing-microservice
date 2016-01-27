from rest_framework import routers

from aden.views import CustomerImageViewSet

__author__ = 'Nestor Velazquez'


router = routers.DefaultRouter()
router.register(r'documents', CustomerImageViewSet, base_name='document')
urlpatterns = router.urls
