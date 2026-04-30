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
            sns.histplot(x=self.df['Temperature'], kde=True, ax=axes[0], color='skyblue')
            axes[0].set_title('Distribution of Temperature')
            sns.histplot(x=self.df['Neutron Yield'], kde=True, ax=axes[1], color='salmon')
            axes[1].set_title('Distribution of Neutron Yield')
            sns.boxplot(x='Ignition', y='Temperature', data=self.df, ax=axes[2])
            axes[2].set_title('Temperature Distribution by Ignition')
            plt.tight_layout()
            plt.show()

    def view_specific_stats(self, mag_config, stat_type, feature):
        """Provides specific statistics based on user input with robustness."""
        # Case-insensitive matching for magnetic field configuration
        available_configs = self.df['Magnetic Field Configuration'].unique()
        config_match = next((c for c in available_configs if str(c).lower() == mag_config.lower()), None)

        if config_match is None:
            print(f"{YELLOW}No data found for magnetic field configuration: {mag_config}{RESET}")
            print(f"Available configurations: {available_configs}")
            return

        filtered_df = self.df[self.df['Magnetic Field Configuration'] == config_match]

        # Validate feature exists and is numeric
        if feature not in self.df.columns:
            print(f"{RED}Error: Feature '{feature}' does not exist in the dataset.{RESET}")
            return

        if not pd.api.types.is_numeric_dtype(self.df[feature]):
            print(f"{RED}Error: Feature '{feature}' is not numeric and cannot be used for statistics.{RESET}")
            return

        stat_type = stat_type.lower()
        try:
            if stat_type == 'mean':
                result = filtered_df[feature].mean()
                print(f"{GREEN}Mean {feature} for {config_match}: {result:.2f}{RESET}")
            elif stat_type == 'median':
                result = filtered_df[feature].median()
                print(f"{GREEN}Median {feature} for {config_match}: {result:.2f}{RESET}")
            elif stat_type == 'std':
                result = filtered_df[feature].std()
                print(f"{GREEN}Standard Deviation of {feature} for {config_match}: {result:.2f}{RESET}")
            else:
                print(f"{YELLOW}Invalid statistic type: {stat_type}. Choose from mean, median, or std.{RESET}")
        except Exception as e:
            print(f"{RED}An error occurred during calculation: {e}{RESET}")

    def config_design_matrix(self, feature_choice):
        """Configures the design matrix X based on user-selected features. Defaults to all features if none selected."""
        column_hash = {'1': 'Plasma Instabilities', '2': 'Magnetic Field Strength', '3': 'Fuel Density', '4': 'Temperature', '5': 'Confinement Time', 
                       '6': 'Energy Input', '7': 'Power Output', '8': 'Neutron Yield', '9': 'Ignition'}
        
        # Default to all features if no choice provided
        if not feature_choice:
            print(f"{BLUE}No features selected. Defaulting to all features.{RESET}")
            feature_choice = ['10']

        if '10' in feature_choice:
            selected_cols = list(column_hash.values())
        else:
            selected_cols = []
            for i in feature_choice:
                if i in column_hash:
                    selected_cols.append(column_hash[i])
                else:
                    print(f"{YELLOW}Warning: Feature index {i} is invalid and will be ignored.{RESET}")
        
        if not selected_cols:
            print(f"{RED}Error: No valid features selected.{RESET}")
            return

        # Data Cleaning: Drop rows with NaNs in selected columns or target to ensure valid matrix operations
        analysis_df = self.df[selected_cols + ['Overall Efficiency']].dropna()
        if analysis_df.empty:
            print(f"{RED}Error: Not enough data points without NaNs for the selected features.{RESET}")
            return

        self.X = analysis_df[selected_cols].to_numpy()
        self.y = analysis_df[['Overall Efficiency']].to_numpy()
        print(f"{BLUE}Design matrix X configured with shape {self.X.shape}{RESET}")

        try:
            corelation = tools.correlation_matrix(self.X, self.y)
            features_cor = {col: corelation[idx][0] if isinstance(corelation[idx], (np.ndarray, list)) else corelation[idx] 
                           for idx, col in enumerate(selected_cols)}
            print(f"{GREEN}Regression coefficients between selected features and Overall Efficiency:{RESET}")
            print(pd.DataFrame.from_dict(features_cor, orient='index', columns=['Coefficient']))
        except np.linalg.LinAlgError:
            print(f"{RED}Error: Linear algebra operation failed. The design matrix might be singular or non-invertible.{RESET}")
    
    def search_neutron_yield(self, min_val, max_val):
        """Uses the Binary Search Tree to find all experiments within a Neutron Yield range."""
        indices = self.yield_bst.find_range(min_val, max_val)
        if indices:
            print(f"{GREEN}Found {len(indices)} experiments in range [{min_val}, {max_val}]:{RESET}")
            # Use the indices found in the BST to locate the full rows in the dataframe
            results_df = self.df.loc[indices]
            print(results_df.head(15).to_string(max_cols=10))
            if len(indices) > 15:
                print(f"{BLUE}... and {len(indices) - 15} more results.{RESET}")
        else:
            print(f"{YELLOW}No experiments found with Neutron Yield in range [{min_val}, {max_val}].{RESET}")

    def top_neutron_exp(self):
        print(self.df.nlargest(10, 'Neutron Yield').to_string(max_cols=10)) 
    
    def top_efficiency_exp(self):
        print(self.df.nlargest(10, 'Overall Efficiency').to_string(max_cols=10)) 

    def manual_search_id(self, target_id):
        """Uses binary search to find an experiment by ID."""
        sorted_ids = np.sort(self.df.index.to_numpy())
        idx = tools.bin_search(sorted_ids, target_id)
        if idx != -1:
            row = self.df.loc[target_id]
            print(f"{GREEN}Experiment with ID {target_id}:{RESET}")
            print(row.to_string())
        else:
            print(f"{YELLOW}No experiment found with ID {target_id}.{RESET}")

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
    print("4) Manual Search for Experiment ID (Binary Search)")
    print("5) View specific statistics by magnetic field configuration")
    print("6) Configure your own design matrix X")
    print("7) Top 10 experiments with highest neutron yields")
    print("8) Top 10 experiments with highest overall efficiency") 
    print("9) Search for Neutron Yield range (BST Search)")
    print("10) Manual Ranking of Efficiencies (Merge Sort)")
    print("11) Filter experiments by Temperature threshold")
    print("0) Quit")

def print_submenu():
    print(f"{RED}\n--- Nuclear Fusion Feature Menu --- {RESET}")
    print("Enter the numbers corresponding to the features you want, separated by spaces:")
    print("1) Plasma Instabilities   2) Magnetic Field Strength  3) Fuel Density") 
    print("4) Temperature            5) Confinement Time         6) Energy Input")
    print("7) Power Output           8) Neutron Yield            9) Ignition")
    print("10) Include all features")


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
            try:
                target_id = int(input("Enter experiment ID to search for: "))
                data.manual_search_id(target_id)
            except ValueError:
                print(f"{RED}Invalid input. Please enter an integer ID.{RESET}")
        elif choice == "5":
            mag_config = input("Enter magnetic field configuration to filter by: ")
            stat_type = input("Enter statistic type (mean, median, std): ")
            print(f"{YELLOW}Available features: Temperature, Neutron Yield, Overall Efficiency{RESET}")
            feature = input("Enter feature to analyze (e.g., Temperature, Neutron Yield): ")
            data.view_specific_stats(mag_config, stat_type, feature)
        elif choice == "6": 
            print_submenu()
            feature_choice = input("> ").split()
            data.config_design_matrix(feature_choice)
        elif choice == "7": 
            data.top_neutron_exp()
        elif choice == "8":
            data.top_efficiency_exp()
        elif choice == "9":
            try:
                min_yield = float(input("Enter minimum Neutron Yield: "))
                max_yield = float(input("Enter maximum Neutron Yield: "))
                data.search_neutron_yield(min_yield, max_yield)
            except ValueError:
                print(f"{RED}Invalid input. Please enter numbers.{RESET}")
        elif choice == "10":
            data.manual_rank_efficiency()
        elif choice == "11":
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