<<<<<<< HEAD
from enviar_sms import enviar_sms

# Exemplo de envio de SMS
enviar_sms("+5548991986242", "Lembrete de medicamento: tomar Dipirona agora.")

=======
from core.models import (
    cadastrar_agendamento
)

# Exemplo: João toma Dipirona às 08:00 e 20:00 nas seg, qua e sex

user_med_id = 1  # Relacionamento já criado
cadastrar_agendamento(user_med_id, "08:00", "1,3,5", 1.0)
cadastrar_agendamento(user_med_id, "20:00", "1,3,5", 1.0)

>>>>>>> e1696d58aa25e4cb68b54d52f35ae0a672538dff


