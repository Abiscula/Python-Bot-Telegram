import telebot
import busca_cep
from config import API_TOKEN

BOT = telebot.TeleBot(API_TOKEN) #Criação do bot


def formatted_output(text):
    uni_Code = '\n\n' + ('\U00002796' * 20) + '\n\n '
    return uni_Code + text + uni_Code


@BOT.message_handler(commands=['Clique_aqui'])
def input_zip_code(message):
    text = '            \U0000270F      Certo, digite o CEP para consulta:'
    sent_msg = BOT.send_message(message.chat.id, formatted_output(text))
    BOT.register_next_step_handler(sent_msg, search_zip_code) #chama a próxima função
    
    
@BOT.message_handler(commands=['Sair'])
def exit(message):
    user_name = message.from_user.first_name
    text = f'       Obrigado por utilizar o BuscaCEP {user_name},\n\n       volte sempre!   \U0001F601 \U0001F601'
    BOT.send_message(message.chat.id, formatted_output(text))
    

def search_zip_code(message):
    zip_code = message.text
    cep = busca_cep.BuscaCEP(zip_code)
    BOT.reply_to(message, cep.validate_zip_code()) #validação do CEP digitado
    resp = cep.via_cep_request()
    BOT.send_message(message.chat.id, resp)
    if 'inválido' not in resp:
        new_search(message)
       
def new_search(message):
    text = '            \U0001F449      Buscar novo endereço /Clique_aqui \n\n           \U0000274C     /Sair'
    BOT.send_message(message.chat.id, formatted_output(text))
    

def verify(message): #retorna True para função de resposta padrão sempre ser executada
    return True


@BOT.message_handler(func=verify) #faz a função ser executada independente do que o usuário digitar
def default_reponse(message):
    user_name = message.from_user.first_name
    text = f'''     Olá {user_name}, bem-vindo ao BuscaCEP!  \U0001F1E7\U0001F1F7 \U0001F1E7\U0001F1F7
\n      Selecione a opção desejada:
\n      \U0001F449       Buscar endereço pelo CEP /Clique_aqui. '''
    BOT.reply_to(message, formatted_output(text)) #função para responder

BOT.infinity_polling()#gera um loop infinito (para o bot nunca deixar de conversar com o usario)
