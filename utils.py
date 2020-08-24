import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import Span, Label

def make_plot(data):
    p = figure(sizing_mode="stretch_width", plot_width=400, plot_height=400, 
               title="Prices nearing check-in day")
    p.grid.grid_line_alpha=1
    p.xaxis.axis_label = "Number of days from today's date"
    p.yaxis.axis_label = 'Price/night in USD'

    p.line(data.day, data.price, color='#A6CEE3', line_width=3)
    vline = Span(location=data.day[0], dimension='height', line_color='#f46d43', line_width=3)
    # my_label = Label(x=0, y=200, , text='Test label')
    p.renderers.extend([vline])
    # if ticker:
    #     p.legend.location = "top_left"
    return p