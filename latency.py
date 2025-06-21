import falcon.asgi
import mimetypes
import uvicorn
from pathlib import Path


image_path = Path("assets/5x5.png")


class Image:
    __slots__ = ("image_data", "content_type")

    def __init__(self, image_data: bytes, content_type: str):
        self.image_data = image_data
        self.content_type = content_type

    async def on_get(self, req: falcon.Request, resp: falcon.Response, path: str):
        # Optional parameter to disable the Timing-Allow-Origin header
        # This can be used to test the behavior of the browser when the header is not present
        disabled = req.get_param_as_bool("disabled", blank_as_true=False)
        if not disabled:
            resp.set_header("Timing-Allow-Origin", "*")

        resp.data = self.image_data
        resp.content_type = self.content_type


def load_image(filepath: Path) -> bytes:
    return filepath.read_bytes()


if __name__ == "__main__":
    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    image_data = load_image(image_path)

    app = falcon.asgi.App()
    app.add_route("/{path}", Image(image_data, mimetypes.guess_type(image_path)[0]))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="warning",
        server_header=False,
        date_header=False,
    )
