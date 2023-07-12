import panel as pn
import numpy as np
from bs4 import BeautifulSoup
from IPython.display import SVG

import plotly.subplots as sp
import plotly.graph_objects as go
tag = ["F3", "F4", "F7", "F8", "FZ"]
col = [
    "#FF3C00",  # Vivid Orange
    "#FF9700",  # Bright Orange
    "#FFD300",  # Sunflower Yellow
    "#FF4D6E",  # Coral Pink
    "#FF66B2",  # Bubblegum Pink
    "#FF8AC3",  # Light Pink
    "#FF00D8",  # Magenta
    "#6A00FF",  # Vivid Purple
    "#A050FF",  # Lavender Purple
    "#FFA6FF",  # Cotton Candy
    "#00C4FF",  # Sky Blue
    "#00E6FF",  # Aqua Blue
    "#00FFD4",  # Mint Green
    "#1AFFB5",  # Turquoise
    "#00FF89",  # Neon Green
    "#00FF00",  # Lime Green
    "#FFFF33",  # Bright Yellow
    "#F9FF66",  # Lemon Yellow
    "#FF9F00",  # Amber
    "#FF7733",  # Coral Orange
    "#FFAF40"   # Peach
]

options = {
    'Sujeito01': '1',
    'Sujeito02': '2',
    'Sujeito03': '3'
}

colors = dict(zip(tag, col))

def createRnd(seed, num_lines):
    np.random.seed(0)
    lines = []
    for _ in range(num_lines):
        x = np.random.rand(seed)
        y = np.random.rand(seed)
        lines.append((x, y))
    return lines

# Create the line plot using Plotly graph objects
num_lines = 4  # Number of lines to plot
lines = createRnd(100, num_lines)

# Create the SVG pane
svg_content = open("brain.svg").read()
svg_image = pn.pane.SVG(SVG(svg_content), width=600, height=600)

def changeElementHeight(soup, element_id, new_height):
    element = soup.find(id=element_id)
    if element is not None:
        element['height'] = str(new_height/1000)

def paintSensor(soup, tag):
    element = soup.find(id=tag)
    if element is not None:
        color = colors[tag]
        element["style"] = f'fill:{color}'

def update_svg_fill(event, svg_image):
    # Change the "fill" attribute in the in-memory SVG representation
    soup = BeautifulSoup(svg_image.object.data, "xml")
    
    paintSensor(soup, "F3")
    paintSensor(soup, "F4")
    paintSensor(soup, "F7")
    paintSensor(soup, "F8")
    paintSensor(soup, "FZ")
    
    changeElementHeight(soup, "F8bar", event)
    changeElementHeight(soup, "F7bar", event)
    
    # Must be the last call!
    svg_image.object = SVG(str(soup))

def update_plot(event):
    num_lines = 3  # Number of lines to plot
    lines = createRnd(event.new, num_lines)

    fig = sp.make_subplots(rows=num_lines, cols=1, subplot_titles=[f'Line {i+1}' for i in range(num_lines)])

    for i, line in enumerate(lines):
        x, y = line
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines'), row=i+1, col=1)

    fig.update_layout(height=600, width=800, title='Line Plots')
    plot_pane.object = fig

    # Change the "fill" attribute in the in-memory SVG representation
    update_svg_fill(event.new, svg_image)

fig = sp.make_subplots(rows=num_lines, cols=1, subplot_titles=[f'Line {i+1}' for i in range(num_lines)])

for i, line in enumerate(lines):
    x, y = line
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines'), row=i+1, col=1)

fig.update_layout(height=600, width=800, title='Line Plots')

# Create the Plotly pane
plot_pane = pn.pane.Plotly(fig)

int_range_slider = pn.widgets.IntSlider(
    name='Integer Range Slider',
    start=0, end=10000, value=0, step=1)

# Bind the slider value to the update_plot function
int_range_slider.param.watch(update_plot, 'value')

select_widget = pn.widgets.Select(
    name='Selecione a sujeito',
    groups={'Imaginado': ['Sujeito01', 'Sujeito02'], 'Falado': ['Sujeito03']}
)

def callback(event):
    selected_option = event.obj.value
    print(options.get(selected_option, 'Invalid option'))
    return options.get(selected_option, 'Invalid option')

select_widget.param.watch(callback, 'value')

switchLabel = pn.widgets.StaticText(name='Visão geral', value='')
switch = pn.widgets.Switch(name='Visão geral')


# Bind the select value to the update_plot function
#select.param.watch(update_plot, 'value')

dashboard = pn.Row(
    svg_image, 
    pn.Column(
        pn.Row(int_range_slider, select_widget),
        plot_pane,
        pn.Row(switchLabel, switch)
        ), 
    sizing_mode='stretch_width')

# Launch the dashboard with hot reloading enabled
dashboard.servable()
