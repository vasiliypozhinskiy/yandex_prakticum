import time
from concurrent import futures

import grpc
from loguru import logger

from integration.messages import user_pb2_grpc
from services.user import UserServices

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

def grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_serve = UserServices()
    user_pb2_grpc.add_UserServicer_to_server(user_serve, server)
    logger.info('GRPC server running')
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        logger.debug('GRPC stop')
        server.stop(0)

if __name__ == '__main__':
    grpc_server()