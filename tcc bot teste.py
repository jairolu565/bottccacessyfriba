import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
import asyncio
import nest_asyncio
import google.generativeai as genai
import paramiko
import time

def ssh_invoke_shell_online(hostname, username, password, pon):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=hostname, username=username, password=password, timeout=60)
        print(f"Conectado ao {hostname}")
        shell = client.invoke_shell()
        time.sleep(1)

        output = shell.recv(1000).decode('utf-8')
        print(output)

        shell.send(f'show gpon onu state gpon-olt_1/2/{pon} working\n')
        time.sleep(2)

        output = shell.recv(1000000).decode('utf-8')
        return output

    except paramiko.SSHException as e:
        print(f"Erro de SSH: {e}")
    finally:
        client.close()


def ssh_invoke_shell_offline(hostname, username, password, pon):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=hostname, username=username, password=password, timeout=60)
        print(f"Conectado ao {hostname}")
        shell = client.invoke_shell()
        time.sleep(1)

        output = shell.recv(1000).decode('utf-8')
        print(output)

        shell.send(f'show gpon onu state gpon-olt_1/2/{pon} Offline\n')
        time.sleep(2)

        output = shell.recv(1000000).decode('utf-8')
        return output

    except paramiko.SSHException as e:
        print(f"Erro de SSH: {e}")
    finally:
        client.close()

nest_asyncio.apply()

API_TOKEN = '5940928964:AAGe9JsxuwCYgfqOcvZzVgvrUWq3zjfmFKM'
CHAT_ID = '1272169092'

olt_ip = '10.90.10.10'
olt_user = 'luigi'
olt_pass = '0Eq36!Q0Eq36Eq36'

genai.configure(api_key="AIzaSyAsAtbBi9mfv1y8AHKYsqKEQIpOqrAUkSM")
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="Você é um bot que serve para puxar as informações de uma OLT de um provedor de internet a partir da solicitação de um usuário. Você deve analisar a solicitação, e caso seja uma mensagem de saudação, você deve responder normalmente, perguntando 'O que posso fazer por você hoje?', mas não necessariamente apenas essa frase. Interaja com o usuário normalmente, não enviando apenas essa mensagem automática, mas pergunte o que ele deseja, após sua resposta. Caso a solicitação do usuário seja direta, você deve avaliar a pergunta e responder APENAS a palavra mais adequada das seguintes: 'onu_clientes_offline_sem_trafego', 'onu_clientes_online_trafegando' ou 'status_da_olt', de acordo com o que for mais adequado ao contexto da pergunta, apenas essas três opções e nada mais, pois, a partir dessas opções, será processado um comando. Caso a solicitação do usuário seja uma mensagem de despedida, você deve responder 'Até mais!'. Caso o prompt do usuário não seja um dos três conandos pré definidos, você deve responder 'Desculpe, não entendi o comando. Você pode digitar '!help' para exibir os comandos disponíveis.'."
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Bot inicializado no grupo!")

async def send_options(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Ver ONUs offline", callback_data='onu_offline')],
        [InlineKeyboardButton("Ver ONUs online", callback_data='onu_online')],
        [InlineKeyboardButton("Ver status da OLT", callback_data='status_olt')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Escolha uma opção:', reply_markup=reply_markup)

async def send_options_pon(update: Update, context):
    Keyboard = [
        [InlineKeyboardButton("PON 1/2/1", callback_data='pon1')],
        [InlineKeyboardButton("PON 1/2/2", callback_data='pon2')],
        [InlineKeyboardButton("PON 1/2/3", callback_data='pon3')],
        [InlineKeyboardButton("PON 1/2/4", callback_data='pon4')],
        [InlineKeyboardButton("PON 1/2/5", callback_data='pon5')],
        [InlineKeyboardButton("PON 1/2/6", callback_data='pon6')],
        [InlineKeyboardButton("PON 1/2/7", callback_data='pon7')],
        [InlineKeyboardButton("PON 1/2/8", callback_data='pon8')],
        [InlineKeyboardButton("PON 1/2/9", callback_data='pon9')],
        [InlineKeyboardButton("PON 1/2/10", callback_data='pon10')]
    ]
    reply_markup = InlineKeyboardMarkup(Keyboard)
    
    # Verifica se a interação foi por mensagem ou por botão
    if update.message:
        await update.message.reply_text('Escolha uma PON:', reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text('Escolha uma PON:', reply_markup=reply_markup)

async def send_options_online(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("PON 1/2/1", callback_data='pon11')],
        [InlineKeyboardButton("PON 1/2/2", callback_data='pon22')],
        [InlineKeyboardButton("PON 1/2/3", callback_data='pon33')],
        [InlineKeyboardButton("PON 1/2/4", callback_data='pon44')],
        [InlineKeyboardButton("PON 1/2/5", callback_data='pon55')],
        [InlineKeyboardButton("PON 1/2/6", callback_data='pon66')],
        [InlineKeyboardButton("PON 1/2/7", callback_data='pon77')],
        [InlineKeyboardButton("PON 1/2/8", callback_data='pon88')],
        [InlineKeyboardButton("PON 1/2/9", callback_data='pon99')],
        [InlineKeyboardButton("PON 1/2/10", callback_data='pon100')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text('Escolha uma PON:', reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text('Escolha uma PON:', reply_markup=reply_markup)

async def button(update: Update, context):
    query = update.callback_query
    await query.answer()  # Confirma a interação

    # Pega o dado do callback (que foi definido em callback_data)
    escolha = query.data

    # Verifica a escolha do botão e responde adequadamente
    if escolha == 'onu_offline':
        await query.edit_message_text(text="De qual PON você deseja ver as ONUs offline?")
        await send_options_pon(update, context)
    elif escolha == 'onu_online':
        await query.edit_message_text(text="De qual PON você deseja ver as ONUs online?")
        await send_options_online(update, context)
    elif escolha == 'status_olt':
        await query.edit_message_text(text="Processando o comando de status da OLT...")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Status da OLT: OK.")
    
    elif escolha == 'pon11':
        await query.edit_message_text(text="Processando o comando para PON 1...")
        resp = ssh_invoke_shell_online(olt_ip, olt_user, olt_pass, 1)
        #retorna apenas as linhas que contém a palavra "Working"
        resp = "\n".join([line for line in resp.split("\n") if "working" in line])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
        #conta quantas vezes a palavra "Working" aparece na resposta
        count = resp.count("working")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Existem {count} ONU online na PON 1 no momento.")

    elif escolha == 'pon22':
        await query.edit_message_text(text="Processando o comando para PON 2...")
        resp = ssh_invoke_shell_online(olt_ip, olt_user, olt_pass, 2)
        #retorna apenas as linhas que contém a palavra "Working"
        resp = "\n".join([line for line in resp.split("\n") if "working" in line])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
        #conta quantas vezes a palavra "Working" aparece na resposta
        count = resp.count("working")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Existem {count} ONU online na PON 2 no momento.")

    elif escolha == 'pon33':
        await query.edit_message_text(text="Processando o comando para PON 3...")
        resp = ssh_invoke_shell_online(olt_ip, olt_user, olt_pass, 3)
        #retorna apenas as linhas que contém a palavra "Working"
        resp = "\n".join([line for line in resp.split("\n") if "working" in line])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
        #conta quantas vezes a palavra "Working" aparece na resposta
        count = resp.count("working")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Existem {count} ONU online na PON 3 no momento.")

    elif escolha == 'pon44':
        await query.edit_message_text(text="Processando o comando para PON 4...")
        resp = ssh_invoke_shell_online(olt_ip, olt_user, olt_pass, 4)
        #retorna apenas as linhas que contém a palavra "Working"
        resp = "\n".join([line for line in resp.split("\n") if "working" in line])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
        #conta quantas vezes a palavra "Working" aparece na resposta
        count = resp.count("working")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Existem {count} ONU online na PON 4 no momento.")

    elif escolha == 'pon55':
        await query.edit_message_text(text="Processando o comando para PON 5...")
        resp = ssh_invoke_shell_online(olt_ip, olt_user, olt_pass, 5)
        #retorna apenas as linhas que contém a palavra "Working"
        resp = "\n".join([line for line in resp.split("\n") if "working" in line])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
        #conta quantas vezes a palavra "Working" aparece na resposta
        count = resp.count("working")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Existem {count} ONU online na PON 5 no momento.")

    elif escolha == 'pon66':
        await query.edit_message_text(text="Processando o comando para PON 6...")
        resp = ssh_invoke_shell_online(olt_ip, olt_user, olt_pass, 6)
        #retorna apenas as linhas que contém a palavra "Working"
        resp = "\n".join([line for line in resp.split("\n") if "working" in line])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
        #conta quantas vezes a palavra "Working" aparece na resposta
        count = resp.count("working")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Existem {count} ONU online na PON 6 no momento.")

    elif escolha == 'pon77':
        await query.edit_message_text(text="Processando o comando para PON 7...")
        resp = ssh_invoke_shell_online(olt_ip, olt_user, olt_pass, 7)
        #retorna apenas as linhas que contém a palavra "Working"
        resp = "\n".join([line for line in resp.split("\n") if "working" in line])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
        #conta quantas vezes a palavra "Working" aparece na resposta
        count = resp.count("working")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Existem {count} ONU online na PON 7 no momento.")

    elif escolha == 'pon88':
        await query.edit_message_text(text="Processando o comando para PON 8...")
        resp = ssh_invoke_shell_online(olt_ip, olt_user, olt_pass, 8)
        #retorna apenas as linhas que contém a palavra "Working"
        resp = "\n".join([line for line in resp.split("\n") if "working" in line])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
        #conta quantas vezes a palavra "Working" aparece na resposta
        count = resp.count("working")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Existem {count} ONU online na PON 8 no momento.")

    elif escolha == 'pon99':
        await query.edit_message_text(text="Processando o comando para PON 9...")
        resp = ssh_invoke_shell_online(olt_ip, olt_user, olt_pass, 9)
        #retorna apenas as linhas que contém a palavra "Working"
        resp = "\n".join([line for line in resp.split("\n") if "working" in line])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
        #conta quantas vezes a palavra "Working" aparece na resposta
        count = resp.count("working")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Existem {count} ONU online na PON 9 no momento.")

    elif escolha == 'pon100':
        await query.edit_message_text(text="Processando o comando para PON 10...")
        resp = ssh_invoke_shell_online(olt_ip, olt_user, olt_pass, 10)
        #retorna apenas as linhas que contém a palavra "Working"
        resp = "\n".join([line for line in resp.split("\n") if "working" in line])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
        #conta quantas vezes a palavra "Working" aparece na resposta
        count = resp.count("working")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Existem {count} ONU online na PON 10 no momento.")



    # Novos handlers para as opções de PON
    elif escolha == 'pon1':
        await query.edit_message_text(text="Processando o comando para PON 1...")
        resp = ssh_invoke_shell_offline(olt_ip, olt_user, olt_pass, 1)
        #retorna apenas as linhas que contém a palavra "OffLine"
        resp = "\n".join([line for line in resp.split("\n") if "OffLine" in line])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
        #conta quantas vezes a palavra "Offline" aparece na resposta
        count = resp.count("OffLine")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Existem {count} ONU offline na PON 1 no momento.")
        
    elif escolha == 'pon2':
        await query.edit_message_text(text="Processando o comando para PON 2...")
        resp = ssh_invoke_shell_offline(olt_ip, olt_user, olt_pass, 2)
        #retorna apenas as linhas que contém a palavra "OffLine"
        resp = "\n".join([line for line in resp.split("\n") if "OffLine" in line])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
        #conta quantas vezes a palavra "Offline" aparece na resposta
        count = resp.count("OffLine")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Existem {count} ONU offline na PON 2 no momento.")
    elif escolha == 'pon3':
        await query.edit_message_text(text="Processando o comando para PON 3...")
        resp = ssh_invoke_shell_offline(olt_ip, olt_user, olt_pass, 3)
        #retorna apenas as linhas que contém a palavra "OffLine"
        resp = "\n".join([line for line in resp.split("\n") if "OffLine" in line])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
        #conta quantas vezes a palavra "Offline" aparece na resposta
        count = resp.count("OffLine")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Existem {count} ONU offline na PON 3 no momento.")
    elif escolha == 'pon4':
        await query.edit_message_text(text="Processando o comando para PON 4...")
        resp = ssh_invoke_shell_offline(olt_ip, olt_user, olt_pass, 4)
        #retorna apenas as linhas que contém a palavra "OffLine"
        resp = "\n".join([line for line in resp.split("\n") if "OffLine" in line])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
        #conta quantas vezes a palavra "Offline" aparece na resposta
        count = resp.count("OffLine")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Existem {count} ONU offline na PON 4 no momento.")
    elif escolha == 'pon5':
        await query.edit_message_text(text="Processando o comando para PON 5...")
        resp = ssh_invoke_shell_offline(olt_ip, olt_user, olt_pass, 5)
        #retorna apenas as linhas que contém a palavra "OffLine"
        resp = "\n".join([line for line in resp.split("\n") if "OffLine" in line])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
        #conta quantas vezes a palavra "Offline" aparece na resposta
        count = resp.count("OffLine")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Existem {count} ONU offline na PON 5 no momento.")
    elif escolha == 'pon6':
        await query.edit_message_text(text="Processando o comando para PON 6...")
        resp = ssh_invoke_shell_offline(olt_ip, olt_user, olt_pass, 6)
        #retorna apenas as linhas que contém a palavra "OffLine"
        resp = "\n".join([line for line in resp.split("\n") if "OffLine" in line])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
        #conta quantas vezes a palavra "Offline" aparece na resposta
        count = resp.count("OffLine")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Existem {count} ONU offline na PON 6 no momento.")
    elif escolha == 'pon7':
        await query.edit_message_text(text="Processando o comando para PON 7...")
        resp = ssh_invoke_shell_offline(olt_ip, olt_user, olt_pass, 7)
        #retorna apenas as linhas que contém a palavra "OffLine"
        resp = "\n".join([line for line in resp.split("\n") if "OffLine" in line])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
        #conta quantas vezes a palavra "Offline" aparece na resposta
        count = resp.count("OffLine")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Existem {count} ONU offline na PON 7 no momento.")
    elif escolha == 'pon8':
        await query.edit_message_text(text="Processando o comando para PON 8...")
        resp = ssh_invoke_shell_offline(olt_ip, olt_user, olt_pass, 8)
        #retorna apenas as linhas que contém a palavra "OffLine"
        resp = "\n".join([line for line in resp.split("\n") if "OffLine" in line])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
        #conta quantas vezes a palavra "Offline" aparece na resposta
        count = resp.count("OffLine")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Existem {count} ONU offline na PON 8 no momento.")
    elif escolha == 'pon9':
        await query.edit_message_text(text="Processando o comando para PON 9...")
        resp = ssh_invoke_shell_offline(olt_ip, olt_user, olt_pass, 9)
        #retorna apenas as linhas que contém a palavra "OffLine"
        resp = "\n".join([line for line in resp.split("\n") if "OffLine" in line])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
        #conta quantas vezes a palavra "Offline" aparece na resposta
        count = resp.count("OffLine")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Existem {count} ONU offline na PON 9 no momento.")
    elif escolha == 'pon10':
        await query.edit_message_text(text="Processando o comando para PON 10...")
        resp = ssh_invoke_shell_offline(olt_ip, olt_user, olt_pass, 10)
        #retorna apenas as linhas que contém a palavra "OffLine"
        resp = "\n".join([line for line in resp.split("\n") if "OffLine" in line])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
        #conta quantas vezes a palavra "Offline" aparece na resposta
        count = resp.count("OffLine")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Existem {count} ONU offline na PON 10 no momento.")
     
async def handle_message(update: Update, context):
    user_message = update.message.text
    logger.info(f"Recebendo mensagem: {user_message}")

    if user_message == "!help":
        await send_options(update, context)
    else:
        label = model.generate_content(user_message)
        response = label.text.strip().lower()

        logger.info(f"Resultado da classificação: {response}")

        if response == 'onu_clientes_offline_sem_trafego':
            await context.bot.send_message(chat_id=update.effective_chat.id, text="De qual PON você deseja ver as ONUs offline?")
            await send_options_pon(update, context)
        elif response == 'onu_clientes_online_trafegando':
            await send_options_online(update, context)
        elif response == 'status_da_olt':
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Status da OLT: OK.")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

async def main():
    application = Application.builder().token(API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button))

    await application.run_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    if not loop.is_running():
        loop.run_until_complete(main())
    else:
        print("O event loop já está em execução.")