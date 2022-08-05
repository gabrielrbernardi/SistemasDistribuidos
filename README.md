# Atualização
## Implementação
Para a implementação da segunda parte do projeto, foram utilizadas duas bibliotecas, PySyncObj, para fazer o tratamento do consenso entre as três instâncias utilizadas. Cada instância está utilizando o banco de dados LevelDB, de fácil execução e instalação. A biblioteca Plyvel foi a escolhida para utilizar o banco de dados LevelDB.

## Detalhamento para execução
Para execução da segunda etapa, é necessário executar o arquivo `pySync01.py`. Dentro dele, basta seguir as etapas mostradas na tela. Além disso, o vídeo enviado mostra como executar o sistema.

## Arquitetura
A arquitetura geral pode ser vista a seguir:
![Arquitetura do sistema](https://raw.githubusercontent.com/gabrielrbernardi/SistemasDistribuidos/main/Screenshot%202022-08-05%20154006.png?token=GHSAT0AAAAAABVRQ3QQV3HNQEA5APLGVU2CYXNMSBA)

#################################################################
# Implementação
A implementação seguiu o proposto na descrição do projeto (https://paulo-coelho.github.io/ds_notes/projeto/). A comunicação entre as aplicações clientes e aplicações servidores foi feita utilizando gRPC. O envio de dados das aplicações servidores foi feito utilizando o protocolo MQTT, onde para recebimento ou subscrição nos tópicos há um básico serviço servidor que mostra os dados enviados no tópico inscrito. As aplicações servidores fazem o envio das informações para o barramento do MQTT e o mesmo, em etapa futura de implementação fará a consolidação (verificação de valores repetidos em diferentes instâncias, etc) desses dados e futura inserção no banco de dados, após validação dos mesmos. Para armazenamento de informações em cache local, foram utilizados dicionários nativos do Python.

# Detalhamento para execução
Os serviços propostos foram desenvolvidos utilizando Python em sua versão "Python 3.10.4". Estes serviços estão separados em três arquivos. O arquivo "./grpcClient.py" contém as informações para interação com usuário final. Arquivo "./grpcServer.py" possui informações para fazer o gerenciamento das interações dos usuários com sistema, regras de negócio, além de tratar as comunicações via gRPC com usuários e MQTT com servidor mosquitto. Por fim, o arquivo "./mqttServer.py" possui informações básicas para receber os dados enviados pelos servidor gRPC.

![Arquitetura do sistema](https://paulo-coelho.github.io/ds_notes/drawings/instancia_projeto.drawio-0.svg)

# Observações da implementação
Os códigos foram desenvolvidos utilizando Sistema Operacional Ubuntu 22.04, utilizando Python 3.10.4 e pip3 (pip 22.0.2) , logo, os comandos informados nos próximos passos são referentes a esses sistemas.

# Dependências
```shell
$ sudo apt install python3-pip
$ pip3 install grpc
$ pip3 install grpcio
$ pip3 install grpcio-tools
$ sudo apt install mosquitto
$ sudo apt install mosquitto-clients
$ sudo pip3 install plyvel
$ sudo pip3 install pysyncobj
```
Para instalar as dependências, em teoria, o script "./install.sh" é capaz de fazer tais operações. Se não for possível, a execução dos comandos acima ainda podem ser feitas via bash.

# Execução

Abrir um terminal para cada serviço. Feito isso, executar cada linha em terminais diferentes (Linha 1 - Terminal 1, Linha 2 - Terminal 2, etc). Para testar múltiplas instâncias dos serviços, somente as linhas 1 e 2 devem ser executadas para cada instância que será testada. A linha 3, referente ao Mosquitto deverá ser executada unicamente.

```shell
$ python3 grpcClient.py
$ python3 grpcServer.py
$ python3 mqttServer.py
```

# Testes

Iniciar server na porta 10000
$ python3 grpcServer.py
\# digitar 1 e apertar enter.
Observação: Para demais portas, selecionar conforme menu


Abrir arquivo "tests/teste01.txt"
Arquivo utilizado para fazer a criação de dois usuários, duas tarefas e enviar o conteudo de usuários e tarefas para Mosquitto.
Copiar conteúdo do arquivo de texto e colar no terminal.
