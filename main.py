import asyncio
from connection import WebSocketServer

server = None  # Zmienna globalna

async def all():
    global server
    od_user = server.get_received_data()

    # Sprawdź, czy odebrane dane istnieją i wypisz je
    if od_user is not None:
        print("Odebrane dane:", od_user)

    do_user = [0, 0, 0, 0]
    await server.wyslij(do_user)

async def main():
    global server
    server = WebSocketServer()

    # Uruchamiamy serwer jako zadanie asynchroniczne
    server_task = asyncio.create_task(server.start())

    # Uruchamiamy `all` w pętli z odstępem czasowym
    while True:
        await all()
        await asyncio.sleep(1)  # Odstęp 1 sekundy

if __name__ == "__main__":
    asyncio.run(main())
