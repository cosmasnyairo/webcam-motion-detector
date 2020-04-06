from motion_detector import datetime, os, df, current_time
from bokeh.plotting import figure, output_file, show

print('Generating graph')

p = figure(x_axis_type='datetime', plot_height=100,
           plot_width=500, title='Motion Graph')

p.sizing_mode = "scale_width"

p.title.text = "Motion Detected"
p.title.text_color = "Gray"
p.title.text_font = "arial"
p.title.text_font_style = "bold"

p.xaxis.minor_tick_line_color = None
p.yaxis.minor_tick_line_color = None


p.xaxis.axis_label="Duration"

q = p.quad(left=df["START"], right=df["END"], bottom=0, top=1, color="green")

filename = current_time.strftime('%Y-%m-%d-%H-%M-%S')
path1 = 'html_files'

if not os.path.exists(path1):
    os.makedirs(path1)

output_file(os.path.join(path1, str(filename + '.html')))

show(p)
