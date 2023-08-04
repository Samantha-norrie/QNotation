import reacton
import reacton.ipyvuetify as rv
import reacton.ipywidgets as w
import math
from PIL import Image

BASE_HEIGHT = 100
CIRCUIT_OPS_PER_ROW = 20.0
DIRAC_OPS_PER_ROW = 10.0

@reacton.component
def Text(text, styling=None):
    return rv.Html(tag='h3', children=[text], style_=styling)

@reacton.component
def ClickableImage(directory, image_number, current_selected, set_current_selected, svg=False):
    
    def change_status(*ignore_args):
        set_current_selected(image_number)

    selected_image_src = None
    not_selected_image_src = None

    # Barrier
    if image_number%2==0:
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
def NonClickableImage(directory, image_number, svg=False):
    image = rv.Html(tag='img', attributes={"src": f"""./{directory}/{str(image_number)}{".png" if not svg else ".svg"}"""}, style_='height: 100px;')
    return image

@reacton.component
def CircuitRow(circ_directory, circ_barriers_directory, qc, current_selected, set_current_selected, row_lower_bound, row_upper_bound):

    with rv.Html(tag='div', class_='d-flex',style_='height: 100px;') as main:
        for i in range(row_lower_bound, row_upper_bound):
            if i%2==0:
                ClickableImage(circ_barriers_directory, i, True if i == current_selected else False, set_current_selected)
            else:
                ClickableImage(circ_directory, i, True if i == current_selected else False, set_current_selected)
    return main

@reacton.component
def CircuitRows(circ_directory, circ_barriers_directory, qc, current_selected, set_current_selected):

    iterations = math.ceil(len(qc.data)/CIRCUIT_OPS_PER_ROW)
    lower_bound = 0

    with rv.Html(tag='div', class_='d-flex flex-column') as main:
        for i in range(0, iterations):
            if i == iterations-1:
                CircuitRow(circ_directory, circ_barriers_directory, qc, current_selected, set_current_selected, int(lower_bound), int(lower_bound+len(qc.data)%CIRCUIT_OPS_PER_ROW))
            else:
                CircuitRow(circ_directory, circ_barriers_directory, qc, current_selected, set_current_selected, int(lower_bound), int(lower_bound+CIRCUIT_OPS_PER_ROW))
                lower_bound = lower_bound+CIRCUIT_OPS_PER_ROW
    return main

@reacton.component
def DiracEquationColumn(state_directory, equation_directory, qc, current_selected, set_current_selected):

    with rv.Col() as main : 
        with rv.Html(tag='div', class_='d-flex justify-start'):
            for i in range(len(qc.data)-1, -1, -1):
                ClickableImage(equation_directory, i, True if i == current_selected else False, set_current_selected, True)
            NonClickableImage(state_directory, 0, True)
    return main

@reacton.component
def DiracEquationRow(state_directory, equation_directory, barrier_directory, qc, current_selected, set_current_selected, row_lower_bound, row_upper_bound, include_equation_start=False):

    with rv.Html(tag='div', class_='d-flex justify-start',style_='height: 100px; margin-top: 2rem;') as main_row:
        for i in range(row_upper_bound-1, row_lower_bound-1, -1):
            # barrier
            if i%2==0:
                ClickableImage(barrier_directory, i, True if i == current_selected else False, set_current_selected, True)
            else:
                ClickableImage(equation_directory, i, True if i == current_selected else False, set_current_selected, True)
            # if include_equation_start:
            #     NonClickableImage(state_directory, 0, True)
    return main_row

@reacton.component
def DiracEquationRows(state_directory, equation_directory, barrier_directory, qc, current_selected, set_current_selected):

    iterations = math.ceil(len(qc.data)/DIRAC_OPS_PER_ROW)
    upper_bound = len(qc.data)

    with rv.Html(tag='div', class_='d-flex flex-column') as main:
        for i in range(0, iterations):
            if i == iterations-1:
                DiracEquationRow(state_directory, equation_directory, barrier_directory, qc, current_selected, set_current_selected, 0, int(upper_bound))
            else:
                DiracEquationRow(state_directory, equation_directory, barrier_directory, qc, current_selected, set_current_selected, int(upper_bound-DIRAC_OPS_PER_ROW), int(upper_bound),
                                 {True if i==0 else False})
                upper_bound = upper_bound-DIRAC_OPS_PER_ROW
    return main

def DiracStateColumn(state_directory, current_selected):

    with rv.Col() as main : 
        with rv.Html(tag='div', class_='d-flex justify-end') as main_row:
            NonClickableImage(state_directory, current_selected, True)
    return main

@reacton.component
def DiracDisplay(state_directory, equation_directory, barrier_directory, qc, current_selected, set_current_selected):

    with rv.Html(tag='div', class_='d-flex justify-start') as main:
        DiracEquationRows(state_directory,equation_directory, barrier_directory, qc, current_selected, set_current_selected)
        DiracStateColumn(state_directory, current_selected)
    return main
