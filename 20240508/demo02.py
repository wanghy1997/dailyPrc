import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def heart_uncertainty_analysis():

    dice = np.array([91.78, 93.02, 91.66, 91.53, 91.76, 92.68, 91.52, 92.05, 92.21, 91.53, 92.40, 92.57, 91.39, 92.44, 92.71])
    # criteria
    g_entropy = np.array([0.09624864, 0.10438952, 0.112696625, 0.107479796, 0.09908596, 0.10323209, 0.10586094, 0.10880481, 0.102086835, 0.10478308, 0.10547292, 0.09755077, 0.09970844, 0.09978076, 0.0993084])
    g_variance = np.array([0.0007410991, 0.0007787661, 0.0007852277, 0.0006981299, 0.0007505929, 0.0007901678, 0.00080709014, 0.0008880724, 0.00085439533, 0.0007861404, 0.0007766993, 0.00073064637, 0.0007763258, 0.0008860531, 0.0008081362])
    l_entropy = np.array([0.1499221, 0.15049969, 0.15507613, 0.17475882, 0.15753883, 0.15868041, 0.13786823, 0.1530365, 0.14532569, 0.13774836, 0.14960463, 0.16460678, 0.14865454, 0.14650092, 0.14159192])
    l_variance = np.array([0.0012267901, 0.0012823908, 0.001209656, 0.0012824732, 0.001314869, 0.0012151236, 0.0011785227, 0.0012883326, 0.0012991482, 0.0011873981, 0.0012311919, 0.0012872189, 0.00123623, 0.0012977166, 0.0012387078])

    sns.set_style("whitegrid")
    plt.rc('axes', labelsize=20)
    fig, axes = plt.subplots(1, 4, figsize=(40, 10))
    fig1 = sns.regplot(ax=axes[0], x=g_entropy, y=dice, scatter_kws={'s':120})
    cor, pval = stats.pearsonr(g_entropy, dice)
    axes[0].set_title(f"Global (Entropy) PCC={cor:.3f}", fontsize='30')
    axes[0].set(xlabel='Uncertainty Score', ylabel='Dice Score (%)')
    fig1.tick_params(axis='both', which='major', labelsize=18)

    fig2 = sns.regplot(ax=axes[1], x=g_variance, y=dice, scatter_kws={'s':120})
    cor, pval = stats.pearsonr(g_variance, dice)
    axes[1].set_title(f"Global (Variance) PCC={cor:.3f}", fontsize='30')
    axes[1].set(xlabel='Uncertainty Score', ylabel='Dice Score (%)')
    fig2.tick_params(axis='both', which='major', labelsize=18)

    fig3 = sns.regplot(ax=axes[2], x=l_entropy, y=dice, scatter_kws={'s':120})
    cor, pval = stats.pearsonr(l_entropy, dice)
    axes[2].set_title(f"Local (entropy) PCC={cor:.3f}", fontsize='30')
    axes[2].set(xlabel='Uncertainty Score', ylabel='Dice Score (%)')
    fig3.tick_params(axis='both', which='major', labelsize=18)

    fig4 = sns.regplot(ax=axes[3], x=l_variance, y=dice, scatter_kws={'s':120})
    cor, pval = stats.pearsonr(l_variance, dice)
    axes[3].set_title(f"Local (Variance) PCC={cor:.3f}", fontsize='30')
    axes[3].set(xlabel='Uncertainty Score', ylabel='Dice Score (%)')
    fig4.tick_params(axis='both', which='major', labelsize=18)

    # plt.savefig(f"heart_uncertainty_analysis.png")
    plt.show()


if __name__ == '__main__':
    heart_uncertainty_analysis()