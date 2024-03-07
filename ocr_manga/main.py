import logging
import aiohttp_cors
import zipfile

from aiohttp import web
from handler import route_handler
from includes.utils import *
from config import *

from PIL import Image
from io import BytesIO

LOGGER = logging.getLogger(__name__)

app = web.Application(client_max_size=Config.CLIENT_MAX_SIZE)

handler = route_handler.RouteHandler()

# app.router.add_post('/v1/translate', handler.translate)
async def translate_and_download(request):
    data = await request.json()
    file_paths = handler.translate(data['url'], data['lang'], data['ocr'], data['srclang'])
    image_data_list = []
    for path in file_paths:
        try:
        # Assuming paths point to valid image files
            with open(path, 'rb') as f:
                image_data_list.append(f.read())
        except FileNotFoundError:
            print(f"Error: File not found: {path}")
    # return success({"status": 200, "translated_list": translated_list})
    zip_buffer = BytesIO()

    # Create a zipfile object
    with zipfile.ZipFile(zip_buffer, mode="w") as zip_file:
        for i, image_bytes in enumerate(image_data_list):
            # Create filename with extension based on assumed format
            filename = f"translated_image_{i}"
            # Add image data to zip file with filename
            zip_file.writestr(filename, image_bytes)

    # Set response headers
        # Create an aiohttp response object
    response = web.Response(
        body=zip_buffer.getvalue(),
        status=200,
        content_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=translated_images.zip"},
    )

    return response

app.add_routes([web.post('/v1/translate', translate_and_download)])


cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})


for route in list(app.router.routes()):

    if not isinstance(route.resource, web.StaticResource):  # <<< WORKAROUND
        cors.add(route)

web.run_app(app, host=Config.HOST , port=Config.PORT)
