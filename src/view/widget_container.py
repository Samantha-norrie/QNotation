import reacton
import reacton.ipyvuetify as rv
import reacton.ipywidgets as w
from .widget_utils import *

@reacton.component
def Container(qc, qc_with_barriers):
    current_selected, set_current_selected = reacton.use_state(2)
    
    with rv.Html(tag='div') as main:
        Title('Circuit')
        CircuitRows('circ', 'circ_barriers', qc_with_barriers, current_selected, set_current_selected)
        Title('Dirac')
        DiracDisplay('dirac','dirac_equations', 'barriers', qc_with_barriers, current_selected, set_current_selected)
        Title('Matrix')
    return main