import time


def application(environ, start_response):
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']

    # CORS 標頭
    cors_headers = [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'POST, OPTIONS'),
        ('Access-Control-Allow-Headers', 'Content-Type')
    ]

    # 處理 OPTIONS 預檢請求 (CORS 需求)
    if method == 'OPTIONS':
        start_response('200 OK', cors_headers)
        return [b""]

    if method == 'POST' and path == '/echo':
        try:
            # 讀取請求內容
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            body = "已收到你的回覆: " + \
                environ['wsgi.input'].read(content_length).decode('utf-8')

            # 設定 Streaming 回應標頭
            headers = [
                ('Content-Type', 'text/event-stream'),
                ('Cache-Control', 'no-cache')
            ] + cors_headers  # 加上 CORS 標頭

            start_response('200 OK', headers)

            # 逐字發送輸入的內容
            def event_stream():
                for char in body:
                    yield f"{char}".encode('utf-8')
                    time.sleep(0.1)  # 模擬逐字顯示效果
                yield b"\n<END/>"  # 結束標記

            return event_stream()

        except Exception as e:
            start_response('500 Internal Server Error', [
                           ('Content-Type', 'text/plain')] + cors_headers)
            return [str(e).encode('utf-8')]

    else:
        start_response('404 Not Found', [
                       ('Content-Type', 'text/plain')] + cors_headers)
        return [b"404 Not Found"]


if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    server = make_server('localhost', 8000, application)
    print("WSGI Streaming Server running at http://localhost:8000/echo")
    server.serve_forever()
