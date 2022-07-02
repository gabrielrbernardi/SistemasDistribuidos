import os
import time
import grpc
import grpc_pb2
import grpc_pb2_grpc
import tasks_pb2
import tasks_pb2_grpc

host = "localhost"
port = "10000"

class GrpcClient:
    def __init__(self, port):
        self.port = port

    ######### Menu methods #########

    def portNumber():
        flag = False
        while True:
            if(flag == False):
                print("\n" * 50)
            print("1 - 10000")
            print("2 - 10001")
            print("3 - 10002")
            print("4 - 10003")
            try:
                choose = int(input("Digite a opcao de porta que sera inicializada: "))
                if choose > 4 or choose < 1:
                    print("Porta invalida")
                    flag = True
                else:
                    return choose
            except:
                raise Exception("Erro no input de configuração de porta")

    
    def userType(self):
        while True:
            print("TIPO USUARIO".center(50, "="))
            print("1 - Administrador")
            print("2 - Cliente")
            choose = int(input("Escolha o tipo de usuario: "))

            if choose > 2 and choose < 1:
                print("Opcao invalida")
            else:
                return choose

    def userActionAdmin(self):
        print("MENU Admin".center(50, "="))
        print(" 1 - Criar usuario")
        print(" 2 - Retornar usuarios")
        print(" 3 - Retornar usuario especifico")
        print(" 4 - Atualizar usuario")
        print(" 5 - Remover usuario")
        print(" 6 - Enviar conteudo")
        print(" 8 - Menu anterior")
        print(" 9 - Finalizar client")
        choose = int(input("Digite o numero da opcao: "))
        if(choose == 1):
            self.createUser()
        elif(choose == 2):
            self.getUsers()
        elif choose == 3:
            self.getUser()
        elif choose == 4:
            self.updateUser()
        elif choose == 5:
            self.deleteUser()
        elif choose == 6:
            self.flushUserContent()

        elif choose == 8:
            self.run()
        elif choose == 9:
            print("Encerrando client")
            exit()
        else:
            print("Opcao invalida")

    def userActionClient(self):
        print("MENU Client".center(50, "="))
        print(" 1 - Criar tarefa")
        print(" 2 - Retornar todas as tarefas")
        print(" 3 - Retornar tarefa especifica por ID")
        print(" 4 - Retornar todas tarefas de um usuario")
        print(" 5 - Atualizar tarefa")
        print(" 6 - Remover tarefa")
        print(" 7 - Enviar conteudo")
        print(" 8 - Menu anterior")
        print(" 9 - Finalizar client")
        choose = int(input("Digite o numero da opcao: "))
        if(choose == 1):
            self.createTask()
        elif(choose == 2):
            self.getTasks()
        elif choose == 3:
            self.getTask()
        elif choose == 4:
            self.getTasksByUser()
        elif choose == 5:
            self.updateTask()
        elif choose == 6:
            self.deleteSpecificTask()
        elif choose == 7:
            self.flushTaskContent()

        elif choose == 8:
            self.run()
        elif choose == 9:
            print("Encerrando client")
            exit()
        else:
            print("Opcao invalida")

    ######### Input methods #########

    def fillUserData(self):
        nomeInput = input("Digite o nome: ")
        emailInput = input("Digite o email: ")
        idadeInput = int(input("Digite a idade: "))
        
        dictValues = {"nome":nomeInput, "email":emailInput, "idade":idadeInput}

        return dictValues
    
    def fillTaskData(self, id):
        tituloInput = input("Digite o titulo da tarefa: ")
        descricaoInput = input("Digite a descricao da tarefa: ")

        dictValues = {"cid": id, "titulo": tituloInput, "descricao": descricaoInput}

        return dictValues

    ######### Create methods #########

    def createUser(self):
        try:
            id0 = 0
            with grpc.insecure_channel(host + ":" + str(self.port)) as channel:
                stub = grpc_pb2_grpc.TodoStub(channel)
                
                formatUserData = self.fillUserData()
                dictValuesString = str(formatUserData)
                
                try:
                    response = stub.createItem(grpc_pb2.Item(id = id0, payload = dictValuesString))
                    id0 = response.id
                    print(f"\n\nRequisicao enviada. ID de acesso: {id0}")
                    time.sleep(0.001)
                except KeyboardInterrupt: 
                    print("\nKeyboardInterrupt solicitada pelo usuario")
                    channel.unsubscribe(self.close)
                    exit()
        except:
            print("Erro na criacao do usuario")
    
    def createTask(self):
        try:
            id0 = 0
            with grpc.insecure_channel(host + ":" + str(self.port)) as channel:            
                stub = tasks_pb2_grpc.TasksStub(channel)

                requestId = self.getUser().id

                formatTaskData = self.fillTaskData(requestId)
                dictValuesString = str(formatTaskData)

                # try:
                response = stub.createTask(tasks_pb2.Task(id = id0, payload=dictValuesString))
                id0 = response.id
                print("Requisicao enviada")
        except:
            print("Erro na criacao da tarefa")

    ######### Read methods #########

    def getUser(self, id0 = 0):
        try:
            with grpc.insecure_channel(host + ":" + str(self.port)) as channel:
                stub = grpc_pb2_grpc.TodoStub(channel)

                if not id0:
                    id0 = int(input("Digite o id do usuario: "))

                message = grpc_pb2.getUserRequest(id=id0)
                response = stub.getUser(message)
                if response.id != 0:
                    print("Usuario buscado")
                    print(response)
                    return response
                else:
                    print("Usuario nao encontrado")
        except:
            print("Erro no retorno do usuario")

    def getTask(self, id0 = 0, origin = 0):
        try:
            with grpc.insecure_channel(host + ":" + str(self.port)) as channel:
                stub = tasks_pb2_grpc.TasksStub(channel)

                if not id0:
                    id0 = int(input("Digite o id da tarefa: "))

                response = stub.getTask(tasks_pb2.getTaskRequest(id = id0))
                print()
                if(origin != 0):
                    return response
                else:
                    print(response)
        except:
            return ("Erro na busca da tarefa")

    def getUsers(self):
        try:
            with grpc.insecure_channel(host + ":" + str(self.port)) as channel:
                stub = grpc_pb2_grpc.TodoStub(channel)
                message = grpc_pb2.voidNoParam()
                response = stub.returnItems(message)
                print("\n")
                print(response)
        except Exception:
            print("deu erro na visualizacao geral")

    def getTasks(self, id0 = 1):
        try:
            with grpc.insecure_channel(host + ":" + str(self.port)) as channel:
                stub = tasks_pb2_grpc.TasksStub(channel)

                response = stub.getTasks(tasks_pb2.getAllTasksByUser(idUsuario = id0))
                print(response)
        except:
            print("Erro na busca de todas as tarefas")
    
    def getTasksByUser(self, id0 = 0):
        try:
            with grpc.insecure_channel(host + ":" + str(self.port)) as channel:
                stub = tasks_pb2_grpc.TasksStub(channel)

                if not id0:
                    id0 = int(input("Digite o id da tarefa: "))

                response = stub.getTasksByUser(tasks_pb2.getAllTasksByUser(idUsuario = id0))
                print(response)
        except:
           print("Nao foi possivel retornar as tarefas!")
    
    ######### Update method #########

    def updateUser(self):
        try:
            idInput = int(input("Digite o ID do usuario a ser atualizado: "))
            response = self.getUser(idInput)
            if response:
                print("\n\nUsuario encontrado")
                print("Atualizando Usuario".center(50, "="))
                
                #Preenchendo valores para serem atualizados
                formatUserData = self.fillUserData()

                dictValuesString = str(formatUserData)

                with grpc.insecure_channel(host + ":" + str(self.port)) as channel:
                    stub = grpc_pb2_grpc.TodoStub(channel)

                    try:
                        response = stub.updateUser(grpc_pb2.UpdateUserRequest(id = idInput, payload = dictValuesString))
                        id0 = response.id
                        print(f"\n\nRequisicao enviada. ID do usuario atualizado: {id0}")
                        time.sleep(0.001)
                    except KeyboardInterrupt: 
                        print("\nKeyboardInterrupt solicitada pelo usuario")
                        channel.unsubscribe(self. close)
                        exit()

            else:
                print("Usuario nao encontrado")
        except:
            print("Erro na atualizacao do usuario")

    def updateTask(self):
        try:
            with grpc.insecure_channel(host + ":" + str(self.port)) as channel:
                stub = tasks_pb2_grpc.TasksStub(channel)
                tempResponse = self.getTask(origin=1)
                id = (tempResponse.tasks[0].id)
                if (tempResponse != "Erro na busca da tarefa"):
                    taskData = str(self.fillTaskData(id = id))
                    print(id)

                    response = stub.updateTask(tasks_pb2.UpdateTaskRequest(id = id, payload = taskData))
                    print(response)
        except:
            print("Erro na atualizaca da tarefa")
        

    ######### Delete method #########

    def deleteUser(self):
        idInput = int(input("Digite o ID do usuario a ser removido: "))
        response = self.getUser(idInput)
        if response:
            with grpc.insecure_channel(host + ":" + str(self.port)) as channel:
                stub = grpc_pb2_grpc.TodoStub(channel)

                try:
                    response = stub.deleteUser(grpc_pb2.getUserRequest(id = idInput))
                    id0 = response.id
                    print(f"\nRequisicao enviada. Usuario de ID {idInput} removido")
                    # print(f"{time.time() - start} : resp={response.id} and txt={response.txt}: pid={pid}")
                    time.sleep(0.001)
                except KeyboardInterrupt: 
                    print("\nKeyboardInterrupt solicitada pelo usuario")
                    channel.unsubscribe(self.close)
                    exit()
        else:
            print("Erro ao excluir usuario")

    def deleteSpecificTask(self):
        id = int(input("Digite o id da tarefa: "))

        with grpc.insecure_channel(host + ":" + str(self.port)) as channel:
            stub = tasks_pb2_grpc.TasksStub(channel)
            try:    
                response = stub.deleteSpecificTask(tasks_pb2.getTaskRequest(id = id))
                print(response)
                print(f"Tarefa com ID {id} removida")
            except:
                print("Erro na exclusao")

    ######### Sent contents PUB/SUB #########
    
    def flushUserContent(self):
        try:
            with grpc.insecure_channel(host + ":" + str(self.port)) as channel:
                stub = grpc_pb2_grpc.TodoStub(channel)

                response = stub.flushUserContent(grpc_pb2.voidNoParam())
                print(response)
        except:
            print("Erro no envio dos usuarios via Mosquitto")


    def flushTaskContent(self):
        try:
            with grpc.insecure_channel(host + ":" + str(self.port)) as channel:
                stub = tasks_pb2_grpc.TasksStub(channel)

                response = stub.flushTaskContent(tasks_pb2.voidNoParam())
                print(response)
        except:
            print("Erro no envio das tarefas via Mosquitto")

    ######### EXECUCAO #########

    def run(self):   
        print("Client conectando na porta " + str(self.port))

        # pid = os.getpid()
        tipoUsuario = self.userType()
        if tipoUsuario == 1: #admin
            while True:
                self.userActionAdmin()
        else:
            while True:
                self.userActionClient()
    
    def close(channel):
        "close the channel"
        channel.close()

if __name__ == "__main__":
    try:
        portInput = GrpcClient.portNumber()
        availablePorts = [10000, 10001, 10002, 10003]
        tempPort = 0

        if portInput == 1:
            tempPort = availablePorts[0]
        elif portInput == 2:
            tempPort = availablePorts[1]
        elif portInput == 3:
            tempPort = availablePorts[2]
        elif portInput == 4:
            tempPort = availablePorts[3]

        gc = GrpcClient(tempPort)
        gc.run()

    except KeyboardInterrupt: 
        print("\nKeyboardInterrupt solicitada pelo usuario")
        exit()
    except AttributeError:
        print("AttributeError: Atributo inexistente e/ou incorreto")
    except grpc.RpcError as e:
        print("Erro na Conexao do gRPC")
        print(e.code())
        print(e.details())
    except Exception as err:
        print(str(err) + "\nErro na execucao do programa!")
    except:
        print("Erro generico!")
