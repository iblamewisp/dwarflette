import uvicorn
import asyncio
from main import Router, path

router = Router()

@path('/test', ['GET'], router)
async def test(request):
	return 'hello, world'

async def app(scope, receive, send):
	asyncio.create_task(test('hi'))
	await router(scope, receive, send)


if __name__ == "__main__":
	uvicorn.run("app:app", port=1488)
