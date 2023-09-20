import reacton
import reacton.ipyvuetify as rv
import reacton.ipywidgets as w
import math
from PIL import Image

BASE_HEIGHT = 100
CIRCUIT_OPS_PER_ROW = 20.0
DIRAC_OPS_PER_ROW = 7.0
MATRIX_OPS_PER_ROW = 7.0

DIRAC = 'dirac'
MATRIX = 'matrix'

@reacton.component
def Text(text, styling=None):
    return rv.Html(tag='h3', children=[text], style_=styling)

# TODO do some SE and combine StartingStateImage with ClickableImage
@reacton.component
def StartingStateImage(directory, notation_type, current_selected, set_current_selected, starting_state_selected, set_starting_state_selected, svg=False):
    def change_status(*ignore_args):
        set_current_selected(-1)
        set_starting_state_selected(True)
    
    # TODO fix svg assumption here
    image = rv.Html(tag='img', attributes={"src": {'./' + directory + '/' + notation_type+"_selected.svg" if starting_state_selected else './' + directory + '/' + notation_type+ "_not_selected.svg"}}, style_='height: 100px;')

    rv.use_event(image, 'click', change_status)
    
    return image
    

@reacton.component
def ClickableImage(directory, image_number, current_selected, set_current_selected, starting_state_selected, set_starting_state_selected, svg=False):
    
    def change_status(*ignore_args):
        set_current_selected(image_number)
        set_starting_state_selected(False)

    selected_image_src = None
    not_selected_image_src = None

    # Barrier
    if image_number%2!=0:
        selected_image_src = f"""./{directory}/selected.png"""
        not_selected_image_src = f"""./{directory}/not_selected.png"""

    # Gate
    else:
        selected_image_src = f"""./{directory}/{str(image_number)}/selected{".png" if not svg else ".svg"}"""
        not_selected_image_src = f"""./{directory}/{str(image_number)}/not_selected{".png" if not svg else ".svg"}"""
    image = rv.Html(tag='img', attributes={"src": {selected_image_src if current_selected else not_selected_image_src}}, style_='height: 100px;')
    rv.use_event(image, 'click', change_status)
    
    return image

@reacton.component
def NonClickableImage(directory, image_number, style="", svg=False):
    image = rv.Html(tag='img', attributes={"src": f"""./{directory}/{str(image_number)}{".png" if not svg else ".svg"}"""}, style_='height: 150px;')
    return image

@reacton.component
def CircuitRow(circ_directory, circ_barriers_directory, qc, current_selected, set_current_selected, row_lower_bound, row_upper_bound, starting_state_selected, set_starting_state_selected):

    with rv.Html(tag='div', class_='d-flex',style_='height: 125px;') as main:
        for i in range(row_lower_bound, row_upper_bound):
            if i%2!=0:
                ClickableImage(circ_barriers_directory, i, True if i == current_selected else False, set_current_selected, starting_state_selected, set_starting_state_selected)
            else:
                ClickableImage(circ_directory, i, True if i == current_selected else False, set_current_selected, starting_state_selected, set_starting_state_selected)
    return main

@reacton.component
def CircuitRows(circ_directory, circ_barriers_directory, qc, current_selected, set_current_selected, starting_state_selected, set_starting_state_selected):

    iterations = math.ceil(len(qc.data)/CIRCUIT_OPS_PER_ROW)
    lower_bound = 0

    with rv.Html(tag='div', class_='d-flex flex-column') as main:
        for i in range(0, iterations):
            if i == iterations-1:
                CircuitRow(circ_directory, circ_barriers_directory, qc, current_selected, set_current_selected, int(lower_bound), int(lower_bound+len(qc.data)%CIRCUIT_OPS_PER_ROW), starting_state_selected, set_starting_state_selected)
            else:
                CircuitRow(circ_directory, circ_barriers_directory, qc, current_selected, set_current_selected, int(lower_bound), int(lower_bound+CIRCUIT_OPS_PER_ROW), starting_state_selected, set_starting_state_selected)
                lower_bound = lower_bound+CIRCUIT_OPS_PER_ROW
    return main

@reacton.component
def DiracEquationColumn(state_directory, equation_directory, qc, current_selected, set_current_selected, starting_state_selected, set_starting_state_selected):

    with rv.Col() as main : 
        with rv.Html(tag='div', class_='d-flex justify-start'):
            for i in range(len(qc.data)-1, -1, -1):
                ClickableImage(equation_directory, i, True if i == current_selected else False, set_current_selected, starting_state_selected, set_starting_state_selected, True)
            NonClickableImage(state_directory, 0, 'height: 100px;', True)
    return main
# starting_state_directory, state_directory, equation_directory, barrier_directory, qc, current_selected, set_current_selected, 0, int(upper_bound), starting_state_selected, set_starting_state_selected, {True if upper_bound < DIRAC_OPS_PER_ROW else False})
@reacton.component
def EquationRow(starting_state_directory, equation_directory, barrier_directory, qc, current_selected, set_current_selected, row_lower_bound, row_upper_bound, starting_state_selected, set_starting_state_selected, include_equation_start=False, dirac=True):

    with rv.Html(tag='div', class_='d-flex justify-start',style_='height: 100px; margin-top: 2rem;') as main_row:
        for i in range(row_upper_bound-1, row_lower_bound-1, -1):
            # barrier
            if i%2!=0:
                ClickableImage(barrier_directory, i, True if i == current_selected else False, set_current_selected, starting_state_selected, set_starting_state_selected, True)
            else:
                ClickableImage(equation_directory, i, True if i == current_selected else False, set_current_selected, starting_state_selected, set_starting_state_selected, True)
        if include_equation_start:
            StartingStateImage(starting_state_directory, DIRAC if dirac else MATRIX, current_selected, set_current_selected, starting_state_selected, set_starting_state_selected, True)
    return main_row

@reacton.component
def DiracEquationRows(starting_state_directory, state_directory, equation_directory, barrier_directory, qc, current_selected, set_current_selected, starting_state_selected, set_starting_state_selected):

    iterations = math.ceil(len(qc.data)/DIRAC_OPS_PER_ROW)
    upper_bound = len(qc.data)

    with rv.Html(tag='div', class_='d-flex flex-column') as main:
        for i in range(0, iterations):
            if i == iterations-1:
                EquationRow(starting_state_directory, equation_directory, barrier_directory, qc, current_selected, set_current_selected, 0, 
                                 int(upper_bound), starting_state_selected, set_starting_state_selected, {True if upper_bound < DIRAC_OPS_PER_ROW else False})
            else:
                EquationRow(starting_state_directory, equation_directory, barrier_directory, qc, current_selected, set_current_selected, int(upper_bound-DIRAC_OPS_PER_ROW), int(upper_bound), starting_state_selected, set_starting_state_selected)
                upper_bound = upper_bound-DIRAC_OPS_PER_ROW
    return main

def DiracStateColumn(state_directory, current_selected, starting_state_selected):

    with rv.Col() as main : 
        with rv.Html(tag='div', class_='d-flex justify-end') as main_row:
            if starting_state_selected:
                Text("This is the starting state of your quantum circuit!")
            else:
                NonClickableImage(state_directory, current_selected+1,'height: 100px;', True)
    return main

@reacton.component
def DiracDisplay(starting_state_directory, state_directory, equation_directory, barrier_directory, qc, current_selected, set_current_selected, starting_state_selected, set_starting_state_selected):

    with rv.Html(tag='div', class_='d-flex justify-start') as main:
        DiracEquationRows(starting_state_directory, state_directory,equation_directory, barrier_directory, qc, current_selected, set_current_selected, starting_state_selected, set_starting_state_selected)
        DiracStateColumn(state_directory, current_selected, starting_state_selected)
    return main

@reacton.component
def MatrixEquationRows(starting_state_directory, state_directory, equation_directory, barrier_directory, qc, current_selected, set_current_selected, starting_state_selected, set_starting_state_selected):

    iterations = math.ceil(len(qc.data)/MATRIX_OPS_PER_ROW)
    upper_bound = len(qc.data)

    with rv.Html(tag='div', class_='d-flex flex-column') as main:
        for i in range(0, iterations):
            if i == iterations-1:
                EquationRow(starting_state_directory, equation_directory, barrier_directory, qc, current_selected, set_current_selected, 0, 
                                 int(upper_bound), starting_state_selected, set_starting_state_selected, {True if upper_bound < MATRIX_OPS_PER_ROW else False}, dirac=False)
            else:
                EquationRow(starting_state_directory, equation_directory, barrier_directory, qc, current_selected, set_current_selected, int(upper_bound-MATRIX_OPS_PER_ROW), int(upper_bound), starting_state_selected, set_starting_state_selected, dirac=False)
                upper_bound = upper_bound-MATRIX_OPS_PER_ROW
    return main

@reacton.component
def MatrixStateColumn(state_directory, equation_directory, current_selected, starting_state_selected):

    with rv.Col() as main : 
        with rv.Html(tag='div', class_='d-flex justify-end') as main_row:
            if current_selected%2 != 0 and not starting_state_selected:
                NonClickableImage(state_directory, current_selected, "height: 200px;")
    return main

@reacton.component
def MatrixDisplay(starting_state_directory, state_directory, equation_directory, barrier_directory, qc, current_selected, set_current_selected, starting_state_selected, set_starting_state_selected):

    with rv.Html(tag='div', class_='d-flex justify-start') as main:
        MatrixEquationRows(starting_state_directory, state_directory,equation_directory, barrier_directory, qc, current_selected, set_current_selected, starting_state_selected, set_starting_state_selected)
        MatrixStateColumn(state_directory, equation_directory, current_selected, starting_state_selected)
    return main
