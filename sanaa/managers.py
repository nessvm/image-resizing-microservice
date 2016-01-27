from multiprocessing import Process, Pipe

from PIL import Image
from django.core.files.images import ImageFile
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db import models

__author__ = 'Nestor Velazquez'


class CustomerImageManager(models.Manager):
    """docstring for CustomerImageManager"""
    def __init__(self):
        self.customer_image = None
        super(CustomerImageManager, self).__init__()

    def create_customer_image(self, fp, anfexi):
        self.customer_image = self.create()
        # Process image (if the uploaded file has an image format)
        try:
            image = Image.open(fp)
        except IOError:
            # An IOError here means the file is not a recognized image format
            generic_file = TemporaryUploadedFile()
            extension = self._get_extension(fp)
            # Store the file as is and don't create a thumbnail
            self.customer_image.document.save(
                '{}-full.{}'.format(
                    anfexi, extension
                ),
                ImageFile(generic_file)
            )
            generic_file.close()
            return self.customer_image

        # Otherwise process images normally
        thumbnail, resize = self._process_image(image)
        # Write images on S3
        thumbnail_file = self._make_temp_file(thumbnail.getvalue())
        image_file = self._make_temp_file(resize.getvalue())
        self.customer_image.thumbnail.save(
            '{}-thumbnail.png'.format(anfexi),
            ImageFile(thumbnail_file), save=False
        )
        thumbnail_file.close()
        self.customer_image.document.save(
            '{}-full.png'.format(anfexi),
            ImageFile(image_file), save=False
        )
        self.customer_image.save()
        image_file.close()
        return self.customer_image

    def _make_temp_file(self, contents):
        from tempfile import TemporaryFile
        file = TemporaryFile()
        file.write(contents)
        return file

    def _process_image(self, image):
        # Create pipes for process communication
        std_size_pipe, std_size_child_end = Pipe()
        thumb_pipe, thumb_child_end = Pipe()
        # Create the threads
        threads = [
            Process(
                target=self._thumbnail,
                args=(image, thumb_child_end, (128, 128))
            ),
            Process(
                target=self._thumbnail,
                args=(image, std_size_child_end, (1920, 1080))
            )
        ]
        # Start threads
        for thread in threads:
            thread.start()
        # Get processed images content and close threads
        images_bytes = (
            thumb_pipe.recv(), std_size_pipe.recv()
        )
        for thread in threads:
            thread.join()

        for obj in images_bytes:
            if type(obj) is IOError:
                raise obj

        return images_bytes

    def _thumbnail(self, image, conn, size):
        try:
            im = image.copy()
            im.thumbnail(size)
            from django.utils.six import BytesIO
            b = BytesIO()
            im.save(b, 'PNG')
            conn.send(b)
        except IOError as e:
            conn.send(e)
        finally:
            conn.close()

    def _get_extension(self, fp):
        index = fp.name.rfind('.') + 1
        return fp.name[-index:]
