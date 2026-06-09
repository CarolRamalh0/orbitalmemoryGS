# Orbital Memory — Front-End Design

Dashboard estático de monitoramento urbano desenvolvido para a Global Solution 2026 da FIAP.

---

## O problema

Desastres naturais como enchentes, incêndios e deslizamentos causam perda de dados críticos no momento em que eles mais importam. Cidades não têm uma "caixa-preta" — um sistema que preserve e centralize informações durante eventos extremos.

## A solução

O Orbital Memory é uma plataforma de monitoramento urbano em tempo real, conectada a sensores distribuídos pela cidade e apoiada por tecnologia espacial. Este repositório contém a interface visual do dashboard principal.

---

## Estrutura do projeto

```
front-end-design-web-development/
├── index.html   — estrutura semântica da interface
├── style.css    — identidade visual e responsividade
└── README.md    — este arquivo
```

---

## Como executar

Não há dependências ou build necessário. Basta abrir o arquivo diretamente no navegador:

```
Clique duas vezes em index.html
```

---

## Seções da interface

| Seção | Conteúdo |
|---|---|
| Dashboard Principal | Eventos registrados, sensores ativos, áreas monitoradas, status orbital |
| Mapa da Cidade | 6 regiões monitoradas com codificação visual por nível de risco |
| Histórico de Eventos | Registros de enchentes, incêndios e deslizamentos |
| Central de Alertas | Alertas críticos e moderados em tempo real |

---

## HTML semântico

A estrutura segue as boas práticas de HTML5:

- `<header>` com `<nav>` e links de âncora para cada seção
- `<main>` como container de todo o conteúdo principal
- `<section>` com `aria-labelledby` em cada bloco de conteúdo
- `<article>` para cada card de evento e indicador independente
- `<aside>` para a legenda do mapa
- `<footer>` com informações do projeto
- Atributos `role`, `aria-label` e `<time datetime="">` aplicados onde relevante

---

## Identidade visual

**Paleta**

| Token | Valor | Uso |
|---|---|---|
| `--cor-fundo` | `#080c10` | Fundo da página |
| `--cor-superficie` | `#0d1117` | Fundo dos cards |
| `--cor-ok` | `#00c896` | Status normal, operação |
| `--cor-alerta` | `#e8a020` | Situação de atenção |
| `--cor-critico` | `#e03040` | Emergência |
| `--cor-info` | `#3a9ece` | Dados informativos |

**Tipografia**

- `Space Mono` — valores numéricos, labels, dados de sensor
- `Syne 800` — títulos e números de destaque nos cards

A combinação foi escolhida para criar contraste real entre dados brutos e hierarquia visual, sem depender de peso ou tamanho excessivo.

**Layout**

Cards e seções separados por `gap: 1px` com fundo de borda — cria divisórias sem bordas duplas. Sem `border-radius` nos contêineres principais, reforçando a estética de painel de controle industrial.

---

## Responsividade

| Breakpoint | Comportamento |
|---|---|
| `> 768px` | Layout completo em múltiplas colunas |
| `≤ 768px` | Mapa e alertas em coluna única |
| `≤ 480px` | Cards em grid 2×2, histórico em coluna única |

---

## Conexão com as disciplinas

Na proposta completa do Orbital Memory, os dados exibidos nos cards serão integrados à lógica de análise de risco desenvolvida em Python (Computational Thinking) e à simulação de sensores físicos (Edge Computing). A interatividade das simulações será adicionada na etapa de Web Development.

---

## ODS relacionado

**ODS 11 — Cidades e Comunidades Sustentáveis**
Tornar as cidades mais inclusivas, seguras, resilientes e sustentáveis.

---

## Projeto

Global Solution 2026 · FIAP · Turma 1TDSPS
Tema: Indústria Espacial — O Código que Move o Universo