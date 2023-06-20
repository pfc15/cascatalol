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

    


def linha(df, time):
    """
    faz gráfico em linha de um time
    """
    limpo = df.iloc[:, 9:].transpose()
    limpo.columns = df.iloc[:,0].transpose().tolist()
    #cascata(limpo, jogador)
    if time!="sai":
        df_plot = limpo[df.loc[df["time"]==time]["nick"]].dropna(how="any")
        plot.plot(df_plot)

def img_todos(df):
    """
    faz gráfico em linha com imagem dos jogadores nos pontos. plota todos os jogadores
    """
    fig, ax = plot.subplots()
    for jogador in df["nick"].values:
        limpo = df.iloc[:, 9:].transpose()
        limpo.columns = df.iloc[:,0].transpose().tolist()
        limpo = pd.DataFrame(limpo.values, index=limpo.index, columns=limpo.columns)
        limpo = limpo.dropna(how="any")
        y = pd.Series(limpo[jogador])
        x = pd.Series(range(1, len(limpo)+1))
        #image_path = get_sample_data('ada.png')
        
        imscatter(limpo.index, y, f"imgs/{jogador}.png", zoom=0.5,ax=ax)
        ax.plot(limpo.index, y)
    plot.title(f"cartinhas todos")
    plot.ylabel("nivel das cartinhas")
    plot.xlabel("semanas")
    refazer_ylabel(ax)



def img_time(df, time):
    """
    plota imagem do time com gráfico em linha
    """
    jogadores = df.loc[df["time"]==time]["nick"]
    fig, ax = plot.subplots()
    for jogador in jogadores.values:
        limpo = df.iloc[:, 9:].transpose()
        limpo.columns = df.iloc[:,0].transpose().tolist()
        limpo = pd.DataFrame(limpo.values, index=limpo.index, columns=limpo.columns)
        limpo = limpo.dropna(how="any")
        y = pd.Series(limpo[jogador])
        x = pd.Series(range(1, len(limpo)+1))
        #image_path = get_sample_data('ada.png')
        
        imscatter(limpo.index, y, f"imgs/{jogador}.png", zoom=0.3,ax=ax)
        ax.plot(limpo.index, y)
    plot.title(f"cartinhas {time}")
    plot.ylabel("nivel das cartinhas")
    plot.xlabel("semanas")
    refazer_ylabel(ax)
    st.pyplot(fig)
    
def refazer_ylabel(ax=None):
    """
    refaz o ylabel pra ficar de 0 a 100 com as cores divididas (bagre: vermelho, mais ou menos:amarelo, bom:verde, god:roxo)
    """
    if ax is None:
        ax = plot.gca()
    colors=["r","gold","lightgreen","purple"]
    y=[60,70,80,90,100]
    x=[0,0,0,0,0]
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = LineCollection(segments,colors=colors, linewidth=2,
                                transform=ax.get_yaxis_transform(), clip_on=False )
    ax.add_collection(lc)
    ax.spines["left"].set_visible(False)
    ax.set_yticks(y)

def imscatter(x, y, image, ax=None, zoom=1):
    """
    função suporte pras funções de plot de imagem, peguei do stackoverflow. Nem ideia de como funciona
    """
    if ax is None:
        ax = plt.gca()
    try:
        image = plot.imread(image)
    except TypeError:
        # Likely already an array...
        pass
    im = OffsetImage(image, zoom=zoom)
    #x, y = np.atleast_1d(x, y)
    artists = []
    for x0, y0 in zip(x, y):
        ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
        artists.append(ax.add_artist(ab))
    #ax.update_datalim(np.column_stack([x, y]))
    ax.autoscale()
    return artists



if __name__=="__main__":
    df = pd.read_excel("cartinhas.xlsx", "jogadores")
    print(df.head(10))
    limpo = df.iloc[:, 9:].transpose()
    limpo.columns = df.iloc[:,0].transpose().tolist()
    jogador = st.text_area("qual jogador vc quer ver? ")
    jogador = "".join(jogador.split())
     # codigo de ver o time
    if jogador in df.nick.values:
        cascata(limpo, jogador)

    time = st.text_area("qual time você quer ver?")
    time = " ".join(time.split())
    #cascata(limpo, jogador)
    #linha(df, time) # ver em linha
    if time in df.time.values:
        img_time(df, time)
    #img_todos(df)
    #cascata(limpo, jogador)

    #plot.show()