import reacton
import reacton.ipyvuetify as rv
import reacton.ipywidgets as w
from .widget_utils import *

NOTATION_TITLE_STYLING = "padding-top: 1rem;"
ERROR_STYLING = "color: red;"

@reacton.component
def LoadingContainer():
    with rv.Html(tag='div') as main:
         Text("Loading")
    return main

@reacton.component
def ErrorContainer(error_message):
    with rv.Html(tag='div') as main:
        Text(error_message, styling=ERROR_STYLING)
    return main   

@reacton.component
def WidgetContainer(qc, qc_with_barriers):
    current_selected, set_current_selected = reacton.use_state(2)
    starting_state_selected, set_starting_state_selected = reacton.use_state(False)
    
    with rv.Html(tag='div') as main:
        Text('Circuit', styling=NOTATION_TITLE_STYLING)
        CircuitRows('circ', 'circ_barriers', qc_with_barriers, current_selected, set_current_selected, starting_state_selected, set_starting_state_selected)
        Text('Dirac', NOTATION_TITLE_STYLING)
        DiracDisplay('starting_states', 'dirac','dirac_equations', 'barriers', qc_with_barriers, current_selected, set_current_selected, starting_state_selected, set_starting_state_selected)
        Text('Matrix', NOTATION_TITLE_STYLING)
        MatrixDisplay('starting_states', 'matrix','matrix_equations', 'barriers', qc_with_barriers, current_selected, set_current_selected, starting_state_selected, set_starting_state_selected)
    return main