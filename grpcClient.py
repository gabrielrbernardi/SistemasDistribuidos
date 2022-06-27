import email
import os
import time
import grpc
import grpc_pb2
import grpc_pb2_grpc

host = "localhost"
port = "10000"

def userType():
    print("TIPO USUARIO".center(50, "="))
    print("1 - Administrador")
    print("2 - Cliente")
    choose = int(input("Escolha o tipo de usuario:"))
    return choose


def userActionAdmin():
    print("MENU".center(50, "="))
    print(" 1 - Criar usuario")
    print(" 2 - Retornar usuarios")
    print(" 3 - Retornar usuario especifico")
    print(" 4 - Atualizar usuario")
    print(" 5 - Remover usuario")
    print(" 9 - Finalizar client")
    choose = int(input("Digite o numero da opcao: "))
    if(choose == 1):
        createUser()
    elif(choose == 2):
        getUsers()
    elif choose == 3:
        getUser()
    elif choose == 4:
        updateUser()
    elif choose == 5:
        deleteUser()

    elif choose == 9:
        print("Encerrando client")
        exit()
    else:
        print("Opcao invalida")

def userActionClient():
    print("MENU".center(50, "="))
    print(" 1 - Criar usuario")
    print(" 2 - Retornar usuarios")
    print(" 3 - Retornar usuario especifico")
    print(" 4 - Atualizar usuario")
    print(" 5 - Remover usuario")
    print(" 9 - Finalizar client")
    choose = int(input("Digite o numero da opcao: "))
    if(choose == 1):
        createUser()
    elif(choose == 2):
        getUsers()
    elif choose == 3:
        getUser()
    elif choose == 4:
        updateUser()
    elif choose == 5:
        deleteUser()

    elif choose == 9:
        print("Encerrando client")
        exit()
    else:
        print("Opcao invalida")


def fillUSerData():
    nomeInput = input("Digite o nome: ")
    emailInput = input("Digite o email: ")
    idadeInput = int(input("Digite a idade: "))
    
    dictValues = {"nome":nomeInput, "email":emailInput, "idade":idadeInput}

    return dictValues
        

######### Create method #########
def createUser():
    id0 = 0
    with grpc.insecure_channel(host + ":" + port) as channel:
        stub = grpc_pb2_grpc.TodoStub(channel)
        
        formatUserData = fillUSerData()
        dictValuesString = str(formatUserData)
        
        try:
            response = stub.createItem(grpc_pb2.Item(id = id0, payload = dictValuesString))
            id0 = response.id
            print(f"\n\nRequisicao enviada. ID de acesso: {id0}")
            # print(f"{time.time() - start} : resp={response.id} and txt={response.txt}: pid={pid}")
            time.sleep(0.001)
        except KeyboardInterrupt: 
            print("\nKeyboardInterrupt solicitada pelo usuario")
            channel.unsubscribe(close)
            exit()
######### Read methods #########
def getUser(id0 = 0):
    with grpc.insecure_channel(host + ":" + port) as channel:
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

def getUsers():
    try:
        with grpc.insecure_channel(host + ":" + port) as channel:
            stub = grpc_pb2_grpc.TodoStub(channel)
            message = grpc_pb2.voidNoParam()
            stub.returnItems(message)
            # print(response)
    except Exception:
        print("deu erro na visualizacao geral")

######### Update method #########
def updateUser():
    idInput = int(input("Digite o ID do usuario a ser atualizado: "))
    response = getUser(idInput)
    if response:
        print("\n\nUsuario encontrado")
        print("Atualizando Usuario".center(50, "="))
        
        #Preenchendo valores para serem atualizados
        formatUserData = fillUSerData()

        dictValuesString = str(formatUserData)

        with grpc.insecure_channel(host + ":" + port) as channel:
            stub = grpc_pb2_grpc.TodoStub(channel)

            try:
                response = stub.updateUser(grpc_pb2.UpdateUserRequest(id = idInput, payload = dictValuesString))
                id0 = response.id
                print(f"\n\nRequisicao enviada. ID do usuario atualizado: {id0}")
                # print(f"{time.time() - start} : resp={response.id} and txt={response.txt}: pid={pid}")
                time.sleep(0.001)
            except KeyboardInterrupt: 
                print("\nKeyboardInterrupt solicitada pelo usuario")
                channel.unsubscribe(close)
                exit()
    
        # print(response)
    else:
        print("Usuario nao encontrado")
    # with grpc.insecure_channel(host + ":" + port) as channel:
    #     stub = grpc_pb2_grpc.TodoStub(channel)
    #     response = stub.checkItem(grpc_pb2.Item(id = idInput))
    #     print("aqui vai a resposta")
    #     print(response)

######### Delete method #########
def deleteUser():
    idInput = int(input("Digite o ID do usuario a ser removido: "))
    response = getUser(idInput)
    if response:
        with grpc.insecure_channel(host + ":" + port) as channel:
            stub = grpc_pb2_grpc.TodoStub(channel)

            try:
                response = stub.deleteUser(grpc_pb2.getUserRequest(id = idInput))
                id0 = response.id
                print(f"\nRequisicao enviada. Usuario de ID {idInput} removido")
                # print(f"{time.time() - start} : resp={response.id} and txt={response.txt}: pid={pid}")
                time.sleep(0.001)
            except KeyboardInterrupt: 
                print("\nKeyboardInterrupt solicitada pelo usuario")
                channel.unsubscribe(close)
                exit()
    else:
        print("Erro ao excluir usuario")



def run():   
    # pid = os.getpid()
    try:
        tipoUsuario = userType()
        if tipoUsuario == 1: #admin
            while True:
                userActionAdmin()
        else:
            while True:
                userActionClient()
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
    print("iniciando client")
    run()
