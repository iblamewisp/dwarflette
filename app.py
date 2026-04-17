import uvicorn
import asyncio
from main import Router

router = Router()

@router.get('/test')
async def test(request):
	return 'hello, world'

async def app(scope, receive, send):
	await router(scope, receive, send)
	

if __name__ == "__main__":
	uvicorn.run("app:app", port=1488)
