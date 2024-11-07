import asyncio
import subprocess

from connection import WebSocket
from modules.arduino import Arduino

server = None 
do_user = None
od_user = None

arduino_podwozie = None
arduino_manipulator = None
do_podwozie = None
od_podwozie = None
do_manipulator = None
od_manipulator = None


async def init_camera_pi():
    #plik z kamerą (uruchamianie kamery automatycznie, trzeba usunac jeszze run_camera_mper.service)
    try:
        subprocess.run(['sudo', 'python3', 'modules/camera_pi.py'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        print("Błąd uruchomienia kamery")

async def init_arduinos():
    global arduino_manipulator, arduino_podwozie

    arduino_podwozie = Arduino('/dev/ttyACM0')
    arduino_podwozie.set_callback(on_detction)
    arudino_podwozie.start_get_data()

    arduino_manipulator= Arduino('/dev/ttyACM0')
    arduino_manipulator.set_callback(on_detction)
    arduino_manipulator .start_get_data()

async def arduinos_task():
    global arduino_podwozie, arduino_manipulator, do_manipulator, od_manipulator, do_podwozie, od

    # Wysyłanie danych do Arduino
    arduino_podwozie.send_data(do_podwozie)
    arduino_manipulator.send_data(do_manipulator)

    # Odczyt danych odebranych z Arduino
    od_podwozie = arduino_podwozie.received_data
    od_manipulator = arduino_manipulator.received_data

async def user_task():
    global do_podwozie, od_podwozie, do_manipulator, od_manipulator
    global server, do_user, od_user

    od_user = server.get_received_data()
    do_user = [0, 0, 0, 0]
    if od_user is not None:
        print("Odebrane dane:", od_user)

    
    
    await server.wyslij(do_user)

async def main():
    server = WebSocket()
    # zadania
    await server.start()
    await init_camera_pi()  # Inicjalizacja kamery
    await init_arduinos()  # Inicjalizacja Arduino

    while True:
        await user_task()       # Zadanie obsługujące dane użytkownika
        await arduinos_task()    # Zadanie obsługujące komunikację z Arduino
        await asyncio.sleep(1)  # Czas oczekiwania między iteracjami

if __name__ == "__main__":
    asyncio.run(main())
