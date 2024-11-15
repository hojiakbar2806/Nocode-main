from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import re
import bcrypt
from urllib.parse import parse_qs
from sqlalchemy.exc import IntegrityError
from models import User
from database import SessionLocal, init_db

class UserHandler(BaseHTTPRequestHandler):
    def _send_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _validate_password(self, password):
        if len(password) < 8:
            return False, "Parol kamida 8 ta belgidan iborat bo'lishi kerak"
        if not re.search(r"[A-Z]", password):
            return False, "Parol kamida 1 ta katta harf bo'lishi kerak"
        if not re.search(r"[a-z]", password):
            return False, "Parol kamida 1 ta kichik harf bo'lishi kerak"
        if not re.search(r"\d", password):
            return False, "Parol kamida 1 ta raqam bo'lishi kerak"
        return True, ""

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        post_body = parse_qs(post_data.decode())
        
        if self.path == '/api/register':
            try:
                fullname = post_body.get('fullname', [''])[0]
                username = post_body.get('username', [''])[0]
                password = post_body.get('password', [''])[0]
                
                if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
                    self._send_response(400, {
                        'success': False,
                        'error': "Noto'g'ri foydalanuvchi nomi. Foydalanuvchi nomi 3 dan 20 gacha belgidan iborat bo'lishi va faqat harflar, raqamlar va pastki chiziqdan iborat bo'lishi kerak."
                    })
                    return

               
                is_valid, error_message = self._validate_password(password)
                if not is_valid:
                    self._send_response(400, {
                        'success': False,
                        'error': error_message
                    })
                    return
                
              
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                
                db = SessionLocal()
                new_user = User(
                    fullname=fullname, 
                    username=username,
                    password_hash=password_hash.decode('utf-8')
                )
                db.add(new_user)
                db.commit()
                user_id = new_user.id
                db.close()
                
                self._send_response(201, {
                    'success': True,
                    'user_id': user_id
                })
                
            except IntegrityError:
                if 'db' in locals():
                    db.rollback()
                self._send_response(400, {
                    'success': False,
                    'error': "Bu foydalanuvchi nomi band."
                })
            except Exception as e:
                if 'db' in locals():
                    db.rollback()
                self._send_response(500, {
                    'success': False,
                    'error': str(e)
                })
            finally:
                if 'db' in locals():
                    db.close()
                
        elif self.path == '/api/login':
            try:
                username = post_body.get('username', [''])[0]
                password = post_body.get('password', [''])[0]
                
                db = SessionLocal()
                user = db.query(User).filter(User.username == username).first()
                
                if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                    self._send_response(200, {
                        'success': True,
                        'user_id': user.id
                    })
                else:
                    self._send_response(401, {
                        'success': False,
                        'error': "Noto'g'ri foydalanuvchi nomi yoki parol."
                    })
                    
            except Exception as e:
                if 'db' in locals():
                    db.rollback()
                self._send_response(500, {
                    'success': False,
                    'error': str(e)
                })
            finally:
                if 'db' in locals():
                    db.close()
        
        else:
            self._send_response(404, {
                'success': False,
                'error': 'Not Found'
            })

def run_server(port=8000):
    init_db()
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, UserHandler)
    print(f"Server running on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()