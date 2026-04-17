import asyncio
import uvicorn

class Route:
	def __init__(self, path, endpoint, methods):
		self.path = path
		self.endpoint = endpoint
		self.methods = {m.upper for m in methods}
	
	async def handle(self, scope, receive, send):
		request = Request(scope, receive)
		await Response(await self.endpoint(request))(scope, receive, send)


class Router:
	def __init__(self, routes=None):
		self.routes = routes or []
	def add_route(self, path, endpoint, methods):
		self.routes.append(Route(path, endpoint, methods))
	def route(self, path, methods=['GET']):
		def decorator(func):
			self.add_route(path, func, methods)
			return func
		return decorator
	def get(self, path):
		return self.route(path, ['GET'])
	def post(self, path):
		return self.route(path, ['POST'])
		
		
	async def __call__(self, scope, receive, send):
		for route in self.routes:
			if scope['path'] == route.path:
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
		
