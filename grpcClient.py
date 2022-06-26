import email
import os
import time
import grpc
import grpc_pb2
import grpc_pb2_grpc

host = "localhost"
port = "10000"

def userAction():
    print("MENU".center(50, "="))
    print(" 1 - Criar usuario")
    print(" 2 - Retornar usuarios")
    print(" 3 - Retornar usuario especifico")
    print(" 4 - Atualizar usuario")
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

    elif choose == 9:
        print("Encerrando client")
        exit()
    else:
        print("Opcao invalida")
    
def createUser():
    id0 = 0
    with grpc.insecure_channel(host + ":" + port) as channel:
        stub = grpc_pb2_grpc.TodoStub(channel)
        nomeInput = input("Digite o nome: ")
        emailInput = input("Digite o email: ")
        idadeInput = int(input("Digite a idade: "))
        
        
        dictValues = {"nome":nomeInput, "email":emailInput, "idade":idadeInput}
        dictValuesString = str(dictValues)
        
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

def updateUser():
    idInput = int(input("Digite o ID do usuario a ser atualizado: "))
    with grpc.insecure_channel(host + ":" + port) as channel:
        stub = grpc_pb2_grpc.TodoStub(channel)
        response = stub.checkItem(grpc_pb2.Item(id = idInput))
        print("aqui vai a resposta")
        print(response)

def getUser():
    with grpc.insecure_channel(host + ":" + port) as channel:
        stub = grpc_pb2_grpc.TodoStub(channel)
        id0 = int(input("Digite o id do usuario: "))
        message = grpc_pb2.getUserRequest(id=id0)
        response = stub.getUser(message)
        print("Usuario buscado")
        print(response)

def getUsers():
    with grpc.insecure_channel(host + ":" + port) as channel:
        stub = grpc_pb2_grpc.TodoStub(channel)
        message = grpc_pb2.voidNoParam()
        response = stub.returnItems(message)
        print(response)

def run():   
    # pid = os.getpid()
    try:
        while True:
            userAction()
    except KeyboardInterrupt: 
        print("\nKeyboardInterrupt solicitada pelo usuario")
        exit()
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
