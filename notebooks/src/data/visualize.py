import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches
import pandas as pd

colors = ["#20B2AA", "#B22028"]
sns.set_theme(style="whitegrid")
sns.set_palette(sns.color_palette(colors))

dict_columns = {
    'GENDER': 'Gênero',
    'AGE': 'Idade',
    'SMOKING': 'Fumante',
    'YELLOW_FINGERS': 'Dedos amarelados',
    'ANXIETY': 'Ansiedade',
    'PEER_PRESSURE' : 'Pressão grupal',
    'CHRONIC DISEASE' : 'Doença crônica',
    'FATIGUE' : 'Fadiga',
    'ALLERGY' : 'Alergia',
    'WHEEZING' :  'Pieira',
    'ALCOHOL CONSUMING' : 'Consumo alcoólico',
    'COUGHING' : 'Tosse',
    'SHORTNESS OF BREATH' : 'Falta de ar',
    'SWALLOWING DIFFICULTY' : 'Dificuldade de ingestão',
    'CHEST PAIN' : 'Dor torácica',
    'LUNG_CANCER' : 'Câncer Pulmonar',
}


def translate(variable): 
    x = dict_columns[variable]
    if (x is not None):
        return x
    else:
        return 'Variável não encontrada'

def variable_dist_count(df, var_name=None, compare=None, axe=None, horizontal=False):
    """Plot the distribution of a variable, returning a countplot"""
    if horizontal:
        ax = sns.countplot(data=df, y=df[var_name], hue=compare, ax=axe, alpha=1)
    else:
        ax = sns.countplot(data=df, x=df[var_name], hue=compare, ax=axe, alpha=1)

    abs_values = df[var_name].value_counts(ascending=False)
    rel_values = df[var_name].value_counts(ascending=False, normalize=True).values * 100
    labels = [f'{p[0]} ({p[1]:.0f}%)' for p in zip(abs_values, rel_values)]
    graph = ax.bar_label(ax.containers[0], labels=labels, label_type='edge', fontsize=12)
    if horizontal:
        #Set yLabel
        ax.set(
            ylabel=translate(var_name),
            xlabel='Quantidade',
        )
    else:
        #Set xLabel
        ax.set(
            xlabel=translate(var_name),
            ylabel='Quantidade',
        )
    sns.despine(left=True, bottom=False)
    return ax

def variable_dist_histogram(df, var_name, compare=None, axe=None, line=False):
    """Plot the distribution of a variable, returning a histplot"""
    ax = sns.histplot(data=df, x=df[var_name], kde=line, hue=compare, ax=axe, alpha=1)
    labels = [f'{(v.get_height()/ len(df) * 100 ):.1f} %' for v in ax.containers[0]]
    
    #Remove labels that are '0.0 %'
    #labels = [l for l in labels if l != '0.0 %']
    graph = ax.bar_label(ax.containers[0], labels=labels, label_type='edge', fontsize=9)
    ax.xaxis.grid(False)
    ax.set(
        ylabel='Quantidade',
        xlabel=translate(var_name)
    )
    sns.despine(left=True, bottom=False)
    return ax

def correlation(df, title, df_dict, annot=False):
    #corr = df[df_dict.query("Grupo == 'Sintoma'").Coluna.to_list()].replace(["Não", "Sim"], [0, 1]).corr()
    corr = df.corr()

    mask = np.triu(np.ones_like(corr, dtype=bool))

    f, ax = plt.subplots(figsize=(6, 6))

    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    ax = sns.heatmap(corr, mask=mask, cmap=cmap, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=annot, fmt=".2f")
    sintomas = df_dict.query("Grupo == 'Sintoma'").Variavel.to_list()
    for i in range(len(sintomas)):
        sintomas[i] = translate(sintomas[i])

    ax.set_xticklabels(sintomas)
    ax.set_yticklabels(sintomas)
    plt.suptitle(f"Correlação ({title})", fontweight='bold')
    return ax