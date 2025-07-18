from core.models import (
    associar_usuario_medicamento,
    registrar_dose,
    listar_medicamentos,
    listar_usuarios,
    listar_historico_uso
)

# 3. Listar usuários e medicamentos cadastrados
listar_usuarios()
listar_medicamentos()

# 4. Associar medicamento a um usuário (João com Dipirona)
associar_usuario_medicamento(
    user_id=1,
    med_id=1,
    quantidade_atual=20,
    unidade="comprimido",
    data_inicio="2025-07-16"
)

# 5. Registrar uso de medicamento (João tomou 1 comprimido de Dipirona)
registrar_dose(
    user_id=1,
    med_id=1,
    dose=1
)

# 6. Listar histórico de uso
listar_historico_uso(1,1)


