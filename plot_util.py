import pandas as pd

import matplotlib.pyplot as plt

import seaborn as sns

def plot_pie_chart(flats, column, explode=None):
    plt.figure(figsize=(8,8))  
    flats[column].value_counts().plot.pie(explode=explode, autopct='%1.0f%%',shadow=False, startangle=90,  
                                                 pctdistance=0.5, labeldistance=1.2)
    
def plot_box_chart(flats, column, map_values = None):
    flats.boxplot(column=['price'], by=column,patch_artist=True, figsize=(12, 8))
    if map_values is not None:
        plt.xticks(map_values[0], map_values[1])
    
def plot_linear_chart(flats, column, column_values=None, labels=None):
    plt.figure(figsize=(12,7))  
    if labels is None:
        labels = column_values
    sns.set_style("white")
    
    if column_values is None:
        sns.distplot(flats[column], bins=30)
    else:
        for column_value, label in zip(column_values, labels):
            x1 = flats.loc[flats[column]==column_value].price
            sns.distplot(x1, label=label)
    plt.legend()
    
def boxplot_sorted(df, by, column, rot=45):  
    df2 = pd.DataFrame({col:vals[column] for col, vals in df.groupby(by)})
    meds = df2.median().sort_values()
    df2[meds.index].boxplot(rot=rot, return_type="axes", figsize=(12,8))