# ThumbsUply

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/) [![Polars](https://img.shields.io/badge/Data_Processing-Polars-orange.svg)](https://pola.rs/) [![Supabase](https://img.shields.io/badge/Backend-Supabase-green.svg)](https://supabase.com/) [![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red.svg)](https://streamlit.io/) [![uv](https://img.shields.io/badge/Environment-uv-purple.svg)](https://github.com/astral-sh/uv)

## Overview
**ThumbsUply** é um projeto de *Data Engineering* e *Analytics* end-to-end desenhado para simular o ecossistema de dados de uma plataforma SaaS B2B. O objetivo principal é atuar como um **Analytics Engineer**, preenchendo a lacuna entre eventos brutos de backend e decisões de estratégia financeira de alto nível.

O sistema simula o ciclo de vida diário de assinaturas (*signups, upgrades, downgrades e churn*), processando-os através de uma pipeline de alta performance para gerar um dashboard de **FP&A** em tempo real. Isso permite monitorar a "saúde" do negócio através de *unit economics* e velocidade de receita.

---

## Tech Stack & Architecture
Este projeto replica um ambiente moderno de **Modern Data Stack (MDS)**:

* **Data Processing:** [Polars](https://pola.rs/)
Utilizado por seu motor de execução multi-threaded em Rust e *lazy evaluation*, proporcionando ganhos de performance de até 30x em comparação a bibliotecas tradicionais.
* **Cloud Backend:** [Supabase](https://supabase.com/)
Backend-as-a-service baseado em PostgreSQL para armazenamento de tabelas dimensões (`customers`, `subscription_plans`) e a tabela fato (`events`).
* **Automation:** [GitHub Actions](https://github.com/features/actions)
Orquestração de scripts Python para simulação de eventos diários, garantindo um dataset dinâmico.
* **BI & Visualization:** [Streamlit](https://streamlit.io/)
Camada de dashboard interativo para planejamento de cenários e acompanhamento de métricas.
* **Environment Management:** [uv](https://github.com/astral-sh/uv)
Instalador e resolvedor de pacotes extremamente rápido para garantir builds reprodutíveis via `uv.lock`.

---

## Data Model
A lógica de negócio segue o framework **SaaS Revenue Waterfall**. Transformamos eventos brutos em cinco baldes críticos de receita:

1.  **Beginning MRR:** Estado inicial da receita no período.
2.  **New MRR:** Receita vinda da aquisição de novos clientes.
3.  **Expansion MRR:** Receita de clientes atuais que fizeram upgrade de plano (Upsells).
4.  **Contraction MRR:** Receita perdida por downgrades de plano.
5.  **Churn MRR:** Receita perdida por cancelamentos.

---

## Key FP&A Metrics Tracked
O dashboard prioriza eficiência de capital e sustentabilidade:

* **Net Revenue Retention (NRR):** Mede a capacidade de crescer a receita a partir da base atual. Benchmarks de mercado buscam $> 100\%$.
* **LTV:CAC Ratio:** Compara o *Lifetime Value* com o custo de aquisição. O benchmark ideal é $3:1$.
* **Burn Multiple:** Mede quanto caixa é "queimado" para gerar cada dólar de nova ARR.
* **Months to Recover CAC:** Tempo necessário para um cliente se tornar lucrativo (*Payback Period*).
* **Natural Rate of Growth (NRG):** Quantifica o crescimento orgânico impulsionado pelo produto, independente de marketing.

---

## Future Roadmap
[ ] Involuntary Churn Analysis: Lógica para rastrear falhas de pagamento (cartões expirados).

[ ] Scenario Manager: Sliders "What-If" no Streamlit para prever impacto de mudanças de preço no Runway.

[ ] Cohort Analysis: Visualização de padrões de retenção usando group_by e agg do Polars.

---