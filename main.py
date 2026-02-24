import http.server
import socketserver
import threading
import webbrowser
import os
import sys
import socket
import time

# -----------------------------
# PyInstaller 경로 대응
# -----------------------------
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# -----------------------------
# 로그 완전 차단 핸들러
# -----------------------------
class SilentHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return  # 로그 출력 완전 차단

# -----------------------------
# 서버 클래스 (포트 재사용 가능)
# -----------------------------
class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

# -----------------------------
# 사용 가능한 포트 자동 탐색
# -----------------------------
def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]

# -----------------------------
# 서버 시작
# -----------------------------
def start_server(port, directory):
    os.chdir(directory)

    with ThreadingTCPServer(("127.0.0.1", port), SilentHandler) as httpd:
        httpd.serve_forever()

# -----------------------------
# 메인 실행
# -----------------------------
if __name__ == "__main__":

    html_path = resource_path("index.html")

    if not os.path.exists(html_path):
        print("❌ index.html 파일이 없습니다.")
        print("현재 경로:", html_path)
        sys.exit(1)

    base_dir = os.path.dirname(html_path)
    port = find_free_port()

    server_thread = threading.Thread(
        target=start_server,
        args=(port, base_dir),
        daemon=True
    )
    server_thread.start()

    time.sleep(1)

    url = f"http://127.0.0.1:{port}/index.html"
    webbrowser.open(url)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
