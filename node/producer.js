const amqp = require('amqplib');

// Configurações do RabbitMQ
const RABBITMQ_CONFIG = {
    url: 'amqp://guest:guest@localhost:5672/',
    exchange: 'basic_exchange',
    routingKey: 'basic.message'
};

/**
 * Envia uma mensagem para o RabbitMQ
 * @param {string} message - A mensagem a ser enviada
 */
async function sendMessage(message) {
    let connection;
    let channel;

    try {
        console.log('Conectando ao RabbitMQ...');

        // Estabelecer conexão
        connection = await amqp.connect(RABBITMQ_CONFIG.url);
        channel = await connection.createChannel();

        // Declarar exchange (caso não exista)
        await channel.assertExchange(RABBITMQ_CONFIG.exchange, 'direct', {
            durable: true
        });

        // Preparar a mensagem
        const messageData = {
            content: message,
            timestamp: new Date().toISOString(),
            sender: 'producer'
        };

        const messageBuffer = Buffer.from(JSON.stringify(messageData));

        // Publicar mensagem
        const published = channel.publish(
            RABBITMQ_CONFIG.exchange,
            RABBITMQ_CONFIG.routingKey,
            messageBuffer,
            {
                persistent: true, // Tornar a mensagem persistente
                timestamp: Date.now()
            }
        );

        if (published) {
            console.log(`Mensagem enviada: ${message}`);
        } else {
            console.error('Falha ao enviar mensagem');
        }

    } catch (error) {
        console.error('Erro ao enviar mensagem:', error.message);

        if (error.code === 'ECONNREFUSED') {
            console.error('Erro: Não foi possível conectar ao RabbitMQ. Verifique se o servidor está rodando.');
        }

        process.exit(1);
    } finally {
        // Fechar conexão
        if (channel) {
            await channel.close();
        }
        if (connection) {
            await connection.close();
        }
    }
}

/**
 * Envia múltiplas mensagens para teste
 * @param {Array<string>} messages - Array de mensagens para enviar
 */
async function sendMultipleMessages(messages) {
    for (const message of messages) {
        await sendMessage(message);
        // Pequeno delay entre mensagens
        await new Promise(resolve => setTimeout(resolve, 500));
    }
}

// Processar argumentos da linha de comando
if (require.main === module) {
    const args = process.argv.slice(2);

    if (args.length === 0) {
        console.log('Uso: node producer.js "sua mensagem aqui"');
        console.log('Ou: node producer.js --test (para enviar mensagens de teste)');
        process.exit(1);
    }

    if (args[0] === '--test') {
        const testMessages = [
            'Mensagem de teste 1',
            'Mensagem de teste 2',
            'Mensagem de teste 3',
            'Hello from Node.js!',
            'RabbitMQ funcionando!'
        ];

        console.log('Enviando mensagens de teste...');
        sendMultipleMessages(testMessages);
    } else {
        const message = args.join(' ');
        sendMessage(message);
    }
}

module.exports = { sendMessage, sendMultipleMessages };
