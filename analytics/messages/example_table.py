from .. import graph
from flask_babel import gettext as _l
import pandas as pd


@graph('messages', _l('Example table'))
def example_table(data):
    s1 = pd.Series([1, 2, 3, 4, 5])
    s2 = pd.Series(['Ala', 'ma', 'kota', 'foo', 'bar'])
    f1 = pd.DataFrame({_l('header 1'): s1, _l('header 2'): s2, _l('header 3'): s1})
    return f1
