import pandas as pd
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plot
import waterfall_chart
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.collections import LineCollection
import streamlit as st


def cascata(df, nome_procurado):
    """
    função criar gráfico em cascata de um jogador apenas
    """
    procurado = df[nome_procurado]
    lista = pd.Series()
    anterior =0
    for e in procurado.index:
        if e==procurado.index[0]:
            anterior= procurado[e]
            lista[e] = procurado[e]
        else:
            lista[e] =  procurado[e] - anterior
            anterior = procurado[e]
    
    procurado = pd.DataFrame(procurado.values, index=procurado.index, columns=["jogador"])
    procurado = procurado.assign(delta=lista.values)
    procurado = procurado.dropna(how="any")
    print(procurado)
    st.pyplot(waterfall_chart.plot(procurado.index, procurado["delta"], trocay=True, net_label="média", media=np.mean(procurado["jogador"])))
    plot.title(f"gráfico cascata cartinhas {nome_procurado}")

if __name__=="__main__":
    df = pd.read_excel("cartinhas.xlsx", "jogadores")
    print(df.head(10))
    limpo = df.iloc[:, 9:].transpose()
    limpo.columns = df.iloc[:,0].transpose().tolist()
    jogador = st.text_area("qual jogador vc quer ver? ", max=20)
    if jogador in df.nick.values:
        cascata(limpo, jogador)
