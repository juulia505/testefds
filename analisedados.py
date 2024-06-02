import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("dark")

cor_genero = ['#F781D8', '#819FF7']

df = pd.read_csv('https://raw.githubusercontent.com/V1n1ci0s/projeto-Kayo_ter-a/main/base%20dados.csv')

# Exibir o dataframe inicial
st.write(df.head())

# Tendência das taxas globais de suicídio ao longo do tempo por sexo
df_trend = df.groupby(['year', 'sex'])['suicides/100k pop'].mean().unstack()

fig, ax = plt.subplots(figsize=(10, 6))
df_trend.plot(kind='line', ax=ax)
ax.set_xlabel('Ano')
ax.set_ylabel('Taxa média de suicídio por 100 mil habitantes')
ax.set_title('Tendência das taxas globais de suicídio ao longo do tempo por sexo')
ax.legend(title='Sex')
st.pyplot(fig)

# Informações do dataframe
st.write(df.info())

# Filtrando dados do Brasil
df_brasil = df[df['country']=='Brazil'].copy()

# Exibindo o dataframe do Brasil
st.write(df_brasil.head())

# Forma dos dataframes
st.write("Forma do dataframe mundial:", df.shape)
st.write("Forma do dataframe do Brasil:", df_brasil.shape)

# Valores nulos
st.write('Mundo------------')
st.write(df.isnull().sum())
st.write('Brasil----------')
st.write(df_brasil.isnull().sum())

# Média de suicídios no Brasil e mundial ao longo dos anos
anos = df_brasil['year'].unique()
suicidio_brasil_media = df_brasil.groupby('year')['suicides/100k pop'].mean()
suicidio_mundial_media = df.groupby('year')['suicides/100k pop'].mean()
gdp_media_mundo = df.groupby('year')['gdp_per_capita ($)'].mean()
gdp_media_brasil = df_brasil.groupby('year')['gdp_per_capita ($)'].mean()

suicidio_mundial_media.drop(2016, inplace=True)

fig, ax = plt.subplots(figsize=(15, 5))
sns.lineplot(x=anos, y=suicidio_mundial_media, label='Mundial', color='blue', ax=ax)
sns.lineplot(x=anos, y=suicidio_brasil_media, label='Brasil', color='green', ax=ax)
ax.set_title('Média de suicídio ao longo do tempo (Brasil X Mundo)', fontsize=19)
ax.set_ylabel('N° de casos a cada 100 mil pessoas', fontsize=13)
st.pyplot(fig)

# Tabela de suicídios por faixa etária no Brasil
tabela = pd.pivot_table(df_brasil, values='suicides_no', index=['year'], columns=['age'])
column_order = ['5-14 years', '15-24 years', '25-34 years', '35-54 years', '55-74 years', '+75 years']
tabela = tabela.reindex(column_order, axis=1)
st.write(tabela.head())

tabela2 = pd.pivot_table(df_brasil, values='suicides/100k pop', index=['sex'], columns=['year'])
tabela2 = tabela2.T

fig, ax = plt.subplots(figsize=(16, 8))
tabela.plot.bar(stacked=True, ax=ax)
ax.legend(title='Idade')
ax.set_xlabel(' ')
ax.set_title('Suicídio por faixa etária', fontsize=21)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(13, 5))
sns.countplot(x='generation', order=df_brasil['generation'].value_counts().index, data=df_brasil, ax=ax)
ax.set_xlabel('Gerações', fontsize=13)
ax.set_ylabel(' ')
ax.set_title('Suicídio por geração', fontsize=21)
st.pyplot(fig)

generos = df_brasil.groupby('sex').suicides_no.sum() / df_brasil.groupby('sex').suicides_no.sum().sum()

fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(generos, labels=['MULHERES', 'HOMENS'], colors=cor_genero, autopct='%1.1f%%', shadow=True, startangle=90)
ax.set_title('Número de suicídio por gênero (1985 - 2015)', fontsize=15)
st.pyplot(fig)

# Quantidade de suicídios por gênero no Brasil
st.write(f"Quantas vezes a mais o homem se suicida em relação às mulheres? {df_brasil.groupby('sex').suicides_no.sum()[1] / df_brasil.groupby('sex').suicides_no.sum()[0]}")

fig, ax = plt.subplots(figsize=(15, 5))
tabela2.plot.bar(stacked=True, color=cor_genero, ax=ax)
ax.set_xlabel(' ')
ax.set_title('Gênero ao longo do tempo', fontsize=19)
ax.set_ylabel('N° de suicídio a cada 100 mil pessoas', fontsize=13)
st.pyplot(fig)

# Faixa etária por sexo
mulheres = df.groupby(['sex', 'age'])['suicides_no'].sum()[:6]
homens = df.groupby(['sex', 'age'])['suicides_no'].sum()[6:]

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=[x.split(' ')[0] for x in mulheres.index.get_level_values(1)], y=mulheres.values, ax=ax)
ax.set_title('Faixa etária (mulheres)', fontsize=19)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=[x.split(' ')[0] for x in homens.index.get_level_values(1)], y=homens.values, ax=ax)
ax.set_title('Faixa etária (homens)', fontsize=19)
st.pyplot(fig)

st.write(f'''
Total de homens: {sum(homens)}
Total de mulheres: {sum(mulheres)}
''')

fig, ax = plt.subplots(figsize=(15, 5))
sns.lineplot(x=anos, y=gdp_media_brasil, color='green', ax=ax)
ax.set_ylabel('PIB per capita ($)', fontsize=15)
ax.set_title('PIB per capita ao longo do tempo', fontsize=19)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(15, 5))
sns.regplot(x=gdp_media_brasil, y=suicidio_brasil_media, ax=ax, color='green')
ax.set_title('Correlação entre PIB per capita e número de suicídios por 100 mil habitantes', fontsize=15)
ax.set_ylabel('Média de suicídio / 100k habitantes', fontsize=13)
ax.set_xlabel('PIB per capita ($)', fontsize=11)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(15, 5))
sns.lineplot(x=anos, y=suicidio_brasil_media, color='green', ax=ax)
ax.set_title('Média de suicídio a cada ano por 100 mil habitantes', fontsize=15)
ax.set_ylabel('Média de suicídio / 100k habitantes', fontsize=13)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(15, 5))
sns.regplot(x=anos, y=suicidio_brasil_media, ax=ax, color='green')
ax.set_title('Média de suicídio no Brasil a cada 100 mil habitantes ao longo do tempo', fontsize=17)
ax.set_ylabel('Média de suicídio / 100k habitantes', fontsize=13)
ax.set_xlabel('Anos', fontsize=13)
sns.lineplot(x=anos, y=suicidio_brasil_media, color='green', ax=ax)
st.pyplot(fig)
