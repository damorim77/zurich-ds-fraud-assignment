import pandas as pd

def get_frequency_table(series: pd.Series) -> pd.DataFrame:
    # Absolute frequency (n)
    abs_freq = series.value_counts(dropna=False)
    
    # Relative frequency (%)
    rel_freq = series.value_counts(dropna=False, normalize=True) * 100
    
    # Combine into a DataFrame
    freq_table = pd.DataFrame({
        'n': abs_freq,
        '%': rel_freq
    })
    
    # Calculate totals
    total_n = freq_table['n'].sum()
    total_pct = freq_table['%'].sum()
    
    # Append the total row
    freq_table.loc['Total'] = [total_n, total_pct]
    
    return freq_table