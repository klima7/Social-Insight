import pandas as pd


def shorten_strings(names_series, width=25):
    series = names_series
    if isinstance(names_series, pd.Index):
        series = names_series.to_series()
    series.loc[series.str.len() > width] = series.loc[series.str.len() > width].str.slice_replace(width-3, repl='...')
    return series
