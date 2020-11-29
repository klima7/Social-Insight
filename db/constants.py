from flask_babel import lazy_gettext as _l


class GraphName:
    names = {}

    def __init__(self, nr, name):
        self.nr = nr
        self.name = name
        GraphName.names[nr] = name


class GraphNames:
    EXAMPLE_BAR_CHART = GraphName(1, _l('bar chart'))
    EXAMPLE_PIE_CHART = GraphName(2, _l('pie chart'))
    EXAMPLE_LINE_CHART = GraphName(3, _l('line chart'))
    EXAMPLE_RADAR_CHART = GraphName(4, _l('radar chart'))
