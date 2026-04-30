"""
Project Fusion main exection file (LUI)
by Khang Luong and Anthony Storm
CSCE 311, University of Nebraska-Lincoln
"""

import data_structure as ds
import toolbox as tools
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
sns.set_palette('husl')
import pandas as pd
pd.set_option('display.max_columns', None)
plt.style.use('seaborn-v0_8-darkgrid')
plt.rc('axes', titlesize=18)     # fontsize of the axes title
plt.rc('axes', labelsize=14)     # fontsize of the x and y labels
plt.rc('xtick', labelsize=13)    # fontsize of the tick labels
plt.rc('ytick', labelsize=13)    # fontsize of the tick labels
plt.rc('legend', fontsize=13)    # legend fontsize
plt.rc('font', size=13)          # controls default text sizes
# Color for better printing
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


class Execution:
    def __init__(self, data_file):
        self.data_file = data_file
        self.clean_data()
        # Initialize BST for efficient lookup as per project requirements
        self.yield_bst = ds.Binary_Search_Tree()
        self.populate_bst()

    def clean_data(self):
        df = pd.read_csv(self.data_file)
        # Future Dev: Consider moving this to toolbox.py if a generic calculation module is created.
        df['Overall Efficiency'] = df['Power Output'] / df['Energy Input'] 
        
        glossary_columns = [
            'Magnetic Field Strength',
            'Plasma Instabilities',
            'Temperature',
            'Fuel Density',
            'Confinement Time',
            'Neutron Yield',
            'Power Output',
            'Energy Input',
            'Ignition',
            'Magnetic Field Configuration',
            'Overall Efficiency'
        ]

        # Keep only the columns that exist in both the dataframe and the glossary
        df = df[df.columns.intersection(glossary_columns)]
        self.df = df.apply(lambda col: pd.to_numeric(col, errors='coerce') if col.dtype != 'object' else col)

    def populate_bst(self):
        """Populates the Binary Search Tree with Neutron Yield as key and index as value."""
        for idx, row in self.df.dropna(subset=['Neutron Yield']).iterrows():
            self.yield_bst.insert(row['Neutron Yield'], idx)

    def view_dataset(self):
        print(f"{GREEN}Dateset after cleanup: {RESET}")
        print(self.df.head().to_string(max_cols=10)) 

    def view_stats(self, figureshowing=False):
        """Provides summary statistics and optional visualizations."""
        print(f"{GREEN}Dataset shape: {self.df.shape}{RESET}")
        print(f"Dataset columns: {self.df.columns.tolist()}")
        
        mag_config = self.df['Magnetic Field Configuration']
        print(f"{RED}Unique magnetic field configuration:{RESET}")
        print(mag_config.unique())

        if figureshowing:
            fig, axes = plt.subplots(1, 3, figsize=(14, 5))
            sns.histplot(self.df['Temperature'], kde=True, ax=axes[0], color='skyblue')
            axes[0].set_title('Distribution of Temperature')
            sns.histplot(self.df['Neutron Yield'], kde=True, ax=axes[1], color='salmon')
            axes[1].set_title('Distribution of Neutron Yield')
            sns.boxplot(x='Ignition', y='Temperature', data=self.df, ax=axes[2])
            axes[2].set_title('Temperature Distribution by Ignition')
            plt.tight_layout()
            plt.show()

    def config_design_matrix(self, feature_choice):
        """Configures the design matrix X based on user-selected features."""
        column_hash = {'1': 'Plasma Instabilities', '2': 'Magnetic Field Strength', '3': 'Fuel Density', '4': 'Temperature', '5': 'Confinement Time', 
                       '6': 'Energy Input', '7': 'Power Output', '8': 'Neutron Yield', '9': 'Ignition'}
        
        selected_cols = []
        for i in feature_choice:
            if i in column_hash:
                selected_cols.append(column_hash[i])
            else:
                print(f"{YELLOW}Warning: Feature index {i} is invalid and will be ignored.{RESET}")
        
        if not selected_cols:
            print(f"{RED}Error: No valid features selected.{RESET}")
            return

        self.X = self.df[selected_cols].to_numpy()
        self.y = self.df[['Overall Efficiency']].to_numpy()
        print(f"{BLUE}Design matrix X configured with shape {self.X.shape}{RESET}")
    
    def top_neutron_exp(self):
        print(self.df.nlargest(10, 'Neutron Yield').to_string(max_cols=10)) 
    
    def top_efficiency_exp(self):
        print(self.df.nlargest(10, 'Overall Efficiency').to_string(max_cols=10)) 

    def manual_search_efficiency(self, target):
        """Uses toolbox.bin_search to find an exact efficiency match."""
        # Get unique sorted efficiencies for binary search
        arr = np.sort(self.df['Overall Efficiency'].dropna().unique())
        idx = tools.bin_search(arr, target)
        if idx != -1:
            print(f"{GREEN}Exact match for efficiency {target} found in sorted array at index {idx}.{RESET}")
        else:
            print(f"{YELLOW}No exact match found for efficiency {target}.{RESET}")

    def search_neutron_yield_range(self, min_val, max_val):
        """Uses the Binary Search Tree to find all experiments within a Neutron Yield range."""
        indices = self.yield_bst.find_range(min_val, max_val)
        if indices:
            print(f"{GREEN}Found {len(indices)} experiments in range [{min_val}, {max_val}]:{RESET}")
            # Use the indices found in the BST to locate the full rows in the dataframe
            results_df = self.df.loc[indices]
            print(results_df.head(10).to_string(max_cols=10))
        else:
            print(f"{YELLOW}No experiments found with Neutron Yield in range [{min_val}, {max_val}].{RESET}")

    def filter_by_temperature(self, threshold):
        """Filters experiments where temperature exceeds a certain threshold."""
        filtered_df = self.df[self.df['Temperature'] > threshold]
        print(f"{BLUE}Found {len(filtered_df)} experiments with Temperature > {threshold} keV:{RESET}")
        print(filtered_df.head(10).to_string(max_cols=10))

    def manual_rank_efficiency(self):
        """Uses toolbox.merge_sort to rank the top efficiencies."""
        # Extract efficiencies to numpy array
        arr = self.df['Overall Efficiency'].dropna().to_numpy()
        
        print(f"{BLUE}Sorting data using manual Merge Sort (Descending)...{RESET}")
        tools.merge_sort(arr, 0, len(arr))
        
        print(f"{GREEN}Top 5 Efficiencies (Manual Sort):{RESET}")
        print(arr[:5])

def print_menu():
    print(f"{GREEN}\n--- Nuclear Fusion Data Manager --- {RESET}")
    print("1) View dataset") 
    print("2) View statistics (with figure)")
    print("3) View statistics (without figure)")
    print("4) Configure your own design matrix X")
    print("5) Top 10 experiments with highest neutron yields")
    print("6) Top 10 experiments with highest overall efficiency") 
    print("7) Search for Neutron Yield Range (BST Range Search)")
    print("8) Manual Ranking of Efficiencies (Merge Sort)")
    print("9) Filter experiments by Temperature threshold")
    print("0) Quit")

def print_submenu():
    print(f"{RED}\n--- Nuclear Fusion Feature Menu --- {RESET}")
    print("Enter the numbers corresponding to the features you want, separated by spaces:")
    print("1) Plasma Instabilities   2) Magnetic Field Strength  3) Fuel Density") 
    print("4) Temperature            5) Confinement Time         6) Energy Input")
    print("7) Power Output           8) Neutron Yield            9) Ignition")


def read_int(prompt):
    text = input(prompt).strip()
    try: 
        return int(text)
    except ValueError:
        return None

def main():
    data_file = 'fusion_experiment.csv'
    data = Execution(data_file)

    while True:
        print_menu()
        choice = input("Please enter your selection: ").strip()

        if choice == "1":
            data.view_dataset()
        elif choice == "2":
            data.view_stats(figureshowing=True)
        elif choice == "3":
            data.view_stats(figureshowing=False)
        elif choice == "4": 
            print_submenu()
            feature_choice = input("> ").split()
            data.config_design_matrix(feature_choice)
        elif choice == "5":
            data.top_neutron_exp()
        elif choice == "6":
            data.top_efficiency_exp()
        elif choice == "7":
            try:
                low = float(input("Enter minimum Neutron Yield: "))
                high = float(input("Enter maximum Neutron Yield: "))
                data.search_neutron_yield_range(low, high)
            except ValueError:
                print(f"{RED}Invalid input. Please enter numbers for the range.{RESET}")
        elif choice == "8":
            data.manual_rank_efficiency()
        elif choice == "9":
            threshold = input("Enter Temperature threshold (keV): ")
            try:
                data.filter_by_temperature(float(threshold))
            except ValueError:
                print(f"{RED}Invalid input. Please enter a number.{RESET}")
        elif choice == "0":
            break
        else: 
            print("Invalid Choice. Please choose again.")
    print("Thank you for visiting. Come back soon!")


if __name__ == "__main__":
    main()