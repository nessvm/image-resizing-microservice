from django.test import TestCase, RequestFactory
from django.core.files.storage import default_storage
from rest_framework.test import APIClient
from rest_framework.renderers import MultiPartRenderer
from rest_framework import status
from PIL import Image
from sanaa.models import CustomerImage

__author__ = 'Nestor Velazquez'


class CustomerImageEndpointTests(TestCase):
    def setUp(self):
        self._client = APIClient()
        self._factory = RequestFactory()

    def test_bad_request(self):
        response = self._client.post('/documents/')

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            msg='Expected {}, got {} instead'.format(
                status.HTTP_400_BAD_REQUEST, response.status_code
            )
        )

    def test_created(self):
        fp = default_storage.open('back-sample.png')
        data = {'document': fp, 'anfexi': '1234567'}
        response = self._client.post(
            '/documents/', data=data, format='multipart'
        )
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED,
            msg='Expected {}, got {} instead'.format(
                status.HTTP_201_CREATED, response.status_code
            )
        )

    def test_retrieve(self):
        file = default_storage.open('front-sample.png')
        customer_image = CustomerImage.objects.create_customer_image(
            file, anfexi='7655'
        )
        response = self._client.get('/documents/{}/'.format(customer_image.pk))
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg='Customer image retrieval failed'
            )
