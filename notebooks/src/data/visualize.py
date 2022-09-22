import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches
import pandas as pd

colors = ["#20B2AA", "#B22028"]
sns.set_theme(style="whitegrid")
sns.set_palette(sns.color_palette(colors))

def variable_dist_count(df, var_name=None, compare=None, axe=None, horizontal=False):
    """Plot the distribution of a variable, returning a countplot"""
    if horizontal:
        ax = sns.countplot(data=df, y=df[var_name], hue=compare, ax=axe, alpha=1)
    else:
        ax = sns.countplot(data=df, x=df[var_name], hue=compare, ax=axe, alpha=1)
    labels = [f'{(v.get_height() / len(df) * 100):.1f} %' for v in ax.containers[0]]
    graph = ax.bar_label(ax.containers[0], labels=labels, label_type='edge', fontsize=12)
    ax.set(
        ylabel='Quantidade',
    )
    sns.despine(left=True, bottom=False)
    return ax

def variable_dist_histogram(df, var_name, compare=None, axe=None, line=False):
    """Plot the distribution of a variable, returning a histplot"""
    ax = sns.histplot(data=df, x=df[var_name], kde=line, hue=compare, ax=axe, alpha=1)
    labels = [f'{(v.get_height() / len(df) * 100 ):.1f} %' for v in ax.containers[0]]
    
    #Remove labels that are '0.0 %'
    #labels = [l for l in labels if l != '0.0 %']
    graph = ax.bar_label(ax.containers[0], labels=labels, label_type='edge', fontsize=8)
    ax.xaxis.grid(False)
    ax.set(
        ylabel='Quantidade',
    )
    sns.despine(left=True, bottom=False)
    return ax

def correlation(df, title, annot=False ):
    # corr = df[df_dict.query("Grupo == 'Sintoma'").Coluna.to_list()].replace(["Não", "Sim"], [0, 1]).corr()
    corr = df.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(6, 6))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, cmap=cmap, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=annot, fmt=".2f")
    plt.suptitle(f"Correlação ({title})", fontweight='bold')
    plt.show()