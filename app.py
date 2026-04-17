import uvicorn
from main import Router

router = Router()
users = ['Test1', 'Test2']
@router.get('/test/{user_id}')
async def test(request):
	user_id = request.params['user_id']
	return users[int(user_id)]
@router.get('/test/{user_id}/par')
async def test_test(request):
	user_id = request.params['user_id']
	return f'hello, idi nahui from {user_id}' 
async def app(scope, receive, send):
	await router(scope, receive, send)
	

if __name__ == "__main__":
	uvicorn.run("app:app", port=1489)
