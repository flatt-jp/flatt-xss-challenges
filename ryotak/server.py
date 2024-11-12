from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from uuid import uuid4
import urllib.parse as urlparse
import html
import os

index_html = open("index.html").read()
drafts = {}

class RequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    content_type_text = 'text/plain; charset=utf-8'
    content_type_html = 'text/html; charset=utf-8'

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        path = parsed_path.path
        query = urlparse.parse_qs(parsed_path.query)
        if path == "/":
            self.send_response(200)
            self.send_header('Cache-Control', 'max-age=3600')
            self.send_data(self.content_type_html, bytes(index_html, 'utf-8'))
        elif path == "/api/drafts":
            draft_id = query.get('id', [''])[0]
            if draft_id in drafts:
                escaped = html.escape(drafts[draft_id])
                self.send_response(200)
                self.send_data(self.content_type_text, bytes(escaped, 'utf-8'))
            else:
                self.send_response(200)
                self.send_data(self.content_type_text, b'')
        else:
            self.send_response(404)
            self.send_data(self.content_type_text, bytes('Path %s not found' % self.path, 'utf-8'))

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length'))
        if content_length > 100:
            self.send_response(413)
            self.send_data(self.content_type_text, b'Post is too large')
            return
        body = self.rfile.read(content_length)
        draft_id = str(uuid4())
        drafts[draft_id] = body.decode('utf-8')
        self.send_response(200)
        self.send_data(self.content_type_text, bytes(draft_id, 'utf-8'))

    def send_data(self, content_type, body):
        self.send_header('Content-Type', content_type)
        self.send_header('Connection', 'keep-alive')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

port = int(os.environ.get("PORT", 3002))
with ThreadingHTTPServer(("0.0.0.0", port), RequestHandler) as server:
    print("Listening on port %d" % port)
    server.serve_forever()
