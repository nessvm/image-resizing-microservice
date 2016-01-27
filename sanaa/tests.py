from django.test import TestCase
from django.core.files.storage import default_storage
from PIL import Image

from sanaa.models import CustomerImage

__author__ = 'Nestor Velazquez'


class ImageProcessingTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._front_sample_fp = default_storage.open('front-sample.png', 'rb+')
        cls._back_sample_fp = default_storage.open('back-sample.png', 'rb+')
        cls._oversized_jpg_fp = default_storage.open(
            'front-sample-oversize.jpg', 'rb+'
        )

    @classmethod
    def tearDownClass(cls):
        cls._front_sample_fp.close()
        cls._back_sample_fp.close()
        cls._oversized_jpg_fp.close()

    def test_front_thumbnail(self):
        customer_image = CustomerImage.objects.create_customer_image(
            fp=self._front_sample_fp, anfexi='123456'
        )
        # Assertions
        self.assertIsNotNone(
            customer_image.thumbnail, msg='Model object creation returns None'
        )

    def test_thumbnail_size(self):
        customer_image = CustomerImage.objects.create_customer_image(
            fp=self._front_sample_fp, anfexi='123456'
        )
        self.assertLessEqual(
            customer_image.thumbnail.height, 128,
            msg='Thumbnail has an incorrect size'
        )
        self.assertLessEqual(
            customer_image.thumbnail.width, 128,
            msg='Thumbnail has an incorrect size'
        )

    def test_jpeg(self):
        fp = default_storage.open('front-sample-oversize.jpg')
        try:
            CustomerImage.objects.create_customer_image(fp, anfexi='123456')
        except OSError:
            self.fail('JPEG decoders not found')

    def test_tiff(self):
        fp = default_storage.open('front-sample.tiff')
        try:
            CustomerImage.objects.create_customer_image(fp, anfexi='123456')
        except OSError:
            self.fail('TIFF decoders not found')

    def test_gif(self):
        fp = default_storage.open('front-sample.gif')
        try:
            CustomerImage.objects.create_customer_image(fp, anfexi='123456')
        except OSError:
            self.fail('GIF decoders not found')

    def test_bmp(self):
        fp = default_storage.open('front-sample.bmp')
        try:
            CustomerImage.objects.create_customer_image(fp, anfexi='123456')
        except OSError:
            self.fail('BMP decoders not found')
