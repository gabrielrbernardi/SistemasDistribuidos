from concurrent import futures
import time
import grpc
import threading

import grpc_pb2
import grpc_pb2_grpc


class Server(grpc_pb2_grpc.TodoServicer):
    def __init__(self):
        self.id = 0
        self.lastPrintTime = time.time()

    def createItem(self, request, context):
        self.id += 1
        if self.id > 10000:
            formatValue = time.time() - self.lastPrintTime
            print(f"10k chamadas em {formatValue} segundos")
            self.lastPrintTime = time.time()
            self.id = 0
        return grpc_pb2.Items(id=request.id + 1)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    grpc_pb2_grpc.add_TodoServicer_to_server(Server(), server)
    server.add_insecure_port("[::]:10000")
    server.start()
    
    try:
        while True:
            print(f"server na thread: {threading.active_count()}")
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt solicitado pelo usuario")
        server.stop(0)

if __name__ == "__main__":
    print("iniciando server")
    serve()