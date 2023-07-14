import panel as pn
import numpy as np
import plotly.subplots as sp
from bs4 import BeautifulSoup
from IPython.display import SVG
import plotly.graph_objects as go

from data import Dashdata

class Dashboard():
    def __init__(self):
        # Data container
        self.ddata = Dashdata()
        
        # Create the SVG pane widget
        self.svg_image = pn.pane.SVG(
            SVG(self.ddata.brainSvgImage), 
            width=600, 
            height=600)
        
        ########################
        ### Widgets creation ###
        ########################
        
        # Create the Plotly pane widget
        self.plot_pane = pn.pane.Plotly()
        
        # Create the slider widget
        self.intRangeSliderWidget = pn.widgets.IntSlider(name='Integer Range Slider', start=0, end=10, value=0, step=1)
        
        # Create the selection widget
        self.selectWidget = pn.widgets.Select(name='Selecione a sujeito', groups=self.ddata.subjectsNamesAndCodes)

        # Create a label for the switch widget
        self.switchLabelWidget = pn.widgets.StaticText(name='Visão geral', value='')
        
        # Create the switch widget
        self.switchWidget = pn.widgets.Switch(name='Visão geral')

        ############################
        ### Event handle binding ###
        ############################

        # Bind the widgets to its respective event handler
        self.intRangeSliderWidget.param.watch(self._update_plot, 'value')
        self.selectWidget.param.watch(self._selectData, 'value')
        
        #######################
        ### Layout assembly ###
        #######################
        
        self.layout = pn.Row(
            self.svg_image, 
            pn.Column(
                pn.Row(self.intRangeSliderWidget, self.selectWidget),
                self.plot_pane,
                pn.Row(self.switchLabelWidget, self.switchWidget)
                ), 
            sizing_mode='stretch_width')

    def _selectData(event):
        selected_option = event.obj.value
        return selected_option
        
    def _changeElementHeight(self, soup, element_id, new_height):
        element = soup.find(id=element_id)
        if element is not None:
            element['height'] = str(new_height/1000)

    def _paintSensor(self, soup, sensorsTags):
        element = soup.find(id=sensorsTags)
        if element is not None:
            color = self.ddata.sensorToColorRelationship[sensorsTags]
            element["style"] = f'fill:{color}'
            
    def calculate_total_energy(self, values):
        squared_values = np.square(values)       # Square each value
        sum_of_squares = np.sum(squared_values)  # Sum up the squared values
        total_energy = np.sqrt(sum_of_squares)   # Take the square root
    
        return total_energy
            
    def updateBrainFigure(self, event, lines):
        
        # Loads the SVG
        soup = BeautifulSoup(self.ddata.brainSvgImage, "xml")
        
        # Iterates over all available sensors
        for i, line in enumerate(lines):
            
            # Change sensor color
            self._paintSensor(soup, line[0])
            
            # Change sensor energy height
            self._changeElementHeight(soup, line[0] +"bar", 10 * self.calculate_total_energy(line[1]))
            
        # Must be the last call!
        self.svg_image.object = SVG(str(soup))
        
    def _update_plot(self, event):
        lines = []
        
        # Extract data to be plot
        for sensor in self.ddata.sensorToColorRelationship:
            try:
                # Sensor name + signal for example: (F3, 12121212112)
                lines.append((sensor, self.ddata.dataframe.iloc[[event.new]][sensor].values[0]))
            except Exception:
                pass

        # Create the nned subplots
        fig = sp.make_subplots(rows=len(lines), cols=1)

        # Plots data
        for i, line in enumerate(lines):
            
            # Retrieves the color of the sensor
            color = self.ddata.sensorToColorRelationship[line[0]]
            
            fig.add_trace(
                # Plots the line with the corresponding color and name of the sensor 
                go.Scatter(y=line[1], mode='lines', name=line[0], line=dict(color=color)),
            row=i+1, col=1)

        # Refresh the plots UI
        fig.update_layout(height=600, width=800, title='Line Plots')
        self.plot_pane.object = fig

        # Refresh the Svg UI
        self.updateBrainFigure(event.new, lines)
        
        return fig

dashboard = Dashboard()
dashboard.layout.servable()