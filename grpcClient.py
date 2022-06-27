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

    def userType(self):
        print("TIPO USUARIO".center(50, "="))
        print("1 - Administrador")
        print("2 - Cliente")
        choose = int(input("Escolha o tipo de usuario:"))
        return choose


    def userActionAdmin(self):
        print("MENU Admin".center(50, "="))
        print(" 1 - Criar usuario")
        print(" 2 - Retornar usuarios")
        print(" 3 - Retornar usuario especifico")
        print(" 4 - Atualizar usuario")
        print(" 5 - Remover usuario")
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

        elif choose == 9:
            print("Encerrando client")
            exit()
        else:
            print("Opcao invalida")

    def userActionClient(self):
        print("MENU Client".center(50, "="))
        print(" 1 - Criar tarefa")
        # print(" 2 - Retornar usuarios")
        print(" 3 - Retornar tarefa especifica")
        # print(" 4 - Atualizar usuario")
        # print(" 5 - Remover usuario")
        # print(" 9 - Finalizar client")
        choose = int(input("Digite o numero da opcao: "))
        if(choose == 1):
            self.createTask()
        # elif(choose == 2):
        #     self.getUsers()
        elif choose == 3:
            self.getTask()
        # elif choose == 4:creteTask
        #     self.updateUser()
        # elif choose == 5:
        #     self.deleteUser()

        elif choose == 9:
            print("Encerrando client")
            exit()
        else:
            print("Opcao invalida")


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
        id0 = 0
        with grpc.insecure_channel(host + ":" + str(self.port)) as channel:
            stub = grpc_pb2_grpc.TodoStub(channel)
            
            formatUserData = self.fillUserData()
            dictValuesString = str(formatUserData)
            
            try:
                response = stub.createItem(grpc_pb2.Item(id = id0, payload = dictValuesString))
                id0 = response.id
                print(f"\n\nRequisicao enviada. ID de acesso: {id0}")
                # print(f"{time.time() - start} : resp={response.id} and txt={response.txt}: pid={pid}")
                time.sleep(0.001)
            except KeyboardInterrupt: 
                print("\nKeyboardInterrupt solicitada pelo usuario")
                channel.unsubscribe(self.close)
                exit()
    
    def createTask(self):
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
            # except:
            #     print("Erro na criacao da tarefa")
    ######### Read methods #########
    def getUser(self, id0 = 0):
        with grpc.insecure_channel(host + ":" + str(self.port)) as channel:
            stub = grpc_pb2_grpc.TodoStub(channel)

            if not id0:
                id0 = int(input("Digite o id do usuario: "))

            message = grpc_pb2.getUserRequest(id=id0)
            response = stub.getUser(message)
            if response.id != 0:
                print("Usuario buscado")
                # print(response)
                return response
            else:
                print("Usuario nao encontrado")

    def getTask(self, id0 = 0):
        with grpc.insecure_channel(host + ":" + str(self.port)) as channel:
            stub = tasks_pb2_grpc.TasksStub(channel)

            if not id0:
                id0 = int(input("Digite o id da tarefa: "))

            message = tasks_pb2.getTaskRequest(id=id0)
            response = stub.getTask(message)
            if response.id != 0:
                print("Tarefa buscada")
                # print(response)
                print(response)
                return response
            else:
                print("Tarefa nao encontrada")



    def getUsers(self):
        try:
            with grpc.insecure_channel(host + ":" + str(self.port)) as channel:
                stub = grpc_pb2_grpc.TodoStub(channel)
                message = grpc_pb2.voidNoParam()
                stub.returnItems(message)
                # print(response)
        except Exception:
            print("deu erro na visualizacao geral")

    ######### Update method #########
    def updateUser(self):
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
                    # print(f"{time.time() - start} : resp={response.id} and txt={response.txt}: pid={pid}")
                    time.sleep(0.001)
                except KeyboardInterrupt: 
                    print("\nKeyboardInterrupt solicitada pelo usuario")
                    channel.unsubscribe(self. close)
                    exit()
        
            # print(response)
        else:
            print("Usuario nao encontrado")
        # with grpc.insecure_channel(host + ":" + str(self.port)) as channel:
        #     stub = grpc_pb2_grpc.TodoStub(channel)
        #     response = stub.checkItem(grpc_pb2.Item(id = idInput))
        #     print("aqui vai a resposta")
        #     print(response)

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



    def run(self):   
        # pid = os.getpid()
        try:
            print("Client conectando na porta " + str(self.port))
            tipoUsuario = self.userType()
            if tipoUsuario == 1: #admin
                while True:
                    self.userActionAdmin()
            else:
                while True:
                    self.userActionClient()
        except KeyboardInterrupt: 
            print("\nKeyboardInterrupt solicitada pelo usuario")
            exit()
        # except grpc._channel._InactiveRpcError:
        #     print("\n\nerro no grpc\n\n")
        #     run()
        # except AttributeError:
        #     print("AttributeError: Atributo inexistente e/ou incorreto")
        # except grpc.RpcError as e:
        #     print("Erro na Conexao do gRPC")
        #     print(e.code())
        #     print(e.details())
        # except Exception:
        #     print("Erro na execucao do programa!")

    def close(channel):
        "close the channel"
        channel.close()

if __name__ == "__main__":
    availablePorts = [10000, 10001, 10002, 10003]
    # port = int(input("Digite a porta de conexao"))
    # gc = GrpcClient(port)
    gc = GrpcClient(availablePorts[0])
    gc.run()
