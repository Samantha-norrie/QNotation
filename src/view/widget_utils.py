import reacton
import reacton.ipyvuetify as rv
import reacton.ipywidgets as w

@reacton.component
def ClickableImage(image_number, current_selected, set_current_selected):
    selected, set_selected = reacton.use_state(False)
    
    def change_status(*ignore_args):
        
        set_current_selected(image_number)

    image = rv.Img(src=f"""./circ/{str(image_number)}/selected.png""" if current_selected else f"""./circ/{str(image_number)}/not_selected.png""")
    rv.use_event(image, 'click', change_status)
    
    return image

@reacton.component
def CircuitRow(qc, current_selected, set_current_selected):
    with rv.Row(style="height 50px") as main:
        for i in range(0, len(qc.data)):
            ClickableImage(i, True if i == current_selected else False, set_current_selected)
    
    return main

# @reacton.component
# def DiracRow(qc, current_selected):
#     barrier_states = get_barrier_states(qc, 3)
#     with rv.Row(style="height 50px") as main:
#         # Is a barrier
#         if current_selected%2 == 0:
# #             rv.Img(src=f"""./circ/{current_selected/2}.png""")
# #             barrier_states[current_selected/2]
#             barrier_states[2]
#     return main