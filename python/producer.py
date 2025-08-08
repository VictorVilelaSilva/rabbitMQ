#!/usr/bin/env python3
import pika
import sys
import logging
import json
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def send_message(message):
    """
    Envia uma mensagem para o RabbitMQ
    """
    try:
        # Parâmetros de conexão
        connection_params = pika.ConnectionParameters(
            host='localhost',
            port=5672,
            virtual_host='/',
            credentials=pika.PlainCredentials('guest', 'guest')
        )
        
        # Estabelecer conexão
        connection = pika.BlockingConnection(connection_params)
        channel = connection.channel()
        
        # Configurações da exchange
        exchange_name = 'basic_exchange'
        routing_key = 'basic.message'
        
        # Declarar exchange (caso não exista)
        channel.exchange_declare(
            exchange=exchange_name,
            exchange_type='direct',
            durable=True
        )
        
        # Preparar a mensagem
        message_data = {
            'content': message,
            'timestamp': datetime.now().isoformat(),
            'sender': 'producer'
        }
        
        # Publicar mensagem
        channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=json.dumps(message_data),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Tornar a mensagem persistente
            )
        )
        
        logger.info(f"Mensagem enviada: {message}")
        
        # Fechar conexão
        connection.close()
        
    except pika.exceptions.AMQPConnectionError:
        logger.error("Erro: Não foi possível conectar ao RabbitMQ. Verifique se o servidor está rodando.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem: {e}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python producer.py 'sua mensagem aqui'")
        sys.exit(1)
    
    message = ' '.join(sys.argv[1:])
    send_message(message)
