import panel as pn
import numpy as np
from bs4 import BeautifulSoup
from IPython.display import SVG

import plotly.subplots as sp
import plotly.graph_objects as go

from data import Dashdata

class Dashboard(pn.Row):
    def __init__(self):
        # Data container
        self.ddata = Dashdata()
        
        # Create the SVG pane
        self.svg_image = pn.pane.SVG(
            SVG(self.ddata.brainSvgImage), 
            width=600, 
            height=600)
        
        # Create the slider
        intRangeSliderWidget = pn.widgets.IntSlider(
            name='Integer Range Slider',
            start=0, end=10000, value=0, step=1)
        
        # Create the Plotly pane
        plot_pane = pn.pane.Plotly()
        
        # Bind the slider value to the update_plot function
        intRangeSliderWidget.param.watch(update_plot, 'value')
        
        selectWidget = pn.widgets.Select(
            name='Selecione a sujeito',
            groups=ddata.subjectsNamesAndCodes
        )
        
        selectWidget.param.watch(self._selectData, 'value')
        
        switchLabelWidget = pn.widgets.StaticText(name='Visão geral', value='')
        switchWidget = pn.widgets.Switch(name='Visão geral')
        
        self = pn.Row(
            svg_image, 
            pn.Column(
                pn.Row(intRangeSliderWidget, selectWidget),
                plot_pane,
                pn.Row(switchLabelWidget, switchWidget)
                ), 
            sizing_mode='stretch_width')

    def _selectData(event):
        selected_option = event.obj.value
        return selected_option
        
    def _changeElementHeight(soup, element_id, new_height):
        element = soup.find(id=element_id)
        if element is not None:
            element['height'] = str(new_height/1000)

    def _paintSensor(soup, sensorsTags):
        element = soup.find(id=sensorsTags)
        if element is not None:
            color = ddata.sensorToColorRelationship[sensorsTags]
            element["style"] = f'fill:{color}'
            
    def updateBrainFigure(event, svg_image):
        soup = BeautifulSoup(svg_image.object.data, "xml")
        
        paintSensor(soup, "FP1")
        paintSensor(soup, "FP2")
        
        paintSensor(soup, "F3")
        paintSensor(soup, "F4")
        paintSensor(soup, "F7")
        paintSensor(soup, "F8")
        paintSensor(soup, "FZ")
        
        paintSensor(soup, "A1")
        paintSensor(soup, "A2")
        paintSensor(soup, "T3") 
        paintSensor(soup, "T4") 
        paintSensor(soup, "C3") 
        paintSensor(soup, "C4") 
        paintSensor(soup, "CZ")
        
        paintSensor(soup, "T5")
        paintSensor(soup, "T6")
        paintSensor(soup, "P3")
        paintSensor(soup, "P4")
        paintSensor(soup, "PZ")
        
        paintSensor(soup, "O1")
        paintSensor(soup, "O2")
        
        changeElementHeight(soup, "FP1bar", event)
        changeElementHeight(soup, "FP2bar", event)

        changeElementHeight(soup, "F3bar", event)
        changeElementHeight(soup, "F4bar", event)
        changeElementHeight(soup, "F7bar", event)
        changeElementHeight(soup, "F8bar", event)
        changeElementHeight(soup, "FZbar", event)
        
        changeElementHeight(soup, "A1bar", event)
        changeElementHeight(soup, "A2bar", event)
        changeElementHeight(soup, "T3bar", event) 
        changeElementHeight(soup, "T4bar", event) 
        changeElementHeight(soup, "C3bar", event) 
        changeElementHeight(soup, "C4bar", event) 
        changeElementHeight(soup, "CZbar", event)
        
        changeElementHeight(soup, "T5bar", event)
        changeElementHeight(soup, "T6bar", event)
        changeElementHeight(soup, "P3bar", event)
        changeElementHeight(soup, "P4bar", event)
        changeElementHeight(soup, "PZbar", event)
        
        changeElementHeight(soup, "O1bar", event)
        changeElementHeight(soup, "O2bar", event)
        
        # Must be the last call!
        svg_image.object = SVG(str(soup))
        
    def update_plot(event):
        lines = []
        
        for sensor in ddata.sensorToColorRelationship:
            try:
                lines.append(ddata.dataframe.iloc[[event.new]][sensor].values[0])
            except Exception:
                pass

        fig = sp.make_subplots(rows=len(lines), cols=1)

        for i, line in enumerate(lines):
            fig.add_trace(go.Scatter(y=line, mode='lines'), row=i+1, col=1)

        fig.update_layout(height=600, width=800, title='Line Plots')
        plot_pane.object = fig

        # Change the "fill" attribute in the in-memory SVG representation
        updateBrainFigure(event.new, svg_image)
        
        return fig


ddata = Dashdata()

# Create the SVG pane
svg_image = pn.pane.SVG(SVG(ddata.brainSvgImage), width=600, height=600)

def changeElementHeight(soup, element_id, new_height):
    element = soup.find(id=element_id)
    if element is not None:
        element['height'] = str(new_height/1000)

def paintSensor(soup, sensorsTags):
    element = soup.find(id=sensorsTags)
    if element is not None:
        color = ddata.sensorToColorRelationship[sensorsTags]
        element["style"] = f'fill:{color}'

def updateBrainFigure(event, svg_image):
    soup = BeautifulSoup(svg_image.object.data, "xml")
    
    paintSensor(soup, "FP1")
    paintSensor(soup, "FP2")
    
    paintSensor(soup, "F3")
    paintSensor(soup, "F4")
    paintSensor(soup, "F7")
    paintSensor(soup, "F8")
    paintSensor(soup, "FZ")
    
    paintSensor(soup, "A1")
    paintSensor(soup, "A2")
    paintSensor(soup, "T3") 
    paintSensor(soup, "T4") 
    paintSensor(soup, "C3") 
    paintSensor(soup, "C4") 
    paintSensor(soup, "CZ")
    
    paintSensor(soup, "T5")
    paintSensor(soup, "T6")
    paintSensor(soup, "P3")
    paintSensor(soup, "P4")
    paintSensor(soup, "PZ")
    
    paintSensor(soup, "O1")
    paintSensor(soup, "O2")
    
    changeElementHeight(soup, "FP1bar", event)
    changeElementHeight(soup, "FP2bar", event)

    changeElementHeight(soup, "F3bar", event)
    changeElementHeight(soup, "F4bar", event)
    changeElementHeight(soup, "F7bar", event)
    changeElementHeight(soup, "F8bar", event)
    changeElementHeight(soup, "FZbar", event)
    
    changeElementHeight(soup, "A1bar", event)
    changeElementHeight(soup, "A2bar", event)
    changeElementHeight(soup, "T3bar", event) 
    changeElementHeight(soup, "T4bar", event) 
    changeElementHeight(soup, "C3bar", event) 
    changeElementHeight(soup, "C4bar", event) 
    changeElementHeight(soup, "CZbar", event)
    
    changeElementHeight(soup, "T5bar", event)
    changeElementHeight(soup, "T6bar", event)
    changeElementHeight(soup, "P3bar", event)
    changeElementHeight(soup, "P4bar", event)
    changeElementHeight(soup, "PZbar", event)
    
    changeElementHeight(soup, "O1bar", event)
    changeElementHeight(soup, "O2bar", event)
    
    # Must be the last call!
    svg_image.object = SVG(str(soup))

def update_plot(event):
    lines = []
    
    for sensor in ddata.sensorToColorRelationship:
        try:
            lines.append(ddata.dataframe.iloc[[event.new]][sensor].values[0])
        except Exception:
            pass

    fig = sp.make_subplots(rows=len(lines), cols=1)

    for i, line in enumerate(lines):
        fig.add_trace(go.Scatter(y=line, mode='lines'), row=i+1, col=1)

    fig.update_layout(height=600, width=800, title='Line Plots')
    plot_pane.object = fig

    # Change the "fill" attribute in the in-memory SVG representation
    updateBrainFigure(event.new, svg_image)
    
    return fig

intRangeSliderWidget = pn.widgets.IntSlider(
    name='Integer Range Slider',
    start=0, end=10000, value=0, step=1)


# Create the Plotly pane
plot_pane = pn.pane.Plotly()

# Bind the slider value to the update_plot function
intRangeSliderWidget.param.watch(update_plot, 'value')

selectWidget = pn.widgets.Select(
    name='Selecione a sujeito',
    groups=ddata.subjectsNamesAndCodes
)

def selectData(event):
    selected_option = event.obj.value
    return selected_option

selectWidget.param.watch(selectData, 'value')

switchLabelWidget = pn.widgets.StaticText(name='Visão geral', value='')
switchWidget = pn.widgets.Switch(name='Visão geral')

dashboard = pn.Row(
    svg_image, 
    pn.Column(
        pn.Row(intRangeSliderWidget, selectWidget),
        plot_pane,
        pn.Row(switchLabelWidget, switchWidget)
        ), 
    sizing_mode='stretch_width')

# Launch the dashboard with hot reloading enabled
dashboard.servable()