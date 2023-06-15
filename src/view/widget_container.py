import reacton
import reacton.ipyvuetify as rv
import reacton.ipywidgets as w
from .widget_utils import *

@reacton.component
def Container(qc, qc_with_barriers):
    current_selected, set_current_selected = reacton.use_state(2)
    
    with rv.Container() as main:
        CircuitRow(qc_with_barriers, current_selected, set_current_selected)
        # DiracRow(qc_orig, current_selected)
    return main