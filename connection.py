import asyncio
import websockets
import json

class WebSocket:
    def __init__(self, host="0.0.0.0", port=8765):
        self.host = host
        self.port = port
        self.websocket = None
        self.received_data = None  # Zmienna do przechowywania odebranych danych

    async def start(self):
        # Używamy `async with` dla serwera WebSocket
        async with websockets.serve(self.handler, self.host, self.port):
            print(f"Serwer WebSocket uruchomiony na {self.host}:{self.port}")
            await asyncio.Future()  # Czekaj na zamknięcie serwera

    async def handler(self, websocket, path):
        print("Połączono z klientem")
        self.websocket = websocket

        try:
            async for message in websocket:
                self.received_data = json.loads(message)  # Zapisujemy odebrane dane
                print("Odebrano dane:", self.received_data)
        except websockets.exceptions.ConnectionClosed:
            print("Rozłączono z klientem")
            self.websocket = None

    async def wyslij(self, data):
        print("wysylam")
        if self.websocket and self.websocket.open:
            data_to_send = json.dumps(data)
            await self.websocket.send(data_to_send)
            print("Wysłano dane:", data)
        else:
            print("Brak aktywnego połączenia z klientem")

    def get_received_data(self):
        # Zwraca ostatnie odebrane dane
        return self.received_data
