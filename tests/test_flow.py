from pathlib import Path
import json
from flows.main_flow import run_flow
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Custos por 1 milhão de tokens
COST_INPUT_PER_MILLION = 0.100  # USD por 1M tokens de entrada
COST_OUTPUT_PER_MILLION = 0.400  # USD por 1M tokens de saída

# Estimativa de tokens usados por agente (entrada e saída)
TOKEN_USAGE_ESTIMATE = {
    "upload_agent": {"input": 80, "output": 20},
    "parser_agent": {"input": 400, "output": 100},
    "normalizer_agent": {"input": 240, "output": 60},
    "reconciliation_agent": {"input": 320, "output": 80},
    "divergence_agent": {"input": 320, "output": 80},
    "recommendation_agent": {"input": 320, "output": 80},
    "coordinator_agent": {"input": 160, "output": 40},
}

def salvar_pdf_conciliacao(resultado, caminho_saida):
    c = canvas.Canvas(caminho_saida, pagesize=A4)
    largura, altura = A4
    y = altura - 50

    def escrever_linha(texto, tamanho=10, espaco=14):
        nonlocal y
        if y < 60:
            c.showPage()
            y = altura - 50
        c.setFont("Helvetica", tamanho)
        c.drawString(50, y, texto)
        y -= espaco

    escrever_linha("Relatório de Conciliação Financeira da IA", tamanho=14, espaco=20)
    escrever_linha("-" * 90)

    escrever_linha("\n🔹 Transações conciliadas:")
    if resultado.get("conciliated"):
        for item in resultado["conciliated"]:
            escrever_linha(json.dumps(item, ensure_ascii=False), tamanho=9)
    else:
        escrever_linha("Nenhuma transação conciliada encontrada.")

    escrever_linha("\n🔸 Divergências encontradas:")
    if resultado.get("divergent"):
        for item in resultado["divergent"]:
            escrever_linha(json.dumps(item, ensure_ascii=False), tamanho=9)
    else:
        escrever_linha("Nenhuma divergência detectada.")

    escrever_linha("\n💡 Sugestões:")
    for sugestao in resultado.get("sugestoes", []):
        escrever_linha(f"- {sugestao}", tamanho=9)

    c.save()

def calcular_custo_por_agente(token_usage, cost_input=COST_INPUT_PER_MILLION, cost_output=COST_OUTPUT_PER_MILLION):
    custo_total = 0
    print("\n💰 Estimativa de custo por agente:")
    for agente, usage in token_usage.items():
        input_tokens = usage.get("input", 0)
        output_tokens = usage.get("output", 0)
        custo_entrada = (input_tokens / 1_000_000) * cost_input
        custo_saida = (output_tokens / 1_000_000) * cost_output
        custo = custo_entrada + custo_saida
        custo_total += custo
        print(f" - {agente}: {input_tokens + output_tokens} tokens (entrada: {input_tokens}, saída: {output_tokens}) => ~US$ {custo:.5f}")
    print(f"🔹 Custo total estimado: US$ {custo_total:.5f}\n")
    return custo_total

def test_main_flow():
    test_file = Path("data/EXTRATO LOJA - JANEIRO.pdf")
    resultado = run_flow(file_path=str(test_file))

    print("\n=== RESULTADO DO FLUXO DE CONCILIAÇÃO ===\n")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    assert "error" not in resultado, f"Erro na execução: {resultado.get('error')}"
    assert isinstance(resultado, dict), "A saída deve ser um dicionário"
    assert "conciliated" in resultado, "'conciliated' não encontrado na saída"
    assert "divergent" in resultado, "'divergent' não encontrado na saída"
    assert "sugestoes" in resultado, "'sugestoes' não encontrado na saída"
    assert isinstance(resultado["conciliated"], list), "'conciliated' deve ser uma lista"
    assert isinstance(resultado["divergent"], list), "'divergent' deve ser uma lista"
    assert isinstance(resultado["sugestoes"], list), "'sugestoes' deve ser uma lista"

    salvar_pdf_conciliacao(resultado, "analise_conciliacao_final2.pdf")
    print("\n📄 PDF gerado: analise_conciliacao_final.pdf")

    calcular_custo_por_agente(TOKEN_USAGE_ESTIMATE)

if __name__ == "__main__":
    test_main_flow()
