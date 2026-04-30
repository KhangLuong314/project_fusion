# Project Fusion - Nuclear Fusion Data Manager

## Project Overview
Project Fusion is a specialized data management and analysis tool developed for the CSCE 311 course at the University of Nebraska-Lincoln. It is designed to process, analyze, and visualize results from nuclear fusion experiments. The system provides a command-line interface (CLI) that allows researchers to explore experimental parameters such as magnetic field strength, plasma instabilities, temperature, and neutron yield.

### Key Technologies
- **Language:** Python 3
- **Data Manipulation:** `pandas`, `numpy`
- **Visualization:** `matplotlib`, `seaborn`
- **Data Structures:** Custom Binary Search Tree implementation

## Building and Running
### Prerequisites
Ensure you have Python 3 installed along with the following libraries:
```bash
pip install pandas matplotlib seaborn numpy
```

### Running the Application
To start the interactive CLI:
```bash
python main.py
```

## Project Structure
- `main.py`: The entry point and UI controller. Handles data cleaning, menu navigation, and visualization.
- `toolbox.py`: Contains algorithmic implementations including Merge Sort, Binary Search, and OLS Correlation Matrix calculations.
- `data_structure.py`: Defines the `Binary_Search_Tree` and `TreeNode` classes used for efficient data storage and retrieval.
- `fusion_experiment.csv`: The primary dataset containing experimental fusion data.
- `CSCE 311 Project_Spring26.pdf`: Project specification and requirements.

## Development Conventions
- **Modular Design:** Keep UI logic in `main.py` and algorithmic/data structure logic in their respective files.
- **Data Integrity:** `main.py` performs automated cleanup and normalization of the dataset upon initialization.
- **Naming Conventions:** Follows standard PEP 8 naming conventions for Python (though some student-specific naming like `Binary_Search_Tree` exists).
- **Visualization Style:** Uses `seaborn-v0_8-darkgrid` for consistent and readable plotting.

## Completed Features
- [x] Integration of `toolbox.py` methods into `main.py` logic.
- [x] Implementation of Design Matrix configuration with automatic "all features" default.
- [x] OLS Regression Coefficient calculation for feature correlation analysis.
- [x] BST-based Neutron Yield search and range lookup.

## TODOs / Future Work
- [ ] Complete the integration of `toolbox.py` methods directly into `data_structure.py`.
- [ ] Refactor `view_stats` to improve modularity as suggested by code comments.
- [ ] Enhance BST to handle duplicate keys using a linked list or array at each node.
