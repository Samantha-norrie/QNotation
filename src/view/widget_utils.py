import reacton
import reacton.ipyvuetify as rv
import reacton.ipywidgets as w

@reacton.component
def ClickableImage(directory, image_number, current_selected, set_current_selected):
    
    def change_status(*ignore_args):
        
        set_current_selected(image_number)

    image = rv.Img(src=f"""./{directory}/{str(image_number)}/selected.png""" if current_selected else f"""./circ/{str(image_number)}/not_selected.png""")
    rv.use_event(image, 'click', change_status)
    
    return image

@reacton.component
def NonClickableImage(directory, image_number):
    image = rv.Img(src=f"""./{directory}/{str(image_number)}.png""")
    return image

@reacton.component
def CircuitRow(directory, qc, current_selected, set_current_selected):
    with rv.Row(style="height 50px") as main:
        for i in range(0, len(qc.data)):
            ClickableImage(directory, i, True if i == current_selected else False, set_current_selected)
    
    return main

@reacton.component
def DiracRow(directory, qc, current_selected, set_current_selected):
    print('in dirac row')
    with rv.Row(style="height 50px") as main:
        print('creating image')
        NonClickableImage(directory, current_selected)
    return main