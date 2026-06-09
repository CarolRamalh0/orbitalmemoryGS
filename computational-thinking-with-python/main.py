import csv
from datetime import datetime


ARQUIVO_DADOS = "dados_sensores.csv"
ARQUIVO_RELATORIO = "relatorio_alertas.txt"


def classificar_risco(nivel_rio, temperatura, umidade, integridade_estacao, comunicacao):

    pontos = 0
    evento_provavel = "Operação normal"
    acao_recomendada = "Manter monitoramento contínuo."

    if nivel_rio >= 85 and umidade >= 80:
        pontos += 4
        evento_provavel = "Enchente"
        acao_recomendada = "Acionar Defesa Civil, priorizar evacuação preventiva e preservar dados no histórico orbital."
    elif nivel_rio >= 70:
        pontos += 2
        evento_provavel = "Possível enchente"
        acao_recomendada = "Monitorar elevação do rio e preparar equipes de resposta."

    if temperatura >= 380:
        pontos += 4
        evento_provavel = "Incêndio"
        acao_recomendada = "Acionar brigada de emergência, isolar área afetada e registrar ocorrência crítica."
    elif temperatura >= 330:
        pontos += 2
        evento_provavel = "Possível foco de incêndio"
        acao_recomendada = "Verificar sensores térmicos e acompanhar evolução da temperatura."

    if umidade >= 90 and integridade_estacao <= 75:
        pontos += 3
        evento_provavel = "Deslizamento"
        acao_recomendada = "Monitorar encostas, alertar moradores próximos e preservar leituras dos sensores."

    if integridade_estacao <= 50:
        pontos += 3
        evento_provavel = "Falha estrutural ou falha da estação"
        acao_recomendada = "Enviar equipe técnica e ativar redundância de dados."

    if comunicacao.lower() == "offline":
        pontos += 3
        evento_provavel = "Falha de comunicação"
        acao_recomendada = "Ativar canal alternativo e sincronização orbital."
    elif comunicacao.lower() == "instavel":
        pontos += 1
        evento_provavel = "Comunicação instável"
        acao_recomendada = "Monitorar instabilidade e preparar redundância."

    if pontos >= 6:
        risco = "CRÍTICO"
    elif pontos >= 4:
        risco = "ALTO"
    elif pontos >= 2:
        risco = "MÉDIO"
    else:
        risco = "BAIXO"

    return risco, evento_provavel, acao_recomendada, pontos


def ler_dados_csv(caminho_arquivo):

    regioes = []

    try:
        with open(caminho_arquivo, mode="r", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)

            for linha in leitor:
                regiao = {
                    "regiao": linha["regiao"],
                    "nivel_rio": float(linha["nivel_rio"]),
                    "temperatura": float(linha["temperatura"]),
                    "umidade": float(linha["umidade"]),
                    "integridade_estacao": float(linha["integridade_estacao"]),
                    "comunicacao": linha["comunicacao"]
                }

                regioes.append(regiao)

    except FileNotFoundError:
        print(f"Erro: o arquivo {caminho_arquivo} não foi encontrado.")
    except KeyError:
        print("Erro: o arquivo CSV está com colunas incorretas.")
    except ValueError:
        print("Erro: existem valores inválidos no arquivo CSV.")

    return regioes


def gerar_relatorio(resultados):

    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    with open(ARQUIVO_RELATORIO, mode="w", encoding="utf-8") as relatorio:
        relatorio.write("RELATÓRIO DE ALERTAS — ORBITAL MEMORY\n")
        relatorio.write("=" * 50 + "\n")
        relatorio.write(f"Data e hora da análise: {data_hora}\n\n")

        for item in resultados:
            relatorio.write(f"Região: {item['regiao']}\n")
            relatorio.write(f"Risco: {item['risco']}\n")
            relatorio.write(f"Evento provável: {item['evento']}\n")
            relatorio.write(f"Pontuação de risco: {item['pontos']}\n")
            relatorio.write(f"Ação recomendada: {item['acao']}\n")
            relatorio.write("-" * 50 + "\n")


def exibir_resultados(resultados):

    print("\nORBITAL MEMORY — ANÁLISE DE RISCO URBANO")
    print("=" * 50)

    for item in resultados:
        print(f"\nRegião: {item['regiao']}")
        print(f"Risco: {item['risco']}")
        print(f"Evento provável: {item['evento']}")
        print(f"Pontuação de risco: {item['pontos']}")
        print(f"Ação recomendada: {item['acao']}")

    print("\nRelatório gerado com sucesso em: relatorio_alertas.txt")


def main():
    regioes = ler_dados_csv(ARQUIVO_DADOS)

    if not regioes:
        print("Nenhum dado foi processado.")
        return

    resultados = []

    for regiao in regioes:
        risco, evento, acao, pontos = classificar_risco(
            regiao["nivel_rio"],
            regiao["temperatura"],
            regiao["umidade"],
            regiao["integridade_estacao"],
            regiao["comunicacao"]
        )

        resultado = {
            "regiao": regiao["regiao"],
            "risco": risco,
            "evento": evento,
            "acao": acao,
            "pontos": pontos
        }

        resultados.append(resultado)

    exibir_resultados(resultados)
    gerar_relatorio(resultados)


if __name__ == "__main__":
    main()