from asn1_function_sheet import age_splitter, cohortCompare
import pandas as pd
import numpy as np
import pytest

def test_age_splitter_1():
    df = pd.DataFrame({
        'age': [25, 30, 35, 40, 45],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva']
    })
    df_below, df_above_equal = age_splitter(df, 'age', 40)
    assert df_below.shape[0] == 3
    assert df_above_equal.shape[0] == 2

def test_age_splitter_2():
    df = pd.DataFrame({
        'age': [18, 22, 27, 29, 31, 35],
        'name': ['A', 'B', 'C', 'D', 'E', 'F']
    })
    df_below, df_above_equal = age_splitter(df, 'age', 30)
    assert all(df_below['age'] < 30)
    assert all(df_above_equal['age'] >= 30)

def test_cohortCompare():
    df = pd.DataFrame({
        'age': [18, 22, 27, 29, 31, 35],
        'name': ['A', 'B', 'C', 'D', 'E', 'F'],
        'income': [100, 150, 75, 60, 130, 35]
    })
    expected = {
        'age': {
            'mean': df['age'].mean(),
            'median': df['age'].median(),
            'std': df['age'].std(),
            'min': df['age'].min(),
            'max': df['age'].max()
    },
        'income': {
            'mean': df['income'].mean(),
            'median': df['income'].median(),
            'std': df['income'].std(),
            'min': df['income'].min(),
            'max': df['income'].max()
    }}

    result = cohortCompare(df, ['age', 'income'], statistics=['mean', 'median', 'std', 'min', 'max'])

    for cohort in expected:
        for stat in expected[cohort]:
            assert result[cohort][stat] == expected[cohort][stat], f"{cohort} {stat} does not equal expected result" 

    
    
  