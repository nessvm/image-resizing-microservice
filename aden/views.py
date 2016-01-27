from rest_framework import viewsets, mixins

from aden.serializers import *

__author__ = 'nvelazquez'


class CustomerImageViewSet(viewsets.GenericViewSet,
                           mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    queryset = CustomerImage.objects.all()
    serializer_class = CustomerImageSerializer
    parser_classes = (MultiPartParser, )

    def create(self, request, *args, **kwargs):
        response = super(CustomerImageViewSet, self).create(
            request, *args, **kwargs
        )
        response.data['document'] = _trim_img_path(response.data['document'])
        response.data['thumbnail'] = _trim_img_path(response.data['thumbnail'])

        return response


def _trim_img_path(path):
    if path is None:
        return
    index = path.find("?")
    return path[:index]
