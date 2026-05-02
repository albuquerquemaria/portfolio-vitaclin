import streamlit as st
import pandas as pd

st.title("📊 Análise Financeira — VitaClin")
st.markdown("**Jan/2024 – Dez/2025** | Preparado por Maria Eduarda Albuquerque")

st.markdown("""
Este documento consolida os principais indicadores financeiros da VitaClin no período de
janeiro de 2024 a dezembro de 2025, com base em 5.067 atendimentos registrados em nove unidades.
O objetivo é oferecer uma leitura clara do desempenho de receita, composição de faturamento
e oportunidades de crescimento.
""")

# ─────────────────────────────────────────
# MÉTRICAS PRINCIPAIS
# ─────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Faturamento Total", "R$ 157.936")
col2.metric("Ticket Médio Geral", "R$ 31,17")
col3.metric("Atendimentos", "5.067")
col4.metric("Unidades Ativas", "9")

# ─────────────────────────────────────────
# DESEMPENHO POR UNIDADE
# ─────────────────────────────────────────
st.header("Desempenho por Unidade")
st.markdown("O faturamento está concentrado nas duas maiores unidades, que juntas respondem por **65% da receita total**. A Filial I se destaca com o maior ticket médio entre as unidades de alto volume.")

unidades = pd.DataFrame({
    'Unidade': ['Centro Médico Matriz', 'Filial I', 'Miguel Souza', 'Filial II – 10',
                'Campo Verde', 'Nilópolis', 'São João', 'Filial II – 11', 'Méier'],
    'Faturamento': ['R$ 54.584', 'R$ 48.624', 'R$ 13.534', 'R$ 11.186',
                    'R$ 10.267', 'R$ 9.364', 'R$ 6.410', 'R$ 3.450', 'R$ 517'],
    'Atendimentos': [2042, 1204, 524, 214, 427, 353, 198, 82, 23],
    'Ticket Médio': ['R$ 26,73', 'R$ 40,39', 'R$ 25,83', 'R$ 52,27',
                     'R$ 24,04', 'R$ 26,53', 'R$ 32,37', 'R$ 42,07', 'R$ 22,50'],
    '% Receita': ['34,6%', '30,8%', '8,6%', '7,1%', '6,5%', '5,9%', '4,1%', '2,2%', '0,3%']
})
st.dataframe(unidades, use_container_width=True)
st.warning("💡 **Oportunidade:** A Filial II–10 tem o maior ticket médio (R$ 52,27) mas opera com apenas 214 atendimentos — menos de 11% do volume da Matriz. Expandir sua capacidade pode ser a alavanca de receita mais eficiente no curto prazo.")

# ─────────────────────────────────────────
# COMPOSIÇÃO POR GRUPO DE PROCEDIMENTO
# ─────────────────────────────────────────
st.header("Composição da Receita por Grupo de Procedimento")
st.markdown("Os dez grupos abaixo representam **88% do faturamento total**. O dado mais relevante está na contradição entre volume e valor: Exames Laboratoriais lideram em quantidade, mas Ultrassonografia gera receita proporcional muito maior com bem menos atendimentos.")

procedimentos = pd.DataFrame({
    'Grupo de Procedimento': ['Exames Laboratoriais', 'Ultrassonografia', 'Clínica Geral',
                               'Ginecologia', 'Raio X', 'Enfermaria', 'Demais',
                               'Tomografia', 'Ortopedia', 'Psiquiatria'],
    'Faturamento': ['R$ 54.708', 'R$ 25.130', 'R$ 14.138', 'R$ 7.335', 'R$ 7.114',
                    'R$ 5.450', 'R$ 5.479', 'R$ 3.596', 'R$ 3.569', 'R$ 2.967'],
    'Atendimentos': [2870, 243, 726, 229, 113, 137, 50, 14, 111, 43],
    'Ticket Médio': ['R$ 19,06', 'R$ 103,42', 'R$ 19,47', 'R$ 32,03', 'R$ 62,96',
                     'R$ 39,78', 'R$ 109,58', 'R$ 256,86', 'R$ 32,15', 'R$ 69,00'],
    '% Receita': ['34,6%', '15,9%', '9,0%', '4,6%', '4,5%', '3,5%', '3,5%', '2,3%', '2,3%', '1,9%']
})
st.dataframe(procedimentos, use_container_width=True)

st.info("🔬 **Exames Laboratoriais** dominam em volume (57% dos atendimentos), mas com ticket médio baixo de R$ 19 — motor de captação, não de margem.")
st.info("📡 **Ultrassonografia** concentra 15,9% da receita com apenas 4,8% dos atendimentos (ticket R$ 103). Ampliar essa oferta nas filiais elevaria o faturamento por slot.")
st.info("🧠 **Tomografia** tem o maior ticket médio (R$ 256,86) com apenas 14 atendimentos — potencial claramente subutilizado.")
st.info("🧬 **Psiquiatria** apresenta ticket médio de R$ 69 com demanda consistente — grupo com potencial de crescimento via agenda dedicada.")

# ─────────────────────────────────────────
# MEIOS DE PAGAMENTO
# ─────────────────────────────────────────
st.header("Meios de Pagamento e Implicações de Receita")
st.markdown("**Dinheiro** responde por 87,4% da receita total — um percentual elevado que representa baixa previsibilidade de fluxo de caixa e menor capacidade de parcelamento em procedimentos de alto valor.")

pagamentos = pd.DataFrame({
    'Forma de Pagamento': ['Dinheiro', 'Cartão de Crédito', 'Cartão de Débito', 'PIX'],
    'Faturamento': ['R$ 138.001', 'R$ 12.389', 'R$ 3.796', 'R$ 3.751'],
    'Atendimentos': [4185, 652, 125, 105],
    'Ticket Médio': ['R$ 32,98', 'R$ 19,00', 'R$ 30,37', 'R$ 35,72']
})
st.dataframe(pagamentos, use_container_width=True)

st.warning("💳 **Dinheiro** representa 87,4% da receita — elevada concentração que reduz previsibilidade de fluxo de caixa.")
st.info("📲 **PIX** tem o maior ticket médio (R$ 35,72) mesmo com o menor volume — estimular sua adoção pode elevar o ticket geral.")
st.info("💳 **Cartão de Crédito** tem o menor ticket médio (R$ 19,00) — mais usado em consultas e exames rápidos, não nos procedimentos que mais rentabilizam.")

# ─────────────────────────────────────────
# SAZONALIDADE
# ─────────────────────────────────────────
st.header("Sazonalidade e Evolução de Receita")
st.markdown("O faturamento acumulado de 2024 (R$ 78.760) e 2025 (R$ 79.176) é praticamente idêntico — crescimento de apenas **0,5%** no período. A estabilidade total, no entanto, mascara uma mudança importante no padrão mensal entre os dois anos.")

sazonalidade = pd.DataFrame({
    'Mês': ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
    '2024': ['R$ 10.302', 'R$ 7.612', 'R$ 12.330', 'R$ 7.628', 'R$ 9.444', 'R$ 4.967',
             'R$ 5.969', 'R$ 3.870', 'R$ 3.390', 'R$ 5.688', 'R$ 4.203', 'R$ 3.356'],
    '2025': ['R$ 6.168', 'R$ 3.558', 'R$ 3.125', 'R$ 3.866', 'R$ 2.831', 'R$ 4.327',
             'R$ 14.171', 'R$ 9.420', 'R$ 6.972', 'R$ 8.341', 'R$ 6.948', 'R$ 9.450'],
    'Variação': ['▼ 40,1%', '▼ 53,3%', '▼ 74,6%', '▼ 49,3%', '▼ 70,0%', '▼ 12,9%',
                 '▲ 137,4%', '▲ 143,4%', '▲ 105,7%', '▲ 46,6%', '▲ 65,3%', '▲ 181,5%']
})
st.dataframe(sazonalidade, use_container_width=True)

st.warning("📉 No primeiro semestre de 2025, o faturamento caiu em todos os meses — queda média de 50%. Sugere saída de profissionais, redução de agenda ou perda de convênios.")
st.success("📈 A partir de julho de 2025, a operação se recuperou com força — julho e agosto cresceram mais de 137% sobre o mesmo período em 2024.")
st.success("🏆 Dezembro de 2025 (R$ 9.450) representa crescimento de 181% sobre dezembro de 2024. Investigar o que foi feito nesse mês pode revelar boas práticas replicáveis.")

# ─────────────────────────────────────────
# CONCLUSÃO
# ─────────────────────────────────────────
st.header("Conclusão")
st.markdown("""
- A **Filial II–10** é a grande oportunidade de curto prazo — maior ticket médio com volume muito baixo
- **Ultrassonografia e Tomografia** são os procedimentos com maior potencial de alavancagem de receita
- A **dependência de Dinheiro** como forma de pagamento é um risco operacional que merece atenção
- A **recuperação do segundo semestre de 2025** é um sinal positivo, mas precisa ser investigada para garantir sustentabilidade

---
*Análise elaborada com base em 5.067 registros de atendimento. Dados de cidade e perfil demográfico dos pacientes disponíveis no banco PostgreSQL e não incluídos nesta análise.*

*VitaClin | Jan/2024 – Dez/2025*
""")
