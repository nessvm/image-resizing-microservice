# Image resizing microservice
## Invoking
To create a new image/thumbnail entry in the database, make a POST request to 
/documents/ with a multipart Content-Type in the request header. The service 
takes a single argument that should be called 'image' in case the request is 
form encoded.

To retrieve an image package object given its id make a GET request to 
/documents/\<id\>/.

### Response
A successful POST request will yield an HTTP response with status code 201 and
the *Location* link in the response header.

A successful GET request will result in an HTTP response with status code 200
and the image-package representation in the body.

## Decoder Support
Decoder support relies entirely on the packages available in the host machine, 
the image processing libraries used in the service uses Python's Pillow module.