from rest_framework import serializers
from rest_framework.parsers import MultiPartParser

from sanaa.models import CustomerImage

__author__ = 'Nestor Velazquez'


class CustomerImageSerializer(serializers.HyperlinkedModelSerializer):
    """
    """
    parser_classes = (MultiPartParser, )

    url = serializers.HyperlinkedIdentityField(view_name='document-detail')
    anfexi = serializers.CharField(max_length=12, write_only=True)

    def create(self, validated_data):
        customer_image = CustomerImage.objects.create_customer_image(
            validated_data['document'],
            validated_data['anfexi']
        )
        if customer_image is not None:
            return customer_image

    class Meta:
        model = CustomerImage
        fields = (
            'url', 'anfexi', 'document', 'thumbnail'
        )
        read_only_fields = (
            'url', 'thumbnail'
        )
