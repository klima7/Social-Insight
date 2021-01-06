from .. import graph, style
from flask_babel import gettext as _l
import pygal


@graph(_l('Browser'))
def device_usage(data):
    acc_act = data['account_activity']
    browser = acc_act.browser.value_counts()
    browser = browser / browser.sum() * 100
    browser = browser.round(2)

    pie_chart = pygal.Pie(style=style, inner_radius=.4)
    for os, count in zip(browser.index, browser):
        pie_chart.add(os, count)

    return pie_chart

    return chart
