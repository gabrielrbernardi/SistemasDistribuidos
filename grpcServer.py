from concurrent import futures
import time
import grpc
import threading

import grpc_pb2
import grpc_pb2_grpc
import tasks_pb2
import tasks_pb2_grpc

# import context

import paho.mqtt.publish as publish

cacheValues = {}

cacheValuesTask = {}

class Server(grpc_pb2_grpc.TodoServicer):
    def __init__(self):
        self.id = 0
        self.lastPrintTime = time.time()

    def createItem(self, request, _):
        self.id += 1
        cacheValues[self.id] = request.payload

        return grpc_pb2.Items(id=self.id, payload = request.payload)

    def returnItems(self, request, _):   
        il = grpc_pb2.ItemsList()
        
        for i in cacheValues:
            il.items.append(grpc_pb2.Item(id=i, payload=cacheValues[i]))

        return il

    def getUser(self, request, _):
        if(not request.id in cacheValues):
            response = grpc_pb2.returnErrorRequest(Error="Usuario nao encontrado")
            return response
        else:
            response = grpc_pb2.Item(
                id=request.id,
                payload=cacheValues[request.id]
            )
            return response

    def updateUser(self, request, _):
        try:
            if(request.id in cacheValues):
                # print("ID existente")
                cacheValues[request.id] = request.payload
                # print(cacheValues[request.id])
            else:
                raise Exception("ID inexistente")

            response = grpc_pb2.UpdateUserRequest(id=request.id, payload=str(cacheValues[request.id]))

            return (response)
        except Exception as err:
            raise Exception(err)

    def deleteUser(self, request, _):
        cacheValues.pop(request.id)

        response = grpc_pb2.voidNoParam()
        return response

    def flushUserContent(self, request, _):
        publish.single("content/client_" + str(portInput) + "/users", str(cacheValues), hostname="localhost")

        response = tasks_pb2.voidNoParam()
        return response

class ServerTask(tasks_pb2_grpc.TasksServicer):
    def __init__(self):
        self.taskId = 0
    
    def createTask(self, request, _):
        try:
            self.taskId += 1
            cacheValuesTask[self.taskId] = request.payload

            return tasks_pb2.Task(id=self.taskId, payload = request.payload)
        except:
            raise Exception("Erro na criacao da tarefa")

    def returnItems(self, request, _):   
        try:
            il = grpc_pb2.ItemsList()
            
            for i in cacheValuesTask:
                il.items.append(grpc_pb2.Item(id=i, payload=cacheValues[i]))

            return il
        except:
            raise Exception("Erro no retorno das tarefas")
    
    def getTask(self, request, _):
        try:
            if(not request.id in cacheValuesTask):
                raise Exception("Nao possui tarefa com o ID informado")
            else:
                it = tasks_pb2.TasksList()

                it.tasks.append(tasks_pb2.Task(id = request.id, payload = cacheValuesTask[request.id]))
                return it
        except Exception as err:
            raise Exception("Erro no retorno da tarefa")

    def getTasks(self, request, _):
        try:
            it = tasks_pb2.TasksList()

            for i in cacheValuesTask:
                it.tasks.append(tasks_pb2.Task(id = i, payload = cacheValuesTask[i]))
            return it
        except:
            raise Exception("Erro no retorno das tarefas")

    def getTasksByUser(self, request, _):
        try:
            if(not request.idUsuario in cacheValuesTask):
                raise Exception("Tarefa nao encontrada")
            else:
                it = tasks_pb2.TasksList()

                for i in cacheValuesTask:
                    tempStr = cacheValuesTask[i].partition(", 'titulo'")
                    tempStr = tempStr[0].replace("{'cid': ", "")
                    userId = int(tempStr)
                    if(userId == request.idUsuario):
                        it.tasks.append(tasks_pb2.Task(id = i, payload = cacheValuesTask[i]))
                return it
        except:
            raise Exception("Erro no retorno das tarefas")

    def updateTask(self, request, _):
        try:
            if not request.id in cacheValuesTask:
                raise Exception("Tarefa nao encontrada")
            else:
                cacheValuesTask[request.id] = request.payload
                # print(cacheValuesTask[request.id])
                response = tasks_pb2.Task(
                    id=request.id,
                    payload=cacheValuesTask[request.id]
                )
                return response
        except:
            raise Exception("Erro na atualizacao da tarefa")

    def deleteSpecificTask(self, request, _):
        try:
            if not request.id in cacheValuesTask:
                raise Exception("Tarefa nao encontrada")
            else:
                cacheValuesTask.pop(request.id)

                response = tasks_pb2.voidNoParam()
                return response
        except:
            raise Exception("Erro na exclusao da tarefa")
    
    def flushTaskContent(self, request, _):
        publish.single("content/client_" + str(portInput) + "/tasks", str(cacheValuesTask), hostname="localhost")

        response = tasks_pb2.voidNoParam()
        return response

portInput = 0

def mainServer():
    availablePorts = [10000, 10001, 10002, 10003]
    
    print(" 1 - 10000")
    print(" 2 - 10001")
    print(" 3 - 10002")
    print(" 4 - 10003")
    
    global portInput
    while True:
        portInput = int(input("Digite a opcao de porta que sera inicializado: "))
        
        port = 0
        if portInput == 1:
            port = availablePorts[0]
        elif portInput == 2:
            port = availablePorts[1]
        elif portInput == 3:
            port = availablePorts[2]
        elif portInput == 4:
            port = availablePorts[1]
        
        if portInput > 4 and portInput < 1:
            print("Opcao invalida")
        else:
            break

    serve(port = port)

def serve(port=10000):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    grpc_pb2_grpc.add_TodoServicer_to_server(Server(), server)
    tasks_pb2_grpc.add_TasksServicer_to_server(ServerTask(), server)
    server.add_insecure_port("[::]:" + str(port))
    server.start()
    print("Server iniciado na porta " + str(port))

    try:
        while True:
            # print(f"server na thread: {threading.active_count()}")
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt solicitado pelo usuario")
        server.stop(0)
    except:
        print("Erro generico")

if __name__ == "__main__":
    mainServer()