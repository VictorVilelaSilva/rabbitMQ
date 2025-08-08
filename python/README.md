# RabbitMQ Consumer/Producer Básico em Python

Este diretório contém um exemplo básico de consumer e producer para RabbitMQ usando Python.

## Dependências

- Python 3.7+
- RabbitMQ Server
- Biblioteca `pika`

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Certifique-se de que o RabbitMQ está rodando no seu sistema:
```bash
sudo systemctl start rabbitmq-server
# ou
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

## Uso

### Consumer (basic.py)

O consumer irá:
- Criar automaticamente a exchange `basic_exchange` (tipo direct, durável)
- Criar automaticamente a queue `basic_queue` (durável)
- Conectar a queue à exchange usando a routing key `basic.message`
- Consumir mensagens e imprimi-las no console

Para executar o consumer:
```bash
python basic.py
```

### Producer (producer.py)

O producer envia mensagens para a exchange que serão consumidas pelo consumer.

Para enviar uma mensagem:
```bash
python producer.py "Minha mensagem de teste"
```

## Configurações

### Exchange
- **Nome**: `basic_exchange`
- **Tipo**: `direct`
- **Durável**: `True`

### Queue
- **Nome**: `basic_queue`
- **Durável**: `True`
- **Routing Key**: `basic.message`

### Conexão RabbitMQ
- **Host**: `localhost`
- **Porta**: `5672`
- **Virtual Host**: `/`
- **Credenciais**: `guest/guest`

## Funcionalidades

### Consumer
- ✅ Cria exchange e queue automaticamente se não existirem
- ✅ Conecta queue à exchange com routing key
- ✅ Processa mensagens com acknowledgment manual
- ✅ Logging detalhado
- ✅ Tratamento de erros
- ✅ QoS configurado para processar uma mensagem por vez
- ✅ Graceful shutdown com CTRL+C

### Producer
- ✅ Envia mensagens com timestamp
- ✅ Mensagens persistentes
- ✅ Logging detalhado
- ✅ Tratamento de erros

## Teste

1. Em um terminal, execute o consumer:
```bash
python basic.py
```

2. Em outro terminal, envie uma mensagem:
```bash
python producer.py "Teste de mensagem"
```

3. Observe a mensagem sendo consumida no terminal do consumer.
