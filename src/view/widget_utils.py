import reacton
import reacton.ipyvuetify as rv
import reacton.ipywidgets as w
import math
from PIL import Image

BASE_HEIGHT = 100
CIRCUIT_OPS_PER_ROW = 20.0

@reacton.component
def Title(title_name):
     with rv.Html(tag='div', class_='d-flex',style_='height: 100px;') as main:
        rv.TextField(label=title_name)
        return main

@reacton.component
def ClickableImage(directory, image_number, current_selected, set_current_selected):
    
    def change_status(*ignore_args):
        
        set_current_selected(image_number)

    selected_image_src = f"""./{directory}/{str(image_number)}/selected.png"""
    not_selected_image_src = f"""./{directory}/{str(image_number)}/not_selected.png"""

    im = Image.open(selected_image_src)
    width, height = im.size

    hpercent = (BASE_HEIGHT/width)
    wsize = int(height*float(hpercent))

    # image = rv.Img(src= selected_image_src if current_selected else not_selected_image_src,style_='height: 100px;', max_width="100px" if directory == 'dirac_equations' else None)
    image = rv.Html(tag='img', attributes={"src": {selected_image_src if current_selected else not_selected_image_src}}, style_='height: 100px;')
    rv.use_event(image, 'click', change_status)
    
    return image

@reacton.component
def NonClickableImage(directory, image_number):
    image = rv.Html(tag='img', attributes={"src": f"""./{directory}/{str(image_number)}.png"""}, style_='height: 100px;')
    # image = rv.Img(src=f"""./{directory}/{str(image_number)}.png""", max_height="200px", max_width="200px")
    return image

@reacton.component
def CircuitRow(directory, qc, current_selected, set_current_selected, row_lower_bound, row_upper_bound):

    with rv.Html(tag='div', class_='d-flex',style_='height: 100px;') as main:
        for i in range(row_lower_bound, row_upper_bound):
            ClickableImage(directory, i, True if i == current_selected else False, set_current_selected)
    
    return main
@reacton.component
def CircuitRows(directory, qc, current_selected, set_current_selected):
    iterations = math.ceil(len(qc.data)/CIRCUIT_OPS_PER_ROW)

    lower_bound = 0
    with rv.Html(tag='div', class_='d-flex flex-column') as main:
        for i in range(0, iterations):
            if i == iterations-1:
                CircuitRow(directory, qc, current_selected, set_current_selected, int(lower_bound), int(lower_bound+len(qc.data)%CIRCUIT_OPS_PER_ROW))
            else:
                CircuitRow(directory, qc, current_selected, set_current_selected, int(lower_bound), int(lower_bound+CIRCUIT_OPS_PER_ROW))
                lower_bound = lower_bound+CIRCUIT_OPS_PER_ROW
    return main

@reacton.component
def DiracEquationColumn(state_directory, equation_directory, qc, current_selected, set_current_selected):
    with rv.Col() as main : 
        with rv.Html(tag='div', class_='d-flex justify-start') as main_row:
            for i in range(len(qc.data)-1, -1, -1):
                ClickableImage(equation_directory, i, True if i == current_selected else False, set_current_selected)
            NonClickableImage(state_directory, 0)
    return main

def DiracStateColumn(state_directory, current_selected):
    with rv.Col() as main : 
        with rv.Html(tag='div', class_='d-flex justify-end') as main_row:
            NonClickableImage(state_directory, current_selected)
    return main

@reacton.component
def DiracRow(state_directory, equation_directory, qc, current_selected, set_current_selected):

    with rv.Html(tag='div', class_='d-flex justify-start') as main:
        DiracEquationColumn(state_directory, equation_directory, qc, current_selected, set_current_selected)
        DiracStateColumn(state_directory, current_selected)

    return main
