import pika
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def callback(ch, method, properties, body):
    """
    Função callback que será executada quando uma mensagem for recebida
    """
    try:
        message = body.decode('utf-8')
        logger.info(f"Mensagem recebida: {message}")
        
        # Aqui você pode processar a mensagem como necessário
        print(f"Processando mensagem: {message}")
        
        # Confirmar que a mensagem foi processada com sucesso
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}")
        # Rejeitar a mensagem e recolocá-la na fila
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def setup_rabbitmq():
    """
    Configura a conexão, exchange e queue do RabbitMQ
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
        
        logger.info("Conexão com RabbitMQ estabelecida")
        
        # Configurações da exchange e queue
        exchange_name = 'basic_exchange'
        queue_name = 'basic_queue'
        routing_key = 'basic.message'
        
        # Declarar exchange
        channel.exchange_declare(
            exchange=exchange_name,
            exchange_type='direct',
            durable=True
        )

        # Declarar queue
        channel.queue_declare(
            queue=queue_name,
            durable=True
        )

        # Conectar a queue à exchange usando routing key
        channel.queue_bind(
            exchange=exchange_name,
            queue=queue_name,
            routing_key=routing_key
        )
        
        return connection, channel, queue_name
        
    except pika.exceptions.AMQPConnectionError:
        logger.error("Erro: Não foi possível conectar ao RabbitMQ. Verifique se o servidor está rodando.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erro ao configurar RabbitMQ: {e}")
        sys.exit(1)

def start_consumer():
    """
    Inicia o consumer RabbitMQ
    """
    connection, channel, queue_name = setup_rabbitmq()
    
    try:
        # Configurar QoS para processar uma mensagem por vez
        channel.basic_qos(prefetch_count=1)
        
        # Configurar o consumer
        channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=False  # Desabilitar auto-acknowledge para controle manual
        )
        
        logger.info("Consumer iniciado. Aguardando mensagens...")
        logger.info("Para sair, pressione CTRL+C")
        
        # Iniciar o loop de consumo
        channel.start_consuming()
        
    except KeyboardInterrupt:
        logger.info("Parando o consumer...")
        channel.stop_consuming()
        connection.close()
        logger.info("Consumer parado")
    except Exception as e:
        logger.error(f"Erro no consumer: {e}")
        connection.close()
        sys.exit(1)

if __name__ == '__main__':
    start_consumer()