# asyncioのStreams
# https://docs.python.org/ja/3.6/library/asyncio-stream.html
import asyncio
import collections

# 今回はhandle_echo関数を書き換える
class CountServer(object):
    def __init__(self):
        self.counter = collections.Counter()
        self.lock = asyncio.Lock()
    
    async def handle_echo(self, reader, writer):
        data = await reader.read()  # クライアントからのデータ待ち
        name = data.decode()

        with await self.lock:
            if self.counter[name] > 10:
                writer.write(b'-1')
                self.counter[name] = 0
            else:
                writer.write(str(self.counter[name]).encode())
                self.counter[name] += 1
            await writer.drain()
            writer.close()

loop = asyncio.get_event_loop()
count_server = CountServer()
coro = asyncio.start_server(
    count_server.handle_echo, '127.0.0.1', 8888, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
