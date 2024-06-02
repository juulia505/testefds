import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("dark")

cor_genero = ['#F781D8', '#819FF7']

df = pd.read_csv('https://raw.githubusercontent.com/V1n1ci0s/projeto-Kayo_ter-a/main/base%20dados.csv')
df.head()

# @title Tendência das taxas globais de suicídio ao longo do tempo por sex

import matplotlib.pyplot as plt

df_trend = df.groupby(['year', 'sex'])['suicides/100k pop'].mean().unstack()

df_trend.plot(kind='line', figsize=(10, 6))
plt.xlabel('Ano')
plt.ylabel('Taxa média de suicídio por 100 mil habitantes')
plt.title('Tendência das taxas globais de suicídio ao longo do tempo por sexo')
_ = plt.legend(title='Sex')

df.info()

df_brasil = df[df['country']=='Brazil'].copy()
df_brasil.head()

df_brasil.shape

print('Mundo------------')
display(df.isnull().sum())
print('Brasil----------')
display(df_brasil.isnull().sum())

#Pegar a média mundial e do Brasil em suicídios
anos = df_brasil.year.unique()
suicidio_brasil_media = df_brasil.groupby('year')['suicides/100k pop'].mean()
suicidio_mundial_media = df.groupby('year')['suicides/100k pop'].mean()
gdp_media_mundo = df.groupby('year')['gdp_per_capita ($)'].mean()
gdp_media_brasil = df_brasil.groupby('year')['gdp_per_capita ($)'].mean()

suicidio_mundial_media.drop(2016, inplace=True)

fig = plt.figure(figsize=(15,5))
ax = sns.lineplot(x=anos,y=suicidio_mundial_media, label='Mundial', color='blue')
ax = sns.lineplot(x=anos, y = suicidio_brasil_media, label='Brasil', color='green')
plt.title('Média de suicídio ao longo do tempo (Brasil X Mundo)', fontsize=19)
plt.ylabel('N° de casos a cada 100 mil pessoas',fontsize=13)


df.groupby('year')['suicides/100k pop'].sum()

tabela = pd.pivot_table(df_brasil, values='suicides_no', index=['year'], columns=['age'])
column_order = ['5-14 years', '15-24 years', '25-34 years', '35-54 years', '55-74 years', '+75 years']
tabela = tabela.reindex(column_order, axis=1)
tabela.head()

tabela2 = pd.pivot_table(df_brasil, values ='suicides/100k pop',index=['sex'],columns=['year'])
tabela2 = tabela2.T

26267 / tabela.sum().sum()

tabela.plot.bar(stacked=True,figsize=(16,8))
plt.legend(title='Idade')
plt.xlabel(' ')
plt.title(' Suicídio por faixa etária',fontsize=21);

df_brasil['generation'].value_counts().sum()

82 / df_brasil['generation'].value_counts().sum().sum()

fig = plt.figure(figsize=(13,5))
sns.countplot(x='generation', order = df_brasil['generation'].value_counts().index, data = df_brasil) # Changed 'generation' to x='generation'
plt.xlabel('Gerações', fontsize=13)
plt.ylabel(' ')
plt.title('Suicídio por geração',fontsize=21);

generos = df_brasil.groupby('sex').suicides_no.sum() / df_brasil.groupby('sex').suicides_no.sum().sum()

fig = plt.figure(figsize=(6,6))
plt.pie(generos, labels=['MULHERES', 'HOMENS'], colors = cor_genero, autopct='%1.1f%%', shadow = True, startangle=90)
plt.title('Número de suicídio por gênero (1985 - 2015)', fontsize=15);

#Quantas vezes a mais o homem se suicida em relação às mulheres?
df_brasil.groupby('sex').suicides_no.sum()[1] / df_brasil.groupby('sex').suicides_no.sum()[0]

tabela2.plot.bar(stacked=True, figsize=(15,5), color=cor_genero)
plt.xlabel(' ')
plt.title('Gênero ao longo do tempo', fontsize=19)
plt.ylabel('N° de suicídio a cada 100 mil pessoas', fontsize=13);

mulheres = df.groupby(['sex', 'age'])['suicides_no'].sum()[:6] # sexo e idade --> numero de suicidios --> somar e pegar os 6 primeiros
homens = df.groupby(['sex', 'age'])['suicides_no'].sum()[6:] # sexo e idade --> numero de suicidios --> somar e pegar os 6 ultimos
m = [] # Mulheres
h = [] # Homens
mn = [] # Numero de mulheres
hn = [] # Numero de homens
for i in range(6):
  m.append(mulheres.index[i][1].split(' ')[0])
  h.append(homens.index[i][1].split(' ')[0])
  mn.append(mulheres[i])
  hn.append(homens[i])


fig = plt.figure(figsize=(10,5))
sns.barplot(x=m, y = mn) # Remove the 'data' parameter as it's not needed when directly passing x and y values
plt.title('Faixa etária (mulheres)', fontsize=19);

fig = plt.figure(figsize=(10,5))
sns.barplot(x=h, y = hn) # Remove the 'data' parameter as it's not needed when directly passing x and y values
plt.title('Faixa etária (homens)', fontsize=19);

print(f'''
Total de homens: {sum(hn)}
Total de mulheres: {sum(mn)}
''')


fig = plt.figure(figsize=(15,5))
ax = sns.lineplot(x=anos,y=gdp_media_brasil, color = 'green')
plt.ylabel('PIB per capita ($)', fontsize=15)
plt.title('PIB per capita ao longo do tempo',fontsize=19);

fig = plt.figure(figsize=(15,5))
sns.regplot(x=gdp_media_brasil, y =suicidio_brasil_media, data=df_brasil, color='green')
plt.title('Correlação entre PIB per capita e número de suicídios por 100 mil habitantes',fontsize=15)
plt.ylabel('Média de suicídio / 100k habitantes', fontsize=13)
plt.xlabel('PIB per capita ($)',fontsize=11)



fig = plt.figure(figsize=(15,5))
sns.lineplot(x=anos, y =suicidio_brasil_media, color = 'green')
plt.title('Média de suicídio a cada ano por 100 mil habitantes', fontsize=15)
plt.ylabel('Média de suicídio / 100k habitantes', fontsize=13)


fig = plt.figure(figsize=(15,5))
sns.regplot(x=anos, y =suicidio_brasil_media, data=df_brasil, color='green')
plt.title('Média de suicídio no Brasil a cada 100 mil habitantes ao longo do tempo',fontsize=17)
plt.ylabel('Média de suicídio / 100k habitantes', fontsize=13)
plt.xlabel('Anos',fontsize=13)
sns.lineplot(x=anos, y =suicidio_brasil_media, color = 'green')
