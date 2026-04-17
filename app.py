import uvicorn
from main import Router, Lifespan

router = Router()
users = ['Test1', 'Test2']

settings = 'чтото'

#examples of handling connections & disconnections
async def connect_to_something(settings): 
	print('first connection')
async def connect_to_second_thing(settings): 
	print('second connection')
async def disconnect1():
	print('disconnected1')
async def disconnect2():
	print('disconnected2')

lifespan = Lifespan(
    startup=(lambda: connect_to_something(settings),
        	 lambda: connect_to_second_thing(settings)
			),
    shutdown=(disconnect1, disconnect2)
)

@router.get('/test/{user_id}')
async def test(request):
	user_id = request.params['user_id']
	return users[int(user_id)]
@router.get('/test/{user_id}/par')
async def test_test(request):
	user_id = request.params['user_id']
	return f'hello, idi nahui from {user_id}' 
@router.post('/add_test/{user_id}')
async def test_test_test(request):
	users.append(request.params['user_id'])

async def app(scope, receive, send):
	await lifespan(scope, receive, send)
	await router(scope, receive, send)
	

if __name__ == "__main__":
	uvicorn.run("app:app", port=1489)
