from components.cards import mostrar_snack
from services.emprestimo_service import verificar_atrasos_e_multas
from data.storage import salvar_dados
        
async def salvar_e_atualizar(page, dados, route_change, atualizar_dropdown, msg: str = None):

    salvar_dados(dados)

    verificar_atrasos_e_multas(dados)

    if atualizar_dropdown:
        atualizar_dropdown()

    if msg:
        await mostrar_snack(page, msg)

    route_change()