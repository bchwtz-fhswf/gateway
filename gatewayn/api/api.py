from concurrent import futures
import logging
import time
from gatewayn.api.services.hub_service import HubService
import gatewayn.proto_generated.hub_pb2_grpc as hub_service
from gatewayn.hub.hub import Hub
from purerpc import Server
import grpc

class API:
    def __init__(self):
        self.server = Server(50051)
        self.hub_service = HubService(Hub())

    def setup_routes(self):
        
        self.server.add_service(self.hub_service.service)

    async def run(self):
        await self.server.serve_async()
        try:
            while True:
                time.sleep(3600*24)
        except KeyboardInterrupt:
            logging.debug('GRPC stop')
            self.server.stop(0)