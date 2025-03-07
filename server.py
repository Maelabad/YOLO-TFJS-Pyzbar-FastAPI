
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import io
import base64
import logging

# Configuration du logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

# Stockage des codes-barres détectés
list_code_bar = []

@app.get("/")
def index():
    return {"message": "Hello, FastAPI WebSockets!"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logging.info("Client WebSocket connecté")
    
    nb_node_barcode_detected = 0  # Initialisation du compteur local
    
    try:
        while True:
            try:
                data = await websocket.receive_text()
                image_data = base64.b64decode(data)  # Décodage base64 en bytes
                image = Image.open(io.BytesIO(image_data))  # Charger l'image
                
                # Décoder le code-barres
                decoded_objects = decode(image)
                if decoded_objects:
                    code = decoded_objects[0].data.decode("utf-8")  # Extraire le texte du code-barres
                    logging.info(f"Code-barre détecté : {code}")
                    list_code_bar.append(code)
                    await websocket.send_text(code)  # Envoyer au client
                    nb_node_barcode_detected = 0  # Réinitialiser le compteur
                else:
                    nb_node_barcode_detected += 1
                    logging.warning("Aucun code-barre détecté")
                
                if nb_node_barcode_detected >= 100:
                    await websocket.send_text("Impossible de détecter un code-barre après plusieurs essais.")
                    nb_node_barcode_detected = 0  # Réinitialisation après avertissement
            
            except WebSocketDisconnect:
                logging.info("Client WebSocket déconnecté proprement")
                break
            except Exception as e:
                logging.error(f"Erreur lors du traitement de l'image : {e}")
                await websocket.send_text("Erreur lors du traitement de l'image.")
                break
    
    finally:
        logging.info("Client WebSocket fermé, affichage des codes-barres détectés :")
        logging.info(list_code_bar)
        await websocket.close()











"""
from fastapi import FastAPI, WebSocket
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import io
import base64

app = FastAPI()

list_code_bar = []
nb_node_barcode_detected = 0

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client WebSocket connecté")

    try:
        while True:
            data = await websocket.receive_text()
            image_data = base64.b64decode(data)  # Décodage base64 en bytes
            image = Image.open(io.BytesIO(image_data))  # Charger l'image

            # Décoder le code-barres
            decoded_objects = decode(image)
            if decoded_objects:
                code = decoded_objects[0].data.decode("utf-8")  # Extraire le texte du code-barres
                print(f"Code-barre détecté : {code}")
                list_code_bar.append(code)
                await websocket.send_text(code)  # Envoyer au client
                nb_node_barcode_detected = 0
            else:
                print("Aucun code bar detecté")
                nb_node_barcode_detected +=1
                # await websocket.send_text("Aucun code-barre détecté")
            if (nb_node_barcode_detected >= 100):
                await websocket.send_text("Nous n'arrivons pas a detecter de code bar. Meme a pres plusieurs essais.")

                

    except Exception as e:
        pass
        # print(f"Erreur WebSocket : {e}")
    finally:
        print("Client WebSocket déconnecté")
        print(list_code_bar)
        await websocket.close()
"""