# RabbitMQ Consumer/Producer em Node.js

Este diretório contém um exemplo básico de consumer e producer para RabbitMQ usando Node.js.

## Dependências

- Node.js 14+
- RabbitMQ Server
- Biblioteca `amqplib`

## Instalação

1. Instale as dependências:
```bash
npm install
```

2. Certifique-se de que o RabbitMQ está rodando no seu sistema:
```bash
sudo systemctl start rabbitmq-server
# ou
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

## Uso

### Consumer (basic.js)

O consumer irá:
- Criar automaticamente a exchange `basic_exchange` (tipo direct, durável)
- Criar automaticamente a queue `basic_queue` (durável)
- Conectar a queue à exchange usando a routing key `basic.message`
- Consumir mensagens e imprimi-las no console

Para executar o consumer:
```bash
npm start
# ou
node basic.js
```

### Producer (producer.js)

O producer envia mensagens para a exchange que serão consumidas pelo consumer.

Para enviar uma mensagem:
```bash
node producer.js "Minha mensagem de teste"
# ou usando o script npm
npm run producer "Minha mensagem de teste"
```

Para enviar mensagens de teste automaticamente:
```bash
node producer.js --test
```

## Configurações

### Exchange
- **Nome**: `basic_exchange`
- **Tipo**: `direct`
- **Durável**: `true`

### Queue
- **Nome**: `basic_queue`
- **Durável**: `true`
- **Routing Key**: `basic.message`

### Conexão RabbitMQ
- **URL**: `amqp://guest:guest@localhost:5672/`

## Funcionalidades

### Consumer
- ✅ Cria exchange e queue automaticamente se não existirem
- ✅ Conecta queue à exchange com routing key
- ✅ Processa mensagens com acknowledgment manual
- ✅ Logging detalhado com timestamps
- ✅ Tratamento de erros robusto
- ✅ QoS configurado para processar uma mensagem por vez
- ✅ Graceful shutdown com CTRL+C ou SIGTERM
- ✅ Código modular e reutilizável

### Producer
- ✅ Envia mensagens com timestamp e metadados
- ✅ Mensagens persistentes
- ✅ Logging detalhado
- ✅ Tratamento de erros
- ✅ Suporte a múltiplas mensagens
- ✅ Modo de teste integrado

## Scripts NPM

```bash
npm start          # Inicia o consumer
npm run producer   # Executa o producer (precisa passar argumentos)
```

## Teste

1. Em um terminal, execute o consumer:
```bash
npm start
```

2. Em outro terminal, envie uma mensagem:
```bash
node producer.js "Teste de mensagem do Node.js"
```

3. Para testar com múltiplas mensagens:
```bash
node producer.js --test
```

4. Observe as mensagens sendo consumidas no terminal do consumer.

## Estrutura do Projeto

```
node/
├── package.json        # Dependências e scripts
├── basic.js           # Consumer RabbitMQ
├── producer.js        # Producer RabbitMQ
└── README.md          # Esta documentação
```

## Exemplo de Output

### Consumer:
```
Conectando ao RabbitMQ...
Conexão com RabbitMQ estabelecida
Exchange 'basic_exchange' declarada
Queue 'basic_queue' declarada
Queue 'basic_queue' conectada à exchange 'basic_exchange' com routing key 'basic.message'
Consumer iniciado. Aguardando mensagens...
Para sair, pressione CTRL+C
[2025-08-08T18:13:45.123Z] Mensagem recebida: {"content":"Teste","timestamp":"2025-08-08T18:13:45.120Z","sender":"producer"}
[2025-08-08T18:13:45.124Z] Processando mensagem: {"content":"Teste","timestamp":"2025-08-08T18:13:45.120Z","sender":"producer"}
[2025-08-08T18:13:45.225Z] Mensagem processada com sucesso
```

### Producer:
```
Conectando ao RabbitMQ...
Mensagem enviada: Teste de mensagem do Node.js
```
