import time


def application(environ, start_response):
    headers = [
        ('Content-Type', 'text/event-stream'),
        ('Cache-Control', 'no-cache'),
    ]
    start_response('200 OK', headers)

    def event_stream():
        messages = [f"data: Message {i}\n\n" for i in range(1, 6)]
        for message in messages:
            for char in message:
                yield char.encode('utf-8')  # 每次發送一個字
                time.sleep(0.1)  # 每個字之間間隔 0.1 秒
        yield b"data: END\n\n"  # 最後結束訊息

    return event_stream()


if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    server = make_server('localhost', 8000, application)
    print("WSGI Streaming Server running at http://localhost:8000")
    server.serve_forever()
