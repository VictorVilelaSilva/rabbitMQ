# setup.py
import pika

RABBIT_URL = "amqp://localhost"
EX_MAIN = "ex.main"
EX_DLX  = "ex.dlx"
Q_MAIN  = "q.main"
Q_DLQ   = "q.dlq"
RK_MAIN = "rk.processar"
RK_DLX  = "rk.erro"

MAX_RETRY = 3  # máximo de 3 tentativas

ch = pika.BlockingConnection(pika.URLParameters(RABBIT_URL)).channel()

# exchanges
ch.exchange_declare(EX_MAIN, "direct", durable=True)
ch.exchange_declare(EX_DLX,  "direct", durable=True)


ch.queue_declare(Q_DLQ, durable=True)
ch.queue_bind(Q_DLQ, EX_DLX, RK_DLX)

# fila principal com DLX
args = {
  "x-dead-letter-exchange": EX_DLX,
  "x-dead-letter-routing-key": RK_DLX,
  # "x-message-ttl": 5000,   # opcional: expirar e ir pra DLX
  # "x-max-length": 1000,    # opcional: lotou -> DLX (conforme policy)
}
ch.queue_declare(Q_MAIN, durable=True, arguments=args)
ch.queue_bind(Q_MAIN, EX_MAIN, RK_MAIN)

# publica 1 msg com retry counter nos headers
import json

message_body = json.dumps({"id": 1, "data": "teste de processamento"})
headers = {"retry_count": 0}  # inicializa o contador de retry
properties = pika.BasicProperties(
    delivery_mode=2,
    headers=headers
)

ch.basic_publish(EX_MAIN, RK_MAIN, message_body.encode(), properties)
