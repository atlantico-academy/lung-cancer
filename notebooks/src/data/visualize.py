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
    'LUNG_CANCER' : 'Câncer pulmonar',
}


def translate(variable): 
    x = dict_columns[variable]
    if (x is not None):
        return x
    else:
        return 'Variável não encontrada'

def variable_dist_count(df, var_name=None, compare=None, axe=None, horizontal=False,):

    """Plot the distribution of a variable, returning a countplot"""
    if horizontal:
        ax = sns.countplot(data=df, y=df[var_name], hue=compare, ax=axe, alpha=1)
    else:
        ax = sns.countplot(data=df, x=df[var_name], hue=compare, ax=axe, alpha=1)
    

    if (compare):
        plt.legend(title=translate(compare))
        for container in ax.containers:
            tmp_hue = df.loc[df[compare]==container.get_label()]
            #Show value and percetage
            abs_val = tmp_hue[var_name].value_counts(ascending=False)
            rel_val = tmp_hue[var_name].value_counts(ascending=False, normalize=True).values * 100
            labels = [f'{p[0]} ({p[1]:.0f}%)' for p in zip(abs_val, rel_val)]
            graph = ax.bar_label(container, labels=labels, label_type='edge', fontsize=12)
    else:
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

def variable_dist_histogram(df, var_name, axe=None, line=False, opacity=1):
    """Plot the distribution of a variable, returning a histplot"""
    ax = sns.histplot(data=df, x=df[var_name], kde=line, ax=axe, alpha=opacity)

    labels = [f'{(v.get_height()/ len(df) * 100 ):.1f} %' for v in ax.containers[0]]
    graph = ax.bar_label(ax.containers[0], labels=labels, label_type='edge', fontsize=9)

    ax.xaxis.grid(False)
    ax.set(
        ylabel='Quantidade',
        xlabel=translate(var_name)
    )
    sns.despine(left=True, bottom=False)
    return ax

def correlation(df, df_dict, annot=False):
    #corr = df[df_dict.query("Grupo == 'Sintoma'").Coluna.to_list()].replace(["Não", "Sim"], [0, 1]).corr()
    corr = df.corr()

    mask = np.triu(np.ones_like(corr, dtype=bool))

    f, ax = plt.subplots(figsize=(7, 7))

    cmap = sns.diverging_palette(220, 20, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    ax = sns.heatmap(corr, mask=mask, cmap=cmap, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=annot, fmt=".2f")
    sintomas = df_dict.query("Grupo == 'Sintoma'").Variavel.to_list()
    for i in range(len(sintomas)):
        sintomas[i] = translate(sintomas[i])

    ax.set_xticklabels(sintomas)
    ax.set_yticklabels(sintomas)
    return ax

def dist_sintomas(df, df_dict, configuration=None, axe=None):
    df_sintomas = df.melt(value_vars=df_dict.query("Grupo == 'Sintoma'").Variavel.to_list())
    #df_sintomas = df_sintomas.replace(["Não", "Sim"], [0, 1])
    df_sintomas = df_sintomas.groupby(['variable', 'value']).size().reset_index(name='count')
    df_sintomas = df_sintomas.rename(columns={'variable': 'Sintoma', 'value': 'Ocorrência'})
    df_sintomas['Sintoma'] = df_sintomas['Sintoma'].apply(translate)
    #Ordena os sintomas por ordem alfabética
    #df_sintomas = df_sintomas.sort_values(by=['Sintoma'])
    
    if configuration:
        #If the configurations says to show only lung_cancer yes
        if configuration['lung_cancer'] == 'yes':
            df_sintomas = df_sintomas.query("Ocorrência == 'Sim'")
        if configuration['lung_cancer'] == 'no':
            df_sintomas = df_sintomas.query("Ocorrência == 'Não'")

    ax = sns.barplot(data=df_sintomas, y='Sintoma', x='count', hue='Ocorrência', hue_order=['Sim', 'Não'], ax=axe)

    for container in ax.containers:
        #Create label for each bar
        tmp_hue = df_sintomas.loc[df_sintomas['Ocorrência']==container.get_label()]
        #Show value and percetage
        abs_val = tmp_hue['count']
        rel_val = tmp_hue['count'].values / df_sintomas['count'].sum() * 100
        labels = [f'{p[0]}' for p in zip(abs_val, rel_val)]
        graph = ax.bar_label(container, labels=labels, label_type='edge', fontsize=12)

    ax.set(
        xlabel='Quantidade',
        ylabel='Sintoma'
    )
    return ax

def sintomas_statistics(df, axe=None):
    #Get mean, median, min and max of symptons, grouped by cancer
    symptons_data = df.groupby('LUNG_CANCER')['Sintomas'].agg(['mean', 'median', 'min', 'max'])

    #Subplots
    ax = sns.barplot(data=symptons_data, x=symptons_data.index, y='mean', ax=axe, order=[1, 0])

    #edit x and y labels
    ax.set(xlabel='Câncer pulmonar', ylabel='Média de sintomas')
    ax.set_xticklabels(['Sim', 'Não'])
    #add title
    ax.set_title('Média de sintomas por paciente', fontweight='bold')
    #add bar_label using height
    labels = ax.bar_label(
        ax.containers[0],
        fmt='%.1f', #1 casa decimal
    )
    sns.despine(left=True, bottom=False)
    return ax

def boxplot_sintomas(df, y=None, axe=None):
    ax = sns.boxplot(data=df, x='Sintomas', y=y, orient='h', ax=axe, order=[1, 0])
    #edit x and y labels
    ax.set(xlabel='Sintomas', ylabel='Câncer pulmonar')
    #add title
    ax.set_title('Distribuição de sintomas por paciente', fontweight='bold')
    #edit y ticks
    ax.set_yticklabels(['Sim', 'Não'])
    #add labels
    sns.despine(left=True, bottom=False)
