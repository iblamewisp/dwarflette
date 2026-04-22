class Route:
	def __init__(self, path, endpoint, methods):
		self.path = path
		self.endpoint = endpoint
		self.methods = {m.upper() for m in methods}

	def match(self, scope):
		request_path = scope['path'].split('/')
		route_path = self.path.split('/')
		if len(request_path) != len(route_path): return 
		params = {}
		for rp, ap in zip(route_path, request_path):
			if '{' in rp:
				params[rp[1:-1]] = ap
			elif rp != ap:
				return 

	async def handle(self, scope, receive, send, params):
		request = Request(scope, receive, params)
		await Response(content=await self.endpoint(request), status=200)(scope, receive, send)

class Lifespan:
    def __init__(self, context_manager):
        self.context_manager = context_manager

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'lifespan':
            return
        
        async with self.context_manager:
            message = await receive()
            assert message['type'] == 'lifespan.startup'
            await send({'type': 'lifespan.startup.complete'})

            message = await receive()
            assert message['type'] == 'lifespan.shutdown'
        
        await send({'type': 'lifespan.shutdown.complete'})


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
	def get(self, path):return self.route(path, ['GET'])
	def post(self, path):return self.route(path, ['POST'])
	async def __call__(self, scope, receive, send):
		for route in self.routes:
			params = route.match(scope)
			if params is not None:
				await route.handle(scope, receive, send, params)
		await Response('Not Found', status=404)(scope, receive, send)
		
class Request:
	def __init__(self, scope, receive, params):
		self._scope = scope
		self._receive = receive
		self.params = params
		print(self.params)
	@property
	def method(self): return self._scope['method']
	@property
	def path(self): return self._scope['path']

class Response:
	def __init__(self, content=None, status=200, content_type="text/plain", headers=None):
		self.status = status
		self.headers = headers or {}
		self.content_type = content_type
		if content:
			self.content = content.encode('utf-8')
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
			'body':	self.content,
		})
		
