import os
from twilio.rest import Client
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Suas credenciais do Twilio a partir das variáveis de ambiente
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")


def enviar_sms(destinatario, mensagem):
    """
    Envia um SMS usando o Twilio.
    :param destinatario: Número de telefone do destinatário (formato +5511999999999)
    :param mensagem: Mensagem a ser enviada
    """
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER]):
        print("❌ As credenciais do Twilio não estão configuradas nas variáveis de ambiente.")
        return

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=mensagem,
            from_=TWILIO_PHONE_NUMBER,
            to=destinatario
        )

        print(f"✅ SMS enviado com sucesso para {destinatario}. SID: {message.sid}")
        return message.sid
    except Exception as e:
        print(f"❌ Erro ao enviar SMS: {e}")
        return None
