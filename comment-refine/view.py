from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType


def build(list, name):
    c = (
        WordCloud()
        .add("", list, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
        .set_global_opts(title_opts=opts.TitleOpts(title="WordCloud"))
        .render("{}.html".format(name))
    )
