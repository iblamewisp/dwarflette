import asyncio
import uvicorn

class Route:
	def __init__(self, path, endpoint, methods):
		_, self.path, self.path_params = path.split('/', 3)
		self.endpoint = endpoint
		self.methods = {m.upper for m in methods}
	
	async def handle(self, scope, receive, send):
		params = {self.path_params.replace('{', "").replace('}', ""):scope['path'].split('/', 3)[-1]}
		request = Request(scope, receive, params)
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
			path = scope['path'].split('/', 3)[1:]
			route_path = [route.path, route.path_params]
			print(path, route_path)
			if len(path) == len(route_path) and path[0] == route_path[0]:
				await route.handle(scope, receive, send)
		
	
class Request:
	def __init__(self, scope, receive, path_params):
		self._scope = scope
		self._receive = receive
		self.path_params = path_params or {}
		print(self.path_params)
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
		
