def calcular_valor_multa(
    dias_atraso: int,
    valor_por_dia: float
) -> float:

    return round(
        dias_atraso * valor_por_dia,
        2
    )