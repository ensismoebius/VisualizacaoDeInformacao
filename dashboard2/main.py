import panel as pn
import numpy as np
import plotly.subplots as sp
from bs4 import BeautifulSoup
from IPython.display import SVG
import plotly.graph_objects as go

from data import Dashdata


class Dashboard():
    def __init__(self):

        #######################
        ### Core properties ###
        #######################

        # Data container
        self.ddata = Dashdata()

        self.selectedModality = -1

        self.selectedArtifact = -1

        self.selectedEstimuli = -1

        self.generalView = False

        self.subjects = self.ddata.dataframe

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

        # Create the subject selection widget
        self.selectSubjectWidget = pn.widgets.Select(
            name='Selecione o sujeito')

        # Create the modality selection widget
        self.selectModalityWidget = pn.widgets.Select(
            name='Selecione a modalidade')
        self.selectModalityWidget.options = self.ddata.modalities

        # Create the artfact selection widget
        self.selectArtefactWidget = pn.widgets.Select(
            name='Selecione o artefato')
        self.selectArtefactWidget.options = self.ddata.artfacts

        # Create the estimul selection widget
        self.selectStimuliWidget = pn.widgets.Select(
            name='Selecione o estímulo')
        self.selectStimuliWidget.options = self.ddata.estimulos

        # Create a label for the switch widget
        self.switchLabelWidget = pn.widgets.StaticText(
            name='Visão geral', value='')

        # Create the switch widget
        self.switchWidget = pn.widgets.Switch(name='Visão geral')

        ############################
        ### Event handle binding ###
        ############################

        self.selectModalityWidget.param.watch(self._modalitySelected, 'value')
        self.selectStimuliWidget.param.watch(self._estimuliSelected, 'value')
        self.selectArtefactWidget.param.watch(self._artifactSelected, 'value')
        self.selectSubjectWidget.param.watch(self._update_plot, 'value')
        self.switchWidget.param.watch(self._generalViewChange, 'value')

        #######################
        ### Layout assembly ###
        #######################

        self.layout = pn.Row(
            self.svg_image,
            pn.Column(
                pn.Row(self.selectModalityWidget, self.selectStimuliWidget),
                pn.Row(self.selectArtefactWidget, self.selectSubjectWidget),
                self.plot_pane,
                pn.Row(self.switchLabelWidget, self.switchWidget)
            ),
            sizing_mode='stretch_width')

    ############################
    ### Callbacks definition ###
    ############################

    def _generalViewChange(self, event):
        self.generalView = event.new
        self._update_plot(event, self.selectSubjectWidget.value)

    def _modalitySelected(self, event):
        self.selectedModality = event.new
        if (self.selectedModality != -1) and (self.selectedEstimuli != -1):
            self.subjects = self.filterSignals(
                self.selectedModality, self.selectedEstimuli, self.selectedArtifact)
            self.selectSubjectWidget.options = self.subjects.index.tolist()

    def _estimuliSelected(self, event):
        self.selectedEstimuli = event.new
        if (self.selectedModality != -1) and (self.selectedEstimuli != -1):
            self.subjects = self.filterSignals(
                self.selectedModality, self.selectedEstimuli, self.selectedArtifact)
            self.selectSubjectWidget.options = self.subjects.index.tolist()

    def _artifactSelected(self, event):
        self.selectedArtifact = event.new
        if (self.selectedModality != -1) and (self.selectedArtifact != -1):
            self.subjects = self.filterSignals(
                self.selectedModality, self.selectedEstimuli, self.selectedArtifact)
            self.selectSubjectWidget.options = self.subjects.index.tolist()

    def _update_plot(self, event, subjectNumber = -1):
        lines = []
        if subjectNumber == -1:
            subjectNumber = event.new

        # Extract data to be plot
        for sensor in self.ddata.sensorToColorRelationship:
            try:
                # Sensor name + signal for example: (F3, 12121212112)
                lines.append(
                    (sensor, self.subjects.loc[[subjectNumber]][sensor].values[0]))
            except Exception:
                pass

        fig = go.Figure()

        if self.generalView:
            
            #########################
            ### Single panel plot ###
            #########################
            
            # Iterate over the y data and create traces for each line
            for i, line in enumerate(lines):
                # Retrieves the color of the sensor
                color = self.ddata.sensorToColorRelationship[line[0]]
                fig.add_trace(go.Scatter(y=line[1], mode='lines', name=line[0], line=dict(color=color)))
        else:
            
            ###########################
            ### Multiple panel plot ###
            ###########################

            # Create the subplots
            fig = sp.make_subplots(rows=len(lines), cols=1)

            # Plots data
            for i, line in enumerate(lines):

                # Retrieves the color of the sensor
                color = self.ddata.sensorToColorRelationship[line[0]]

                fig.add_trace(
                    # Plots the line with the corresponding color and name of the sensor
                    go.Scatter(y=line[1], mode='lines',
                               name=line[0], line=dict(color=color)),
                    row=i+1, col=1)

        # Refresh the plots UI
        fig.update_layout()
        self.plot_pane.object = fig

        # Refresh the Svg UI
        self.updateBrainFigure(subjectNumber, lines)

        return fig

    ##########################
    ### Methods definition ###
    ##########################

    def print_subjects_by_group(self):
        subjects_by_group = self.ddata.extract_subjects_by_group()

        for group, subjects in subjects_by_group.items():
            modality, artifacts = group
            print(f"Modalidade: {modality}, Artefatos: {artifacts}")
            print(subjects)
            print()

    def _changeElementHeight(self, soup, element_id, new_height):
        element = soup.find(id=element_id)
        if element is not None:
            element['height'] = str(new_height/1000)
            element["style"] = 'fill:#000000'

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
            self._changeElementHeight(
                soup, line[0] + "bar", 5 * self.calculate_total_energy(line[1]))

        # Must be the last call!
        self.svg_image.object = SVG(str(soup))

    def filterSignals(self, modalidade, estimulo, artefato=-1):

        print(f'{modalidade}, {estimulo}, {artefato}')

        if (artefato != -1):
            return self.ddata.dataframe[
                (self.ddata.dataframe.Modalidade == modalidade) &
                (self.ddata.dataframe.Estímulo == estimulo) &
                (self.ddata.dataframe.Artefatos == artefato)
            ]

        return self.ddata.dataframe[
            (self.ddata.dataframe.Modalidade == modalidade) &
            (self.ddata.dataframe.Estímulo == estimulo)
        ]


dashboard = Dashboard()
dashboard.layout.servable()
