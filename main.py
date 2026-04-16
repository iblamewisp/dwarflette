from pprint import pprint
import uvicorn
async def app(scope, receive, send):
	assert scope['type'] == 'http'
	request = Request(scope, receive)
	if request.path == '/test':
		await Response('Hello, world!', 200, 'text/plain')(scope, receive, send)
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
		
if __name__ == '__main__':
	uvicorn.run('main:app', port=1488, log_level='info')
