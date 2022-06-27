from concurrent import futures
import time
import grpc
import threading

import grpc_pb2
import grpc_pb2_grpc
import tasks_pb2
import tasks_pb2_grpc

cacheValues = {}

cacheValuesTask = {}

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

class ServerTask(tasks_pb2_grpc.TasksServicer):
    def __init__(self):
        self.taskId = 0
    
    def createTask(self, request, context):
        self.taskId += 1
        cacheValuesTask[self.taskId] = request.payload

        return tasks_pb2.Task(id=self.taskId, payload = request.payload)

    def getTask(self, request, context):
        if(not request.id in cacheValuesTask):
            response = tasks_pb2.returnErrorRequest(Error="Tarefa nao encontrada")
            return response
        else:
            response = tasks_pb2.Task(
                id=request.id,
                payload=cacheValuesTask[request.id]
            )
            return response



def mainServer():
    availablePorts = [10000, 10001, 10002, 10003]
    serve()

def serve(port=10000):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    grpc_pb2_grpc.add_TodoServicer_to_server(Server(), server)
    tasks_pb2_grpc.add_TasksServicer_to_server(ServerTask(), server)
    server.add_insecure_port("[::]:" + str(port))
    server.start()
    print("Server iniciado na porta " + str(port))

    # def createItem(self, request, context):
    #     self.id += 1
    #     cacheValues[self.id] = request.payload

    #     return grpc_pb2.Items(id=self.id, payload = request.payload)

    try:
        while True:
            # print(f"server na thread: {threading.active_count()}")
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt solicitado pelo usuario")
        server.stop(0)

if __name__ == "__main__":
    mainServer()