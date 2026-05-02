import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from matplotlib.patches import Patch
import warnings

warnings.filterwarnings('ignore')

sns.set_theme(style='whitegrid', palette='muted')
plt.rcParams['figure.dpi'] = 110
plt.rcParams['font.family'] = 'DejaVu Sans'

# ─────────────────────────────────────────
# TÍTULO
# ─────────────────────────────────────────
st.title("Análise Exploratória de Dados — VitaClin")
st.markdown("""
Este app explora os dados de atendimentos clínicos da VitaClin,
investigando a estrutura, identificando inconsistências e transformando
dados brutos em informação útil para o negócio.
""")

# ─────────────────────────────────────────
# CARREGANDO OS DADOS
# ─────────────────────────────────────────
st.header("Estrutura do Dataset")
st.subheader("Carregando os Dados")

df = pd.read_csv(
    'Base Vitaclin.csv',
    sep=';',
    decimal=',',
    encoding='utf-8'
)

st.success("✅ Arquivo carregado com sucesso!")
st.write(f"O dataset possui **{df.shape[0]}** linhas e **{df.shape[1]}** colunas.")

# ─────────────────────────────────────────
# PRIMEIRAS LINHAS
# ─────────────────────────────────────────
st.subheader("Primeiras 5 Linhas do Dataset")
st.dataframe(df.head(), use_container_width=True)

# ─────────────────────────────────────────
# DIMENSÕES
# ─────────────────────────────────────────
st.subheader("Dimensões do Arquivo")

linhas, colunas = df.shape
st.write(f"O dataset possui **{linhas}** linhas e **{colunas}** colunas.")
st.write("**Colunas disponíveis:**")
for col in df.columns:
    st.write(f"• {col}")

# ─────────────────────────────────────────
# TIPOS E NULOS
# ─────────────────────────────────────────
st.subheader("Tipos de Dados e Valores Nulos")

st.write("**Tipos de dados por coluna:**")
st.write(df.dtypes)

st.write("**Valores nulos por coluna:**")
nulos = df.isnull().sum()
st.write(nulos)
st.write(f"Total de células nulas no dataset: **{nulos.sum()}**")

# ─────────────────────────────────────────
# LIMPEZA E TRATAMENTO
# ─────────────────────────────────────────
st.header("Limpeza e Tratamento dos Dados")

# 1. Converter data
df['data_atendimento'] = pd.to_datetime(df['data_atendimento'], format='%d/%m/%Y', errors='coerce')

# 2. Remover espaços extras
df['nomeunidade'] = df['nomeunidade'].str.strip()

# 3. Padronização defensiva
df['grupoprocedimento'] = df['grupoprocedimento'].str.strip()

# 4. Remover linhas sem valor_pago ou paciente_id
antes = df.shape[0]
df = df.dropna(subset=['valor_pago', 'paciente_id'])
st.write(f"Removidas **{antes - df.shape[0]}** linhas com dados essenciais faltando.")

# 5. Corrigir tipos dos IDs
df['paciente_id'] = df['paciente_id'].astype(int)
df['idprofissional'] = df['idprofissional'].fillna(0).astype(int)

# 6. Outlier de valor_pago
st.write("**Outlier detectado (valor muito acima do esperado):**")
outliers = df[df['valor_pago'] > 5000][['data_atendimento', 'nomeprocedimento', 'valor_pago', 'nomeunidade']]
st.dataframe(outliers, use_container_width=True)
df = df[df['valor_pago'] <= 5000]

# 7. Coluna auxiliar mês/ano
df['mes'] = df['data_atendimento'].dt.to_period('M')

st.success("✅ Dados limpos e prontos para análise!")
st.write(f"Linhas restantes: **{df.shape[0]}**")
st.write(f"Período coberto: **{df['data_atendimento'].min().date()}** até **{df['data_atendimento'].max().date()}**")

# ─────────────────────────────────────────
# ESTATÍSTICAS DESCRITIVAS
# ─────────────────────────────────────────
st.subheader("Estatísticas Descritivas")
st.dataframe(df.describe(), use_container_width=True)

# ─────────────────────────────────────────
# VALOR TOTAL POR MÊS
# ─────────────────────────────────────────
st.header("Valor Total Atendido por Mês")

valor_mes = (df.groupby('mes')['valor_pago']
               .sum()
               .reset_index())
valor_mes.columns = ['Mês', 'Valor Total (R$)']
valor_mes['Valor Total (R$)'] = valor_mes['Valor Total (R$)'].round(2)
valor_mes['Mês'] = valor_mes['Mês'].astype(str)

st.write("**Valor total atendido por mês:**")
st.dataframe(valor_mes, use_container_width=True)

fig, ax = plt.subplots(figsize=(14, 5))
ax.fill_between(valor_mes['Mês'], valor_mes['Valor Total (R$)'], alpha=0.12, color='steelblue')
ax.plot(valor_mes['Mês'], valor_mes['Valor Total (R$)'],
        marker='o', color='steelblue', linewidth=2.5, markersize=6, label='Valor mensal')

for _, row in valor_mes.iterrows():
    ax.annotate(
        f"R${row['Valor Total (R$)']:,.0f}",
        xy=(row['Mês'], row['Valor Total (R$)']),
        xytext=(0, 10), textcoords='offset points',
        ha='center', fontsize=7.5, color='steelblue'
    )

ax.set_title('Valor Total Atendido por Mês', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Mês', fontsize=11)
ax.set_ylabel('Valor Total (R$)', fontsize=11)

fmt = mticker.FuncFormatter(lambda x, _: f'R${x:,.0f}')
ax.yaxis.set_major_formatter(fmt)

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig)

mes_maior = valor_mes.loc[valor_mes['Valor Total (R$)'].idxmax()]
mes_menor = valor_mes.loc[valor_mes['Valor Total (R$)'].idxmin()]
st.info(f"📈 Mês com maior faturamento: **{mes_maior['Mês']}** → R$ {mes_maior['Valor Total (R$)']:,.2f}")
st.info(f"📉 Mês com menor faturamento: **{mes_menor['Mês']}** → R$ {mes_menor['Valor Total (R$)']:,.2f}")
st.info(f"📊 Faturamento médio mensal: R$ {valor_mes['Valor Total (R$)'].mean():,.2f}")

# ─────────────────────────────────────────
# QUANTIDADE DE ATENDIMENTOS POR MÊS
# ─────────────────────────────────────────
st.header("Quantidade de Atendimentos por Mês")

atend_mes = (df.groupby('mes')
               .size()
               .reset_index(name='Qtd Atendimentos'))
atend_mes.columns = ['Mês', 'Qtd Atendimentos']
atend_mes['Mês'] = atend_mes['Mês'].astype(str)

st.write("**Quantidade de atendimentos por mês:**")
st.dataframe(atend_mes, use_container_width=True)

fig, ax = plt.subplots(figsize=(14, 5))
cores = ['#e07b54' if m.startswith('2025') else '#5b8db8' for m in atend_mes['Mês']]
bars = ax.bar(atend_mes['Mês'], atend_mes['Qtd Atendimentos'],
              color=cores, edgecolor='white', width=0.7)

for bar in bars:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 2,
        str(int(bar.get_height())),
        ha='center', va='bottom', fontsize=8.5
    )

legenda = [Patch(color='#5b8db8', label='2024'), Patch(color='#e07b54', label='2025')]
ax.legend(handles=legenda, fontsize=10)
ax.set_title('Quantidade de Atendimentos por Mês', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Mês', fontsize=11)
ax.set_ylabel('Nº de Atendimentos', fontsize=11)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig)

media = atend_mes['Qtd Atendimentos'].mean()
mes_pico = atend_mes.loc[atend_mes['Qtd Atendimentos'].idxmax()]
st.info(f"📊 Média mensal de atendimentos: **{media:.0f}**")
st.info(f"📈 Mês com mais atendimentos: **{mes_pico['Mês']}** ({int(mes_pico['Qtd Atendimentos'])} atendimentos)")
st.info(f"🔢 Total geral de atendimentos: **{atend_mes['Qtd Atendimentos'].sum()}**")

# ─────────────────────────────────────────
# TOP 5 PACIENTES
# ─────────────────────────────────────────
st.header("Top 5 Pacientes com Maior Frequência")

top5 = (df.groupby('paciente_id')
          .agg(
              total_atendimentos=('paciente_id', 'count'),
              valor_total=('valor_pago', 'sum'),
              ticket_medio=('valor_pago', 'mean'),
              primeiro_atend=('data_atendimento', 'min'),
              ultimo_atend=('data_atendimento', 'max')
          )
          .sort_values('total_atendimentos', ascending=False)
          .head(5)
          .reset_index())

top5['valor_total'] = top5['valor_total'].round(2)
top5['ticket_medio'] = top5['ticket_medio'].round(2)
top5.columns = ['ID Paciente', 'Total Atendimentos', 'Valor Total (R$)',
                'Ticket Médio (R$)', 'Primeiro Atend.', 'Último Atend.']

st.write("**Top 5 Pacientes com Maior Frequência de Atendimento:**")
st.dataframe(top5, use_container_width=True)

fig, ax = plt.subplots(figsize=(10, 5))
ids = top5['ID Paciente'].astype(str)
qtds = top5['Total Atendimentos']
palette = sns.color_palette('Blues_d', len(ids))

bars = ax.barh(ids, qtds, color=palette, edgecolor='white', height=0.55)

for bar, val in zip(bars, qtds):
    ax.text(
        bar.get_width() + 0.5,
        bar.get_y() + bar.get_height() / 2,
        f'{val} atendimentos',
        va='center', fontsize=10
    )

ax.set_title('Top 5 Pacientes por Frequência de Atendimento', fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Nº de Atendimentos', fontsize=11)
ax.set_ylabel('ID do Paciente', fontsize=11)
ax.invert_yaxis()
ax.set_xlim(0, qtds.max() * 1.2)
plt.tight_layout()
st.pyplot(fig)

st.info(f"👤 O paciente mais frequente (ID {top5.iloc[0]['ID Paciente']}) realizou **{int(top5.iloc[0]['Total Atendimentos'])} atendimentos** no período, com ticket médio de **R$ {top5.iloc[0]['Ticket Médio (R$)']:,.2f}** por visita.")
st.info(f"👥 Esses 5 pacientes juntos somam **{int(qtds.sum())} atendimentos** — média de **{qtds.mean():.0f}** atendimentos por paciente nesse grupo.")

# ─────────────────────────────────────────
# RESUMO DOS INSIGHTS
# ─────────────────────────────────────────
st.header("Resumo dos Insights")
st.markdown("""
Após a limpeza e análise dos dados, os principais achados foram:

- O dataset continha **inconsistências** em nomes de unidades e grupos de procedimentos
- **Exames Laboratoriais** é a categoria mais frequente, representando mais da metade dos atendimentos
- O volume e o faturamento variam bastante ao longo dos meses, com picos em **março/2024** e **julho/2025**
- Os **Top 5 pacientes** têm entre 58 e 82 atendimentos cada — perfil de alta frequência
- **Dinheiro** representa 87% da receita; **PIX** tem o maior ticket médio (R$ 35,72) apesar do menor volume

---
*Análise exploratória — VitaClin | Jan/2024 – Dez/2025*
""")
