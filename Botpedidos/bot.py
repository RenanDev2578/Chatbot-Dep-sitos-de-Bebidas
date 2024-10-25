import telebot
from telebot import types

# Chave da API do bot
API = "S8073508771:AAEdPDi94Ot_tuDxdVx5K1MhBGXriNAwhrQ"
bot = telebot.TeleBot(API)

# Dicionário para armazenar pedidos em andamento
pedidos = {}

# Função de boas-vindas
@bot.message_handler(commands=["start"])
def send_welcome(mensagem):
    # Cria o menu de opções com os botões
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    pedido_btn = types.KeyboardButton('🍻 Fazer Pedido')
    contato_btn = types.KeyboardButton('📞 Opções de Contato')
    preco_btn = types.KeyboardButton('💲 Ver Preços dos Produtos')
    markup.add(pedido_btn, contato_btn, preco_btn)

   
    welcome_message = (
        "🍺 **Bem-vindo ao Depósito de Bebidas!** 🍺\n"
        "Escolha uma opção abaixo e aproveite nossos serviços! 👇"
    )
    bot.send_message(mensagem.chat.id, welcome_message, parse_mode='Markdown', reply_markup=markup)

# Função para fazer pedido
@bot.message_handler(func=lambda mensagem: mensagem.text == '🍻 Fazer Pedido')
def fazer_pedido(mensagem):
   
    texto = "Por favor, envie o nome do produto e a quantidade desejada."
    bot.send_message(mensagem.chat.id, texto)
    bot.register_next_step_handler(mensagem, processar_pedido)

# Função para processar o pedido
def processar_pedido(mensagem):
    try:
        # Divide a mensagem em quantidade e produto
        partes = mensagem.text.split(maxsplit=1)
        quantidade = int(partes[0])
        produto = partes[1] if len(partes) > 1 else ''

        # Armazena o pedido no dicionário
        pedidos[mensagem.chat.id] = {'produto': produto, 'quantidade': quantidade}

        # Mostra o resumo do pedido e pede confirmação
        resumo_pedido = f"Você pediu {quantidade} de {produto}. Deseja confirmar o pedido? (Sim/Não)"
        bot.send_message(mensagem.chat.id, resumo_pedido)
        bot.register_next_step_handler(mensagem, confirmar_pedido)
    except (ValueError, IndexError):
        # Mensagem de erro caso o formato esteja errado
        bot.send_message(mensagem.chat.id, "Por favor, use o formato correto: 'quantidade produto'.")

# Função para confirmar o pedido
def confirmar_pedido(mensagem):
    if mensagem.text.lower() == 'sim':
        # Solicita o contato do cliente
        bot.send_message(mensagem.chat.id, "Por favor, informe seu contato (telefone ou email).")
        bot.register_next_step_handler(mensagem, coletar_contato)
    else:
        # Cancela o pedido
        bot.send_message(mensagem.chat.id, "Pedido cancelado.")

# Função para coletar o contato do usuário
def coletar_contato(mensagem):
    contato = mensagem.text
    pedidos[mensagem.chat.id]['contato'] = contato
    # Solicita o endereço do cliente
    bot.send_message(mensagem.chat.id, "Agora, informe seu endereço.")
    bot.register_next_step_handler(mensagem, coletar_endereco)

# Função para coletar o endereço do usuário
def coletar_endereco(mensagem):
    endereco = mensagem.text
    pedidos[mensagem.chat.id]['endereco'] = endereco

    # Mostra o resumo do pedido com todas as informações
    resumo = (
        f"📦 **Resumo do Pedido:**\n"
        f"Produto: {pedidos[mensagem.chat.id]['quantidade']} de {pedidos[mensagem.chat.id]['produto']}\n"
        f"Contato: {pedidos[mensagem.chat.id]['contato']}\n"
        f"Endereço: {pedidos[mensagem.chat.id]['endereco']}\n"
        "Deseja confirmar o pedido? (Sim/Não)"
    )
    bot.send_message(mensagem.chat.id, resumo, parse_mode='Markdown')
    bot.register_next_step_handler(mensagem, finalizar_pedido)

# Função para finalizar o pedido e gerar relatório automaticamente
def finalizar_pedido(mensagem):
    if mensagem.text.lower() == 'sim':
        # Confirma o pedido e gera o relatório
        bot.send_message(mensagem.chat.id, "🎉 Pedido confirmado! Obrigado por comprar conosco!")
        gerar_relatorio_automatico(mensagem)
    else:
        # Cancela o pedido
        bot.send_message(mensagem.chat.id, "Pedido cancelado.")

# Função para gerar o relatório automaticamente após confirmação

def gerar_relatorio_automatico(mensagem):
    info = pedidos.get(mensagem.chat.id)
    if info:

        # Relatório do pedido
        relatorio = (
            "📊 **Relatório do Pedido:**\n\n"
            f"🛒 **Usuário:** {mensagem.chat.id}\n"
            f"Produto: {info['quantidade']}x {info['produto']}\n"
            f"Contato: {info['contato']}\n"
            f"Endereço: {info['endereco']}\n"
        )
        
        # Envia o relatório para o próprio usuário
        bot.send_message(mensagem.chat.id, relatorio, parse_mode='Markdown')
        
        # Envia o relatório para o administrador (substitua pelo ID do admin)
        ADM_ID = '7998708133:AAEPvWGQw0Aeq-E-KZbv5xYSEl9_ZnciZWg'
        bot.send_message(ADM_ID, relatorio, parse_mode='Markdown')

# Função para exibir preços dos produtos
@bot.message_handler(func=lambda mensagem: mensagem.text == '💲 Ver Preços dos Produtos')
def mostrar_precos(mensagem):
    produtos = (
        "💲 **Preços dos Produtos:** 💲\n"
        "- Cerveja AMSTEL: R$ 5,00\n"
        "- Refrigerante Coca: R$ 5,00\n"
        "- Água Mineral: R$ 2,50\n"
        "- Vodka: R$ 150,00\n"
    )
    bot.send_message(mensagem.chat.id, produtos, parse_mode='Markdown')

# Função para opções de contato
@bot.message_handler(func=lambda mensagem: mensagem.text == '📞 Opções de Contato')
def opcoes_contato(mensagem):
    contatos = (
        "📞 **Nossas opções de contato:**\n"
        "- Telefone: (75)983126821\n"
        "- Email: renancarvalho1850s@gmail.com\n"
        "- WhatsApp: (75)983126821"
    )
    bot.send_message(mensagem.chat.id, contatos)

# Função para lidar com mensagens não reconhecidas
def verificar(mensagem):
    return True

@bot.message_handler(func=verificar)
def responder(mensagem):
    texto = """
    Escolha uma opção para continuar (Clique no item):
     🍻 Fazer Pedido
     📞 Opções de Contato
     💲 Ver Preços dos Produtos
    """
    bot.reply_to(mensagem, texto)

# Mantém o bot funcionando
bot.polling()






