import asyncio
import json

class NotificadorSSE:
    def __init__(self):
        self.clientes = []

    async def conectar_cliente(self):
        
        cola = asyncio.Queue()
        self.clientes.append(cola)
        return cola

    def desconectar_cliente(self, cola):
        
        if cola in self.clientes:
            self.clientes.remove(cola)

    async def notificar_nueva_alerta(self, noticia_json: dict):
        
        for cola in self.clientes:
            await cola.put(noticia_json)

notificador = NotificadorSSE()