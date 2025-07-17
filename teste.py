from core.models import associar_usuario_medicamento

associar_usuario_medicamento(
    user_id=1,
    med_id=1,
    quantidade_atual=10.0,
    unidade="comprimidos",
    data_inicio="2025-07-16"  # data de início no formato ISO
)
