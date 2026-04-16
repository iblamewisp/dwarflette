from pprint import pprint
import asyncio
import uvicorn

def route(url, method, router):
	def decorator(func):
		route = Route(url, func, method)
		print(route.path)
		router.routes.append(route)
		async def wrapper(*args, **kwargs):
			return await func(*args, **kwargs)
		return wrapper 
	return decorator

class Route:
	def __init__(self, path, endpoint, methods):
		self.path = path
		self.endpoint = endpoint
		self.methods = methods
	async def handle(self, scope, receive, send):
		request = Request(scope, receive)
		await Response(await self.endpoint(request))(scope, receive, send)

class Router:
	def __init__(self, routes=None):
		self.routes = routes or []

	async def __call__(self, scope, receive, send):
		for route in self.routes:
			print(route.path)
			print(scope['path'])
			# if scope['path'] == route.path убрал нахуй
			# он в 10 из 10 случаев не работал нахуй
			await route.handle(scope, receive, send)
			
class Request:
	def __init__(self, scope, receive):
		self._scope = scope
		self._receive = receive
	
	@property
	def method(self):
		return self._scope['method']
	
	@property
	def path(self):
		return self._scope['path']

class Response:
	def __init__(self, content=None, status=200, content_type="text/plain", headers=None):
		self.status = status
		self.headers = headers or {}
		self.content_type = content_type
		if content:
			self.content = content
		else:
			self.content = b""
	async def __call__(self, scope, receive, send):
		await send({
			'type': 'http.response.start',
			'status': self.status,
			'headers': [
				(b'content-type', self.content_type.encode()),
			]
			}
		)
		await send({
			'type': 'http.response.body',
			'body':	self.content.encode('utf-8'),
		})
		
