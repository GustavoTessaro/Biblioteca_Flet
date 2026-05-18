from datetime import date

from services.multa_service import calcular_valor_multa
from core.constants import STATUS_ABERTO, STATUS_ATRASADO, STATUS_ENTREGUE
from core.helpers import obter_por_id, parse_data, proximo_id
from data.storage import salvar_dados


def obter_status_emprestimo(emprestimo: dict, hoje: date) -> str:
    if emprestimo["status"] == STATUS_ENTREGUE:
        return STATUS_ENTREGUE
    data_entrega = parse_data(emprestimo["data_entrega"])
    if hoje > data_entrega:
        return STATUS_ATRASADO
    return STATUS_ABERTO

def verificar_atrasos_e_multas(dados: dict):
    hoje = date.today()
    for emprestimo in dados["emprestimos"]:
        if emprestimo["status"] != STATUS_ENTREGUE:
            novo_status = obter_status_emprestimo(emprestimo, hoje)
            emprestimo["status"] = novo_status

            if novo_status == "Atrasado":
                livro = obter_por_id(dados["livros"], emprestimo["livro_id"])
                prateleira = obter_por_id(dados["prateleiras"], livro["prateleira_id"]) if livro else None
                if livro and prateleira:
                    dias_atraso = (hoje - parse_data(emprestimo["data_entrega"])).days
                    valor = calcular_valor_multa(dias_atraso, prateleira.get("multa_por_dia", 1.0))

                    multa_existente = next(
                        (m for m in dados["multas"] if m["emprestimo_id"] == emprestimo["id"]),
                        None,
                    )
                    if multa_existente:
                        if multa_existente["status"] == "Pendente":
                            multa_existente["dias_atraso"] = dias_atraso
                            multa_existente["valor"] = valor
                    else:
                        dados["multas"].append({
                            "id": proximo_id(dados["multas"]),
                            "emprestimo_id": emprestimo["id"],
                            "cliente_id": emprestimo["cliente_id"],
                            "livro_id": emprestimo["livro_id"],
                            "dias_atraso": dias_atraso,
                            "valor": valor,
                            "status": "Pendente",
                        })

    salvar_dados(dados)
