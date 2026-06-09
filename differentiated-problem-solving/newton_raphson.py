def E(x):
    return (-x**6 / 6) + (3 * x**5) - (21.25 * x**4) + (75 * x**3) - (137 * x**2) + (120 * x)


def dE(x):
    return (-x**5) + (15 * x**4) - (85 * x**3) + (225 * x**2) - (274 * x) + 120


def d2E(x):
    return (-5 * x**4) + (60 * x**3) - (255 * x**2) + (450 * x) - 274


def newton_raphson(x0, tolerancia=1e-7, max_iteracoes=1000):
    x = x0

    for i in range(max_iteracoes):
        fx  = dE(x)
        dfx = d2E(x)

        if abs(dfx) < 1e-12:
            return None  # derivada segunda próxima de zero — evita divisão inválida

        x_novo = x - fx / dfx

        if abs(x_novo - x) < tolerancia:
            return round(x_novo, 6)

        x = x_novo

    return None  # não convergiu


def classificar_ponto(x):
    valor = d2E(x)

    if valor < 0:
        return "Máximo local"
    elif valor > 0:
        return "Mínimo local"
    else:
        return "Inconclusivo"


def pontos_unicos(pontos, tolerancia=1e-3):
    unicos = []

    for p in pontos:
        if all(abs(p - u) > tolerancia for u in unicos):
            unicos.append(p)

    return sorted(unicos)


def main():
    print("ORBITAL MEMORY — ANÁLISE DE EFICIÊNCIA DE SINAL")
    print("=" * 52)
    print("Método de Newton-Raphson aplicado sobre E'(x)")
    print("Objetivo: encontrar pontos críticos de E(x)\n")

    # Testa valores iniciais distribuídos no intervalo de interesse [0, 6]
    valores_iniciais = [x * 0.5 for x in range(1, 13)]

    candidatos = []

    for x0 in valores_iniciais:
        resultado = newton_raphson(x0)

        if resultado is not None and 0 < resultado < 6:
            candidatos.append(resultado)

    criticos = pontos_unicos(candidatos)

    print(f"Valores iniciais testados: {valores_iniciais}\n")
    print(f"Pontos críticos encontrados: {len(criticos)}\n")
    print("-" * 52)

    for x in criticos:
        tipo        = classificar_ponto(x)
        eficiencia  = E(x)
        altura_m    = x * 100

        print(f"x = {x:.4f}  →  {altura_m:.1f} metros")
        print(f"  E(x)   = {eficiencia:.4f}")
        print(f"  E'(x)  = {dE(x):.6f}  (próximo de zero: ponto crítico confirmado)")
        print(f"  E''(x) = {d2E(x):.4f}")
        print(f"  Tipo   : {tipo}")
        print()

    print("-" * 52)
    print("\nANÁLISE DE REGIÕES\n")

    # Avalia a eficiência em pontos intermediários para análise de estabilidade
    pontos_analise = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

    print(f"{'x':>6}  {'Altura (m)':>10}  {'E(x)':>10}  {'dE(x)':>12}")
    print("-" * 46)

    for x in pontos_analise:
        print(f"{x:>6.1f}  {x*100:>10.0f}  {E(x):>10.4f}  {dE(x):>12.4f}")

    print("\nRelatório gerado com sucesso.")


if __name__ == "__main__":
    main()