import reacton
import reacton.ipyvuetify as rv
import reacton.ipywidgets as w

class WidgetContainer(w.VBox):
    def __init__(self, qc):
        self.circuit_images = None
        self.dirac_images = None
        self.matrix_images = None


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

    @reacton.component
    def Container():
        current_selected, set_current_selected = reacton.use_state(2)
        
        with rv.Container() as main:
            CircuitRow(current_selected, set_current_selected)
            # DiracRow(qc_orig, current_selected)
        return main
    
    
# qc = QuantumCircuit(3)
# qc.h(0)
# qc.h(1)
# qc.h(0)
# qc.h(2)
# qc.x(1)

# qc2 = create_highlighted_circuit_figures(qc)
# print(qc.data)

# WidgetContainer.Container()