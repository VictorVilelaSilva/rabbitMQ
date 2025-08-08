# RabbitMQ - Exemplos de Consumer/Producer

Este repositório contém exemplos básicos de consumer e producer para RabbitMQ em diferentes linguagens de programação.

## 📁 Estrutura do Projeto

```
rabbitMQ/
├── docker-compose.yml          # RabbitMQ para produção
├── docker-compose.dev.yml      # RabbitMQ para desenvolvimento
├── rabbitmq.sh                 # Script de gerenciamento
├── python/                     # Implementação em Python
│   ├── basic.py                # Consumer Python
│   ├── producer.py             # Producer Python
│   ├── requirements.txt        # Dependências Python
│   └── README.md              # Documentação Python
├── node/                       # Implementação em Node.js
│   ├── basic.js               # Consumer Node.js
│   ├── producer.js            # Producer Node.js
│   ├── package.json           # Dependências Node.js
│   └── README.md             # Documentação Node.js
└── php/                       # Implementação em PHP (futuro)
```

## 🐰 RabbitMQ com Docker

### Início Rápido

1. **Iniciar RabbitMQ (desenvolvimento)**:
```bash
./rabbitmq.sh start
```

2. **Verificar status**:
```bash
./rabbitmq.sh status
```

3. **Acessar Management UI**:
   - URL: http://localhost:15672
   - Usuário: `guest`
   - Senha: `guest`

### Comandos Disponíveis

```bash
./rabbitmq.sh start-dev    # Inicia em modo desenvolvimento
./rabbitmq.sh start        # Inicia em modo produção
./rabbitmq.sh stop         # Para o RabbitMQ
./rabbitmq.sh restart      # Reinicia o RabbitMQ
./rabbitmq.sh logs         # Mostra os logs
./rabbitmq.sh status       # Verifica o status
./rabbitmq.sh clean        # Remove tudo (containers, volumes, etc)
./rabbitmq.sh help         # Mostra ajuda
```

### Credenciais

- **Desenvolvimento** (`docker-compose.dev.yml`):
  - Usuário: `guest`
  - Senha: `guest`
  - URL: `amqp://guest:guest@localhost:5672`

## 🐍 Python

Implementação usando a biblioteca `pika`.

```bash
cd python/
python basic.py                    # Inicia o consumer
python producer.py "mensagem"      # Envia uma mensagem
```

[Ver documentação completa](python/README.md)

## 🟢 Node.js

Implementação usando a biblioteca `amqplib`.

```bash
cd node/
npm start                          # Inicia o consumer
node producer.js "mensagem"        # Envia uma mensagem
node producer.js --test            # Envia mensagens de teste
```

[Ver documentação completa](node/README.md)

## 🚀 Como Usar

### 1. Iniciar RabbitMQ
```bash
./rabbitmq.sh start-dev
```

### 2. Executar Consumer (Python ou Node.js)

**Python:**
```bash
cd python/
python basic.py
```

**Node.js:**
```bash
cd node/
npm start
```

### 3. Enviar Mensagens

**Python:**
```bash
cd python/
python producer.py "Olá do Python!"
```

**Node.js:**
```bash
cd node/
node producer.js "Olá do Node.js!"
```

## 📊 Configurações Padrão

- **Exchange**: `basic_exchange` (direct, durável)
- **Queue**: `basic_queue` (durável)
- **Routing Key**: `basic.message`
- **Porta AMQP**: `5672`
- **Management UI**: `15672`

## 🔧 Requisitos

- Docker e Docker Compose
- Python 3.7+ (para exemplos Python)
- Node.js 14+ (para exemplos Node.js)

## 📝 Funcionalidades

✅ Criação automática de exchange e queue  
✅ Binding automático entre exchange e queue  
✅ Acknowledgment manual de mensagens  
✅ Tratamento de erros robusto  
✅ Mensagens persistentes  
✅ QoS configurado  
✅ Graceful shutdown  
✅ Logging detalhado  
✅ Docker Compose para fácil setup  

## 🆘 Solução de Problemas

### RabbitMQ não conecta
```bash
./rabbitmq.sh status    # Verificar se está rodando
./rabbitmq.sh logs      # Ver logs de erro
```

### Resetar completamente
```bash
./rabbitmq.sh clean     # Remove tudo
./rabbitmq.sh start-dev # Inicia novamente
```

### Verificar portas em uso
```bash
netstat -tlnp | grep :5672   # Porta AMQP
netstat -tlnp | grep :15672  # Management UI
```