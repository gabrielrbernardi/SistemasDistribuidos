from concurrent import futures
import time
import grpc
import threading

import grpc_pb2
import grpc_pb2_grpc

cacheValues = {}

class Server(grpc_pb2_grpc.TodoServicer):
    def __init__(self):
        self.id = 0
        self.lastPrintTime = time.time()

    def createItem(self, request, context):
        self.id += 1
        cacheValues[self.id] = request.payload

        return grpc_pb2.Items(id=self.id, payload = request.payload)

    def returnItems(self, request, context):
        itemsList = []
        for i in cacheValues:
            tempValueDict = (i, str(cacheValues.get(i)))
            itemsList.append(tempValueDict)

        print("\n")
        print(itemsList)
        return 

    def getUser(self, request, context):
        if(not request.id in cacheValues):
            response = grpc_pb2.returnErrorRequest(Error="Usuario nao encontrado")
            return response
        else:
            response = grpc_pb2.Item(
                id=request.id,
                payload=cacheValues[request.id]
            )
            return response

    def updateUser(self, request, context):
        print(request.id)
        if(request.id in cacheValues):
            print("ID existente")
            cacheValues[request.id] = request.payload
            print(cacheValues[request.id])
        else:
            print("ID inexistente")

        response = grpc_pb2.UpdateUserRequest(id=request.id, payload=str(cacheValues[request.id]))
        print(response)
        return (response)

    def deleteUser(self, request, context):
        print(request)
        print(cacheValues)
        cacheValues.pop(request.id)
        print(cacheValues)

        response = grpc_pb2.voidNoParam()
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    grpc_pb2_grpc.add_TodoServicer_to_server(Server(), server)
    server.add_insecure_port("[::]:10000")
    server.start()
    
    try:
        while True:
            # print(f"server na thread: {threading.active_count()}")
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt solicitado pelo usuario")
        server.stop(0)

if __name__ == "__main__":
    print("iniciando server")
    serve()