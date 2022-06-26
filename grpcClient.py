import os
import time
import grpc
import grpc_pb2
import grpc_pb2_grpc

host = "localhost"
port = "10000"

def run():
    id0 = 0
    pid = os.getpid()
    with grpc.insecure_channel(host + ":" + port) as channel:
        stub = grpc_pb2_grpc.TodoStub(channel)
        while True:
            try:
                start = time.time()
                response = stub.createItem(grpc_pb2.Item(id = id0))
                id0 = response.id
                if id0 % 1000 == 0:
                    print(f"{time.time() - start} : resp={response.id} : pid={pid}")
                time.sleep(0.001)
            except KeyboardInterrupt: 
                print("\nKeyboardInterrupt solicitada pelo usuario")
                channel.unsubscribe(close)
                exit()

def close(channel):
    "close the channel"
    channel.close()

if __name__ == "__main__":
    print("iniciando client")
    run()
