#!/bin/bash

# Script para gerenciar o RabbitMQ com Docker Compose

set -e

DEV_COMPOSE_FILE="docker-compose.yml"

show_help() {
    echo "Uso: $0 [COMANDO] [OPÇÕES]"
    echo ""
    echo "Comandos:"
    echo "  start       Inicia o RabbitMQ (produção)"
    echo "  start-dev   Inicia o RabbitMQ (desenvolvimento com guest/guest)"
    echo "  stop        Para o RabbitMQ"
    echo "  restart     Reinicia o RabbitMQ"
    echo "  logs        Mostra os logs do RabbitMQ"
    echo "  status      Mostra o status dos containers"
    echo "  clean       Para e remove containers, volumes e redes"
    echo "  help        Mostra esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  $0 start-dev    # Inicia em modo desenvolvimento"
    echo "  $0 logs         # Acompanha os logs"
    echo "  $0 status       # Verifica se está rodando"
    echo ""
    echo "URLs de acesso:"
    echo "  AMQP: amqp://localhost:5672"
    echo "  Management UI: http://localhost:15672"
    echo ""
    echo "Credenciais:"
    echo "  Produção: admin/admin123"
    echo "  Desenvolvimento: guest/guest"
}


start() {
    echo "🐰 Iniciando RabbitMQ (Desenvolvimento)..."
    docker-compose -f $DEV_COMPOSE_FILE up -d
    echo "✅ RabbitMQ iniciado em modo desenvolvimento!"
    echo "📊 Management UI: http://localhost:15672 (guest/guest)"
    echo "🔌 AMQP: amqp://guest:guest@localhost:5672"
}

stop_rabbitmq() {
    echo "🛑 Parando RabbitMQ..."
    docker-compose -f $DEV_COMPOSE_FILE down 2>/dev/null || true
    echo "✅ RabbitMQ parado!"
}

restart_rabbitmq() {
    echo "🔄 Reiniciando RabbitMQ..."
    stop_rabbitmq
    sleep 2
    start_dev
}

show_logs() {
    echo "📋 Logs do RabbitMQ:"
    if docker ps --format "table {{.Names}}" | grep -q "rabbitmq-server-dev"; then
        docker-compose -f $DEV_COMPOSE_FILE logs -f
    else
        echo "❌ RabbitMQ não está rodando"
        exit 1
    fi
}

show_status() {
    echo "📊 Status dos containers RabbitMQ:"
    echo ""
    
    if docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -q "rabbitmq"; then
        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep "rabbitmq"
        echo ""
        echo "✅ RabbitMQ está rodando!"
        
        # Verificar qual versão está rodando
        if docker ps --format "table {{.Names}}" | grep -q "rabbitmq-server-dev"; then
            echo "🔧 Modo: Desenvolvimento (guest/guest)"
        elif docker ps --format "table {{.Names}}" | grep -q "rabbitmq-server"; then
            echo "🚀 Modo: Produção (admin/admin123)"
        fi
        
        echo "📊 Management UI: http://localhost:15672"
    else
        echo "❌ RabbitMQ não está rodando"
        echo ""
        echo "Para iniciar:"
        echo "  $0 start-dev    # Para desenvolvimento"
        echo "  $0 start        # Para produção"
    fi
}

clean_all() {
    echo "🧹 Limpando containers, volumes e redes..."
    docker-compose -f $DEV_COMPOSE_FILE down -v --remove-orphans 2>/dev/null || true
    
    # Remover volumes órfãos relacionados ao RabbitMQ
    docker volume ls -q | grep -E "(rabbitmq|rabbit)" | xargs -r docker volume rm 2>/dev/null || true
    
    echo "✅ Limpeza concluída!"
}

case "${1:-help}" in
    start)
        start
        ;;
    stop)
        stop_rabbitmq
        ;;
    restart)
        restart_rabbitmq
        ;;
    logs)
        show_logs
        ;;
    status)
        show_status
        ;;
    clean)
        clean_all
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "❌ Comando inválido: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
