from motion_detector import datetime, os, df, current_time
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool,ColumnDataSource
print('Generating graph')

df["Start_Motion"]=df["START"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_Motion"]=df["END"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds=ColumnDataSource(df)

p = figure(x_axis_type='datetime', plot_height=100,
           plot_width=500, title='Motion Graph')

p.sizing_mode = "scale_width"

p.title.text = "Motion Detected"
p.title.text_color = "Gray"
p.title.text_font = "arial"
p.title.text_font_style = "bold"

p.xaxis.minor_tick_line_color = None
p.yaxis.minor_tick_line_color = None


p.xaxis.axis_label = "Duration"

q = p.quad(left="START", right="END", bottom=0, top=1, color="blue",source=cds)

hover = HoverTool(tooltips=[("START", "@Start_Motion"), ("END", "@End_Motion")])
p.add_tools(hover)

filename = current_time.strftime('%Y-%m-%d-%H-%M-%S')
path1 = 'html_files'

if not os.path.exists(path1):
    os.makedirs(path1)

output_file(os.path.join(path1, str(filename + '.html')))

show(p)
