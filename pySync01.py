from time import sleep
import plyvel
import pysyncobj
from pysyncobj import SyncObjConf, replicated_sync, replicated
from functools import partial

ports = ["20000", "20001", "20002"]
encoding = "UTF-8"

class MyCounter(pysyncobj.SyncObj):
    def __init__(self, listaHosts, DbFile):
        print(listaHosts)
        try:
            cfg = SyncObjConf(dynamicMembershipChange = True, commandsQueueSize=1)
            super(MyCounter, self).__init__("localhost:"+str(listaHosts[0]), ["localhost:"+str(listaHosts[1]), "localhost:"+str(listaHosts[2])], cfg)
            self.__data = {}
            self.__databasePort = DbFile
            self.db = self.initDatabase()
        except:
            print("Erro na inicializacao da classe")

    def initDatabase(self):
        db = plyvel.DB('/tmp/levelDb' + str(self.__databasePort), create_if_missing=True)
        pysyncobj.replicated()
        if(db.closed):
            print("DB Fechado")
        else:
            print("DB Aberto")
            return db
    
    @replicated_sync  
    def insertKV(self, key, value):
        try:
            self.db.put(bytes(key, encoding), bytes(value, encoding))
            print("Valor inserido ou atualizado com sucesso")
        except:
            print("Erro na insercao do valor")

    @replicated_sync
    def deleteKV(self, key):
        try:
            self.db.delete(bytes(key, encoding))
            print("Valor excluido com sucesso")
        except:
            print("Erro na exclusao do valor")

    def getValue(self, key):
        return self.db.get(bytes(key, encoding))

    def initServer(self):
        while True:
            print("1 - Inserir chave:valor")
            print("2 - Retornar valor, por chave")
            print("3 - Excluir valor")
            typeServer = int(input("Digite a operacao desejada (-1 para retornar): "))
            if(typeServer == 1):
                while True:
                    key = input("Digite para continuar: ")
                    if key == "-1":
                        break
                    value = input("Digite para continuar 2: ")
                    instancia.insertKV(key, value)
                    print(self.getValue(key))
                    sleep(1)
            elif(typeServer == 2):
                while True:
                    choose = str(input("Digite a chave para retornar o valor: "))
                    if choose == "-1":
                        break
                    print(self.getValue(choose))
            elif(typeServer == 3):
                while True:
                    choose = str(input("Digite a chave excluir o valor: "))
                    if choose == "-1":
                        break
                    self.deleteKV(choose)
        
hosts = ["5000", "5001", "5002"]

def eleicao():
    print("Eleicao")
    while True:
        if(instancia.isReady()) == True:
            print(instancia._getLeader())
            print("Pronto")
            break
        else:
            print(".")
            sleep(1)

def serverId():
    print(" 1 - localhost:5000")
    print(" 2 - localhost:5001")
    print(" 3 - localhost:5002")
    choose = int(input("Digite o ID do server: "))
    if choose == 1:
        return [[hosts[0], hosts[1], hosts[2]], "01"]
    if choose == 2:
        return [[hosts[1], hosts[0], hosts[2]], "02"]
    if choose == 3:
        return [[hosts[2], hosts[0], hosts[1]], "03"]

id = serverId()
instancia = MyCounter(id[0], id[1])
eleicao()
instancia.initServer()
