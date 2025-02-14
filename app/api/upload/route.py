from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import cgi
import sys
import os

# Add parent directory to path to import process_car
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from process_car import process_car_data

class ImageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Get content length
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            # Parse JSON data
            data = json.loads(post_data)
            
            # Process the car data
            result = process_car_data(
                image_data=data.get('image', ''),
                car_info=data.get('carInfo', {})
            )
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            # Send error response
            error_response = {
                'status': 'error',
                'message': str(e)
            }
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode())

def run(server_class=HTTPServer, handler_class=ImageHandler, port=3001):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()