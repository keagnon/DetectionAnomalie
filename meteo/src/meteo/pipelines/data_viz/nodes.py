import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def correlation_matrix(data: pd.DataFrame, output_path: str) -> None:
    # Select relevant columns
    relevant_columns = ['TempMin_Deg', 'Wind_kmh', 'Wet_percent', 'Visibility_km', 'CloudCoverage_percent', 'Consommation journalière (MWh - PCS 0°C)']
    plt.figure(figsize=(10, 8))
    sns.heatmap(data[relevant_columns].corr(), annot=True, cmap='coolwarm')
    plt.title("Correlation Matrix")
    plt.savefig(output_path)
    plt.close()

def scatter_plot(data: pd.DataFrame, output_path: str) -> None:
    sns.scatterplot(x='TempMax_Deg', y='00:00', data=data)
    plt.title("TempMax vs Consommation d'Energie à 00:00")
    plt.savefig(output_path)
    plt.close()

def box_plot(data: pd.DataFrame, output_path: str) -> None:
    for hour in data.columns[11:]:  
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='CloudCoverage_percent', y=hour, data=data)
        plt.title(f'Cloud Coverage vs Consommation dEnergie à {hour}')
        plt.savefig(f"{output_path}_boxplot_{hour}.png")
        plt.close()
        
def box_plot2(data: pd.DataFrame, output_path: str) -> None:
    for hour in data.columns[11:]:  
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='TempMin_Deg', y=hour, data=data)
        plt.title(f'Temperature Minimale vs Consommation dEnergie à {hour}')
        plt.savefig(f"{output_path}_boxplot_{hour}.png")
        plt.close()

def box_plot3(data: pd.DataFrame, output_path: str) -> None:
    for hour in data.columns[11:]:  
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='TempMax_Deg', y=hour, data=data)
        plt.title(f'Temperature Maximale vs Consommation dEnergie à {hour}')
        plt.savefig(f"{output_path}_boxplot_{hour}.png")
        plt.close()



def box_plot4(data: pd.DataFrame, output_path: str) -> None:
    for hour in data.columns[11:]:  
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='Wet_percent', y=hour, data=data)
        plt.title(f'Wet_percent vs Consommation dEnergie à {hour}')
        plt.savefig(f"{output_path}_boxplot_{hour}.png")
        plt.close()
