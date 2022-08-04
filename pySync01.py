from time import sleep
import plyvel
import pysyncobj
from pysyncobj import SyncObjConf, replicated_sync, replicated
from functools import partial

ports = ["20000", "20001", "20002"]
encoding = "UTF-8"

class MyCounter(pysyncobj.SyncObj):
    def __init__(self):
        # try:
            cfg = SyncObjConf(dynamicMembershipChange = True, commandsQueueSize=1)
            super(MyCounter, self).__init__('localhost:5000', ['localhost:5001', 'localhost:5002'], cfg)
            # pysyncobj.replicated()
            self.__data = {}
            # self.db = self.initDatabase()
        # except:
        #     print("erro")

    def initDatabase(self):
        db = plyvel.DB('/tmp/levelDb01', create_if_missing=True)
        pysyncobj.replicated()
        if(db.closed):
            print("DB Fechado")
        else:
            print("DB Aberto")
            return db
    
    @replicated_sync  
    def insertKV(self, key, value):
        # try:
            self.__data[key] = str(value)
            print("a")
            # print(self.db)
            # self.db.put(bytes(key, encoding), bytes(value, encoding))
        # except:
        #     print("Erro na insercao do valor")

    def getValue(self):
        return self.__data


def onAdd(res, err, cnt):
    print('onAdd %d:' % cnt, res, err)

instancia = MyCounter()

while True:
    while True:
        if (instancia._getLeader()) != None:
            print(instancia._getLeader())
            break
        sleep(1)

    val = input("Digite para continuar: ")
    val1 = input("Digite para continuar 2: ")
    # instancia.incCounter()
    instancia.insertKV(val1, val)
    print(instancia.getValue())
    # print(instancia.db.get(b"key1"))