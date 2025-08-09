# consumer.py
import pika
import json
from datetime import datetime

RABBIT_URL = "amqp://localhost"
Q_MAIN = "q.main"
MAX_RETRY = 3

conn = pika.BlockingConnection(pika.URLParameters(RABBIT_URL))
ch = conn.channel()
ch.basic_qos(prefetch_count=1)

def on_msg(chx, method, props, body):
    try:
        # Decodifica a mensagem
        message = body.decode()
        print(f"[MAIN] recebido: {message}")
        
        # Pega o contador de retry dos headers
        retry_count = 0
        if props.headers and 'retry_count' in props.headers:
            retry_count = props.headers['retry_count']
        
        print(f"[MAIN] tentativa número: {retry_count + 1}")
        
        # Simula falha no processamento
        # Aqui você colocaria sua lógica de processamento real
        success = process_message(message)
        
        if success:
            # Processamento bem-sucedido
            print(f"[MAIN] processado com sucesso!")
            chx.basic_ack(method.delivery_tag)
        else:
            # Falha no processamento
            if retry_count < MAX_RETRY:
                # Ainda tem tentativas restantes, rejeita para DLQ
                print(f"[MAIN] falha no processamento. Tentativa {retry_count + 1}/{MAX_RETRY}. Enviando para DLQ...")
                chx.basic_reject(method.delivery_tag, requeue=False)
            else:
                # Excedeu o número máximo de tentativas - descarta a mensagem
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[MAIN] {timestamp} - DESCARTANDO mensagem após {MAX_RETRY} tentativas:")
                print(f"[MAIN] Conteúdo: {message}")
                print(f"[MAIN] Headers: {props.headers}")
                print("-" * 50)
                
                # Simplesmente confirma a mensagem (descarta)
                chx.basic_ack(method.delivery_tag)
                
    except Exception as e:
        print(f"[MAIN] erro no processamento: {e}")
        chx.basic_reject(method.delivery_tag, requeue=False)

def process_message(message):
    """
    Simula o processamento da mensagem.
    Retorna True para sucesso, False para falha.
    """
    # Simula falha permanente para demonstração
    # Na vida real, aqui seria sua lógica de negócio
    return False  # Mude para True para testar sucesso

ch.basic_consume(Q_MAIN, on_message_callback=on_msg, auto_ack=False)
print("Consumindo só q.main (DLQ fica sem consumer). CTRL+C p/ sair.")
ch.start_consuming()
