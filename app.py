import uvicorn
from main import Router, path
router = Router()

async def app(scope, receive, send):
	await router(scope, receive, send)
@path('test', ['GET'], router)
async def test(request):
	return 'hello, world'
if __name__ == "__main__":
	uvicorn.run("app:app", port=1488)
