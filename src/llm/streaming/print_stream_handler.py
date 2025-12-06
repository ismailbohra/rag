from .base_stream_handler import BaseStreamHandler

class PrintStreamHandler(BaseStreamHandler):
    def __init__(self):
        self.buffer = []

    def on_data(self, chunk):
        # chunk may contain text delta; adapt to API
        delta = getattr(chunk, "text", str(chunk))
        print(delta, end="", flush=True)
        self.buffer.append(delta)

    def get_result(self):
        return "".join(self.buffer)
