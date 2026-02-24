import os
import sys
import webbrowser
import subprocess

def resource_path(relative_path):
    """PyInstaller exe 내부와 일반 실행 환경 모두 대응"""
    try:
        base_path = sys._MEIPASS  # exe 내부
    except AttributeError:
        base_path = os.path.abspath(".")  # 일반 실행
    return os.path.join(base_path, relative_path)

def open_in_chrome(html_file_path):
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Users\{}\\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.getlogin())
    ]
    chrome_path = next((p for p in chrome_paths if os.path.exists(p)), None)
    if chrome_path is None:
        webbrowser.open(html_file_path)
        return
    subprocess.Popen([chrome_path, html_file_path])

if __name__ == "__main__":
    html_file = resource_path("index.html")
    if not os.path.exists(html_file):
        print("index.html 파일이 없습니다!", html_file)
        sys.exit(1)
    html_file_url = f"file:///{html_file.replace(os.sep, '/')}"
    print("브라우저에서 열 URL:", html_file_url)
    open_in_chrome(html_file_url)
    print("브라우저에서 index.html 실행 완료")
