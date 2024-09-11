import asyncio
import websockets
import json

# Funkcja do odbierania danych od klienta
async def joystick_handler(websocket, path):
    print("Połączono z klientem")

    # Zadanie do odbierania danych od klienta
    async def receive_data():
        try:
            async for message in websocket:
                data = json.loads(message)
                print(data)
        except websockets.exceptions.ConnectionClosed:
            print("Rozłączono z klientem")

    # Zadanie do wysyłania danych co 1 sekundę
    async def send_data():
        while True:
            if websocket.open:
                # Przykładowa ramka danych do wysyłania (na razie same 0)
                data_to_send = json.dumps({"frame": 0})
                await websocket.send(data_to_send)
                print("Wysłano ramkę danych: 0")
            await asyncio.sleep(1)  # Wysyłanie co 1 sekundę

    # Uruchamiamy obie funkcje jednocześnie
    await asyncio.gather(receive_data(), send_data())

# Uruchomienie serwera WebSocket
async def main():
    async with websockets.serve(joystick_handler, "0.0.0.0", 8765):
        print("Serwer WebSocket uruchomiony")
        await asyncio.Future()  # Działa bez końca

if __name__ == "__main__":
    asyncio.run(main())
