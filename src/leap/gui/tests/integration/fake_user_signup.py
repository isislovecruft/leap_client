"""
simple server to test registration and
authentication

To test:

curl -d login=python_test_user -d password_salt=54321\
     -d password_verifier=12341234 \
        http://localhost:8000/users.json

"""
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import json
import urlparse

HOST = "localhost"
PORT = 8000

LOGIN_ERROR = """{"errors":{"login":["has already been taken"]}}"""

from leap.base.tests.test_providers import EXPECTED_DEFAULT_CONFIG


class request_handler(BaseHTTPRequestHandler):
    responses = {
        '/': ['ok\n'],
        '/users.json': ['ok\n'],
        '/timeout': ['ok\n'],
        '/provider.json': ['%s\n' % json.dumps(EXPECTED_DEFAULT_CONFIG)]
    }

    def do_GET(self):
        path = urlparse.urlparse(self.path)
        message = '\n'.join(
            self.responses.get(
                path.path, None))
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message)

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        data = dict(
            (key, form[key].value) for key in form.keys())
        path = urlparse.urlparse(self.path)
        message = '\n'.join(
            self.responses.get(
                path.path, ''))

        login = data.get('login', None)
        #password_salt = data.get('password_salt', None)
        #password_verifier = data.get('password_verifier', None)

        if path.geturl() == "/timeout":
            print 'timeout'
            self.send_response(200)
            self.end_headers()
            self.wfile.write(message)
            import time
            time.sleep(10)
            return

        ok = True if (login == "python_test_user") else False
        if ok:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(message)

        else:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(LOGIN_ERROR)


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), request_handler)
    server.serve_forever()
