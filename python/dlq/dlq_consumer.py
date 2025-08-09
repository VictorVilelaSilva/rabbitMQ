# dlq_consumer.py
import pika
import json
from datetime import datetime

RABBIT_URL = "amqp://localhost"
Q_DLQ = "q.dlq"
EX_MAIN = "ex.main"
RK_MAIN = "rk.processar"
MAX_RETRY = 3

conn = pika.BlockingConnection(pika.URLParameters(RABBIT_URL))
ch = conn.channel()
ch.basic_qos(prefetch_count=1)

def on_dlq_msg(chx, method, props, body):
    try:
        message = body.decode()
        print(f"[DLQ] processando mensagem da DLQ: {message}")
        
        # Pega o contador de retry dos headers
        retry_count = 0
        if props.headers and 'retry_count' in props.headers:
            retry_count = props.headers['retry_count']
        
        # Incrementa o contador de retry
        retry_count += 1
        print(f"[DLQ] incrementando retry_count para: {retry_count}")
        
        if retry_count <= MAX_RETRY:
            # Ainda tem tentativas restantes, reenvia para fila principal
            new_headers = props.headers or {}
            new_headers['retry_count'] = retry_count
            
            properties = pika.BasicProperties(
                delivery_mode=2,
                headers=new_headers
            )
            
            print(f"[DLQ] reenviando para fila principal. Tentativa {retry_count}/{MAX_RETRY}")
            chx.basic_publish(EX_MAIN, RK_MAIN, body, properties)
            chx.basic_ack(method.delivery_tag)
        else:
            # Excedeu o número máximo de tentativas - descarta a mensagem
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[DLQ] {timestamp} - DESCARTANDO mensagem após {MAX_RETRY} tentativas:")
            print(f"[DLQ] Conteúdo: {message}")
            print(f"[DLQ] Tentativas realizadas: {retry_count}")
            print(f"[DLQ] Headers: {props.headers}")
            print("-" * 50)
            
            # Simplesmente confirma a mensagem (descarta)
            chx.basic_ack(method.delivery_tag)
            
    except Exception as e:
        print(f"[DLQ] erro no processamento da DLQ: {e}")
        chx.basic_reject(method.delivery_tag, requeue=False)

ch.basic_consume(Q_DLQ, on_message_callback=on_dlq_msg, auto_ack=False)
print(f"[DLQ] Consumindo DLQ com max retry = {MAX_RETRY}. CTRL+C para sair.")
ch.start_consuming()