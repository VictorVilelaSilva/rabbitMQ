const amqp = require('amqplib');

// Configurações do RabbitMQ
const RABBITMQ_CONFIG = {
    url: 'amqp://guest:guest@localhost:5672/',
    exchange: 'basic_exchange',
    queue: 'basic_queue',
    routingKey: 'basic.message'
};

/**
 * Função para processar mensagens recebidas
 * @param {Object} msg - Mensagem recebida do RabbitMQ
 * @param {Object} channel - Canal do RabbitMQ
 */
async function processMessage(msg, channel) {
    try {
        const messageContent = msg.content.toString();
        const timestamp = new Date().toISOString();

        console.log(`[${timestamp}] Mensagem recebida: ${messageContent}`);

        // Aqui você pode processar a mensagem como necessário
        console.log(`[${timestamp}] Processando mensagem: ${messageContent}`);

        // Simular algum processamento (opcional)
        await new Promise(resolve => setTimeout(resolve, 100));

        // Confirmar que a mensagem foi processada com sucesso
        channel.ack(msg);
        console.log(`[${timestamp}] Mensagem processada com sucesso`);

    } catch (error) {
        console.error(`Erro ao processar mensagem: ${error.message}`);
        // Rejeitar a mensagem e recolocá-la na fila
        channel.nack(msg, false, true);
    }
}

/**
 * Configura a conexão, exchange e queue do RabbitMQ
 * @returns {Promise<Object>} Retorna conexão e canal
 */
async function setupRabbitMQ() {
    try {
        console.log('Conectando ao RabbitMQ...');

        // Estabelecer conexão
        const connection = await amqp.connect(RABBITMQ_CONFIG.url);
        const channel = await connection.createChannel();

        console.log('Conexão com RabbitMQ estabelecida');

        // Declarar exchange (será criada se não existir)
        await channel.assertExchange(RABBITMQ_CONFIG.exchange, 'direct', {
            durable: true
        });
        console.log(`Exchange '${RABBITMQ_CONFIG.exchange}' declarada`);

        // Declarar queue (será criada se não existir)
        await channel.assertQueue(RABBITMQ_CONFIG.queue, {
            durable: true
        });
        console.log(`Queue '${RABBITMQ_CONFIG.queue}' declarada`);

        // Conectar a queue à exchange usando routing key
        await channel.bindQueue(
            RABBITMQ_CONFIG.queue,
            RABBITMQ_CONFIG.exchange,
            RABBITMQ_CONFIG.routingKey
        );
        console.log(`Queue '${RABBITMQ_CONFIG.queue}' conectada à exchange '${RABBITMQ_CONFIG.exchange}' com routing key '${RABBITMQ_CONFIG.routingKey}'`);

        return { connection, channel };

    } catch (error) {
        console.error('Erro ao configurar RabbitMQ:', error.message);

        if (error.code === 'ECONNREFUSED') {
            console.error('Erro: Não foi possível conectar ao RabbitMQ. Verifique se o servidor está rodando.');
        }

        process.exit(1);
    }
}

/**
 * Inicia o consumer RabbitMQ
 */
async function startConsumer() {
    try {
        const { connection, channel } = await setupRabbitMQ();

        // Configurar QoS para processar uma mensagem por vez
        await channel.prefetch(1);

        console.log('Consumer iniciado. Aguardando mensagens...');
        console.log('Para sair, pressione CTRL+C');

        // Configurar o consumer
        await channel.consume(RABBITMQ_CONFIG.queue, (msg) => {
            if (msg !== null) {
                processMessage(msg, channel);
            }
        }, {
            noAck: false // Desabilitar auto-acknowledge para controle manual
        });

        // Tratamento de sinais para graceful shutdown
        process.on('SIGINT', async () => {
            console.log('\nParando o consumer...');
            await channel.close();
            await connection.close();
            console.log('Consumer parado');
            process.exit(0);
        });

        process.on('SIGTERM', async () => {
            console.log('\nParando o consumer...');
            await channel.close();
            await connection.close();
            console.log('Consumer parado');
            process.exit(0);
        });

    } catch (error) {
        console.error('Erro no consumer:', error.message);
        process.exit(1);
    }
}

// Iniciar o consumer se este arquivo for executado diretamente
if (require.main === module) {
    startConsumer();
}

module.exports = { startConsumer, setupRabbitMQ, processMessage };