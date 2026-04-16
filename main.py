async def app(scope, receive, send):
    assert scope["type"] == "http"

    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [
            (b"content-type", b"text/plain"),
            (b"content-length", b"12"),
        ],
    })
    await send({
        "type": "http.response.body",
        "body": b"Hello world!",
        "more_body": False,
    })

print('hello goyda')