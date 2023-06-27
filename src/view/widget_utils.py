import reacton
import reacton.ipyvuetify as rv
import reacton.ipywidgets as w
from PIL import Image

BASE_HEIGHT = 100

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

    image = rv.Img(src= selected_image_src if current_selected else not_selected_image_src, max_width="100px" if directory == 'dirac_equations' else None)
    rv.use_event(image, 'click', change_status)
    
    return image

@reacton.component
def NonClickableImage(directory, image_number):
    image = rv.Img(src=f"""./{directory}/{str(image_number)}.png""", max_height="200px", max_width="200px")
    return image

@reacton.component
def CircuitRow(directory, qc, current_selected, set_current_selected):
    with rv.Html(tag='div', class_='d-flex', style_='height 100px') as main:
        for i in range(0, len(qc.data)):
            ClickableImage(directory, i, True if i == current_selected else False, set_current_selected)
    
    return main

@reacton.component
def DiracRow(state_directory, equation_directory, qc, current_selected, set_current_selected):

    with rv.Html(tag='div', class_='d-flex justify-start') as main:
        for i in range(0, len(qc.data)):
            ClickableImage(equation_directory, i, True if i == current_selected else False, set_current_selected)
        NonClickableImage(state_directory, current_selected)

    return main