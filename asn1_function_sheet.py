
import pandas as pd
import numpy as np
import math


def age_splitter(df, col_name, age_threshold):
    """
    Splits the dataframe into two dataframes based on an age threshold.

    Parameters:
    df (pd.DataFrame): The input dataframe.
    col_name (str): The name of the column containing age values.
    age_threshold (int): The age threshold for splitting.

    Returns:
    tuple: A tuple containing two dataframes:
        - df_below: DataFrame with rows where age is below the threshold.
        - df_above_equal: DataFrame with rows where age is above or equal to the threshold.
    """
    df_below = df[df[col_name] < age_threshold]
    df_above_equal = df[df[col_name] >= age_threshold]
    return df_below, df_above_equal                      

    
def effectSizer(df, num_col, cat_col):
    """
    Calculates the effect sizes of binary categorical classes on a numerical value.

    Parameters:
    df (pd.DataFrame): The input dataframe.
    num_col (str): The name of the numerical column.
    cat_col (str): The name of the binary categorical column.

    Returns:
    float: Cohen's d effect size between the two groups defined by the categorical column.
    Raises:
    ValueError: If the categorical column does not have exactly two unique values.
    """
    effect_sizes = {}                                                           # Create dictionary for categorical classes and their corresponding effect sizes
    if df[cat_col].nunique() == 2:                                              # If the cat_column has 2 unique values
        mean1, mean2 = df.groupby(cat_col)[num_col].mean().tolist()             # Calc mean for each group in cat_col and unpack
        var1, var2 = df.groupby(cat_col)[num_col].var().tolist()                # Calc variance
        length1, length2 = df.groupby(cat_col)[num_col].count().tolist()        # Find length of each group
        pooled_var = (length1 * var1 + length2 * var2) / (length1 + length2)    # Calc pooled variance
        eff_sz_d = (mean1 - mean2) / math.sqrt(pooled_var)                      # Calc Cohen's d 
        effect_sizes[cat_col] = eff_sz_d
        return effect_sizes
    else:
        raise ValueError("Categorical column must have exactly two unique values.")


def cohenEffectSize(group1, group2):                                # I don't know what this is for...
    # You need to implement this helper function
    # This should not be too hard...
    return group1, group2


def cohortCompare(df, cohorts, statistics=['mean', 'median', 'std', 'min', 'max']):
    """
    This function takes a dataframe and a list of cohort column names, and returns a dictionary
    where each key is a cohort name and each value is an object containing the specified statistics
    """
    results = {}                                                            # Create dictionary for cohorts and their corresponding statistics
    for column in cohorts:                                                  # Go through each column listed as 'cohorts'
        if pd.api.types.is_numeric_dtype(df[column]):                       # Select numerical columns
            metric = CohortMetric(cohort_name=column)                       # Create CohortMetric object
            setters = {                                                     # Create dictionary to map stat names to setter methods
                "mean": metric.setMean,
                "median": metric.setMedian,
                "std": metric.setStd,
                "min": metric.setMin,
                "max": metric.setMax
            }
            stats_values = {}
            for stat in statistics:                                         # Go through each stat listed as 'statistics'
                stats_values[stat] = df[column].agg(stat)                   # Apply stat calcultaion to column, store results in dictionary with the stat name as the key
                setters[stat](stats_values[stat])                           # I don't get this code... Somehow it updates the internal dictionary for the CohortMetric object aka metric
            results[column] = stats_values                                  # Create a key in results dictionary ('column'), assign the stats_values dictionary as the values
        else:
            results[column] = df[column].value_counts().to_dict()           # Count values in categorical/object columns and store in dictionary
    return results                                                          # Return 'results' dictionary


class CohortMetric():
    # don't change this
    def __init__(self, cohort_name):
        self.cohort_name = cohort_name
        self.statistics = {
            "mean": None,
            "median": None,
            "std": None,
            "min": None,
            "max": None
        }
    def setMean(self, new_mean):
        self.statistics["mean"] = new_mean
    def setMedian(self, new_median):
        self.statistics["median"] = new_median
    def setStd(self, new_std):
        self.statistics["std"] = new_std
    def setMin(self, new_min):
        self.statistics["min"] = new_min
    def setMax(self, new_max):
        self.statistics["max"] = new_max

    def compare_to(self, other):
        for stat in self.statistics:
            if not self.statistics[stat].equals(other.statistics[stat]):
                return False
        return True
    def __str__(self):
        output_string = f"\nCohort: {self.cohort_name}\n"
        for stat, value in self.statistics.items():
            output_string += f"\t{stat}:\n{value}\n"
            output_string += "\n"
        return output_string
