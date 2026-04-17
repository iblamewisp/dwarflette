import uvicorn
import asyncio
from main import Router, route

router = Router()

@route('/test', ['GET'], router)
async def test(request):
	return 'hello, world'

async def app(scope, receive, send):
	await router(scope, receive, send)
	

if __name__ == "__main__":
	uvicorn.run("app:app", port=1488)
