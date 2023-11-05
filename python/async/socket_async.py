import socket
import enum
import select

class WaitEvent(enum.Enum):
    IN = 0
    OUT = 1

class Awaitable:
    def __init__(self, fd: int , evt: WaitEvent) -> None:
        self.evt = evt
        self.fd = fd

    def __await__(self) -> tuple[WaitEvent, int]:
        yield self.evt, self.fd

class AsyncSocket:
    def __init__(self, fd):
        self.fd = fd

    async def accept(self):
        await Awaitable(self.fd, WaitEvent.IN)
        return self.fd.accept()

    async def recv(self, length):
        await Awaitable(self.fd, WaitEvent.IN)
        return self.fd.recv(length)

    async def send(self, data):
        if isinstance(data, str):
            data = data.encode()
        await Awaitable(self.fd, WaitEvent.OUT)
        return self.fd.send(data)

    def close(self):
        self.fd.close()


class EventLoop:
    def __init__(self):
        self.coros = []
        self.reads = {}
        self.writes = {}

    def add_coroutine(self, coro):
        self.coros.append(coro)

    def select(self):
        rs, ws, _ = select.select(self.reads, self.writes, [])
        for r in rs:
            self.add_coroutine(self.reads.pop(r))
        for w in ws:
            self.add_coroutine(self.writes.pop(w))

    def handle_event(self, coro, evt, fd):
        if evt == WaitEvent.IN:
            self.reads[fd] = coro
        elif evt == WaitEvent.OUT:
            self.writes[fd] = coro
        else:
            pass

    def run(self):
        while any((self.coros, self.reads, self.writes)):
            while not self.coros:
                self.select()
            cur_coro = self.coros.pop(0)
            try:
                evt, fd = cur_coro.send(None)
            except StopIteration:
                continue
            self.handle_event(cur_coro, evt, fd)


async def server(ev_loop : EventLoop, host :str, port: int):
    svr_fd = socket.socket()
    svr_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    svr_fd.bind((host, port,))
    svr_fd.listen(5)
    svr_fd = AsyncSocket(svr_fd)
    while True:
        client, client_address = await svr_fd.accept()
        client = AsyncSocket(client)
        await client.send('@ connect\n'.encode())
        ev_loop.add_coroutine(handler(client))


async def handler(client):
    while True:
        req = await client.recv(100)  # size of bytes chuck
        if not req:
            await client.send('@ close connection\n'.encode())
            client.close()
            return

        try:
            value = int(req)
        except ValueError:
            await client.send('@ enter integer\n'.encode())
            client.close()
            return

        resp = value * 2
        await client.send(f'> {resp}\n'.encode())


if __name__ == '__main__':
    ev_loop = EventLoop()
    ev_loop.add_coroutine(server(ev_loop, 'localhost', 30303))
    ev_loop.run()