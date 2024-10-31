import asyncio
from server import WebSocketServer

async def main():
    server = WebSocketServer()
    server_task = asyncio.create_task(server.start())
    od_user = server.get_received_data()

    do_user = [0, 0, 0, 0]
    await server.wyslij(do_user)


if __name__ == "__main__":
    asyncio.run(main())
