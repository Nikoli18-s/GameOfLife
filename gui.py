import PySimpleGUI as sg
import logic
import time


class GUI:
    def __init__(self):
        # colors
        self.theme_color = '#0c231e'
        self.first_color = '#008000'
        self.second_color = '#003200'

        # theme
        sg.theme('DarkGreen7')

        # start screen
        self.start_button = sg.Button(key='START', button_text='Start', font=('Arial', 40), size=(12, 2), pad=(450, 300))

        # main screen
        self.graph_len = 500
        self.graph = sg.Graph(key='GRAPH', background_color=self.second_color,
                              canvas_size=(680, 680), graph_bottom_left=(0, 0),
                              graph_top_right=(self.graph_len, self.graph_len),
                              pad=(10, 10), enable_events=True, drag_submits=True, visible=False)
        ###
        self.text_1 = sg.Text(key='X', text='X: ', font=('Arial Bold', 20), pad=(10, 10),
                              enable_events=True, visible=False)
        self.input_1 = sg.Input(key='X_VAL', font=('Arial Bold', 20), pad=(10, 10),
                                enable_events=True, expand_x=True, visible=False)
        ###
        self.text_2 = sg.Text(key='Y', text='Y: ', font=('Arial Bold', 20), pad=(10, 10),
                              enable_events=True, visible=False)
        self.input_2 = sg.Input(key='Y_VAL', font=('Arial Bold', 20), pad=(10, 10),
                                enable_events=True, expand_x=True, visible=False)
        ###
        self.boundary = sg.Listbox(['wall', 'cyclic'], default_values=['wall'], key='CH_BOUND_COND', size=(9, 2),
                                   font=('Arial Bold', 20), pad=(10, (10, 330)), enable_events=True, visible=False)
        self.initial = sg.Listbox(['random', 'custom'], default_values=['random'], key='CH_GEN_TYPE', size=(9, 2),
                                  font=('Arial Bold', 20), pad=(25, (10, 330)), enable_events=True, visible=False)
        self.apply_button = sg.Button(key='APPLY', button_text='Apply', font=('Arial', 20), size=(9, 2),
                                      pad=(10, (10, 330)), enable_events=True, visible=False)
        ###
        self.text_3 = sg.Text(key='STEP', text='Step 0 ', font=('Arial Bold', 20), justification='center', pad=(10, 10),
                              enable_events=True, visible=False)
        ###
        self.stop_button = sg.Button(key='STOP', button_text='||', font=('Arial', 20), size=(9, 1), pad=(10, 10),
                                     enable_events=True, visible=False)
        self.next_button = sg.Button(key='NEXT', button_text='>', font=('Arial', 20), size=(9, 1), pad=(25, 10),
                                     enable_events=True, visible=False)
        self.run_button = sg.Button(key='RUN', button_text='>>', font=('Arial', 20), size=(9, 1), pad=(10, 10),
                                    enable_events=True, visible=False)

        layout = [[sg.Column([[self.start_button, self.graph]]),
                   sg.Column([[self.text_1, self.input_1],
                              [self.text_2, self.input_2],
                              [self.boundary, self.initial, self.apply_button],
                              [self.text_3],
                              [self.stop_button, self.next_button, self.run_button]
                              ])]]

        self.window = sg.Window('Game of Life', layout, size=(1280, 720))
        self.field = logic.Field(10, 10, True)

    def run(self):
        run_flag = False
        draw_flag = False

        while True:
            event, values = self.window.read(timeout=200)

            # print(event, values)

            # process events
            if event == sg.WIN_CLOSED:
                break

            #
            if event == 'START':
                self.window['START'].update(visible=False)

                self.window['GRAPH'].update(visible=True)

                self.window['X'].update(visible=True)
                self.window['Y'].update(visible=True)
                self.window['X_VAL'].update(visible=True)
                self.window['Y_VAL'].update(visible=True)
                self.window['CH_BOUND_COND'].update(visible=True)
                self.window['CH_GEN_TYPE'].update(visible=True)
                self.window['APPLY'].update(visible=True)
                self.window['STEP'].update(visible=True)
                self.window['STOP'].update(visible=True)
                self.window['NEXT'].update(visible=True)
                self.window['RUN'].update(visible=True)

            #
            if event == 'APPLY':
                self.window['GRAPH'].erase()

                x = int(values['X_VAL'])
                y = int(values['Y_VAL'])
                boundary = values['CH_BOUND_COND']
                generation = values['CH_GEN_TYPE']

                if boundary == ['wall']:
                    self.field.reset(x, y, True)

                if boundary == ['cyclic']:
                    self.field.reset(x, y, False)

                if generation == ['random']:
                    self.field.random_set()

                if generation == ['custom']:
                    draw_flag = True

                self.draw_field()
                output = 'Step ' + str(self.field.step)
                self.window['STEP'].update(output)

            if event == 'GRAPH' and draw_flag:
                x_px, y_px = values['GRAPH']
                self.set_unset_point(x_px, y_px)
                self.draw_field()
                time.sleep(0.1)

            #
            if event == 'NEXT':
                self.field.update()
                self.draw_field()
                output = 'Step ' + str(self.field.step)
                self.window['STEP'].update(output)

            if event == 'RUN':
                run_flag = True

            if event == 'STOP':
                run_flag = False

            if run_flag:
                self.field.update()
                self.draw_field()
                output = 'Step ' + str(self.field.step)
                self.window['STEP'].update(output)

        # end
        self.window.close()

    def enable_cell(self, cell_px, x, y, shift_x, shift_y):
        x_px = shift_x + x * cell_px
        y_px = shift_y + y * cell_px
        self.window['GRAPH'].draw_rectangle((x_px + 1, y_px + cell_px - 1), (x_px + cell_px - 1, y_px + 1),
                                            fill_color=self.first_color, line_color=self.first_color, line_width=1)

    def disable_cell(self, cell_px, x, y, shift_x, shift_y):
        x_px = shift_x + x * cell_px
        y_px = shift_y + y * cell_px
        self.window['GRAPH'].draw_rectangle((x_px + 1, y_px + cell_px - 1), (x_px + cell_px - 1, y_px + 1),
                                            fill_color=self.second_color, line_color=self.second_color, line_width=1)

    def draw_field(self):
        nx = self.field.width
        ny = self.field.height

        cell_px = self.graph_len // max(nx, ny)

        shift_x = (self.graph_len - nx * cell_px) // 2
        shift_y = (self.graph_len - ny * cell_px) // 2

        x_cur = shift_x
        y_cur = shift_y

        while x_cur <= self.graph_len - shift_x:
            self.window['GRAPH'].draw_line((x_cur, shift_y),
                                           (x_cur, self.graph_len - shift_y),
                                           color=self.theme_color, width=1)
            x_cur += cell_px

        while y_cur <= self.graph_len - shift_y:
            self.window['GRAPH'].draw_line((shift_x, y_cur),
                                           (self.graph_len - shift_x, y_cur),
                                           color=self.theme_color, width=1)
            y_cur += cell_px

        self.window['GRAPH'].draw_rectangle((0, self.graph_len), (shift_x, 0),
                                            fill_color=self.theme_color, line_color=self.theme_color, line_width=1)
        self.window['GRAPH'].draw_rectangle((0, self.graph_len), (self.graph_len, self.graph_len - shift_y),
                                            fill_color=self.theme_color, line_color=self.theme_color, line_width=1)
        self.window['GRAPH'].draw_rectangle((self.graph_len - shift_x, self.graph_len), (self.graph_len, 0),
                                            fill_color=self.theme_color, line_color=self.theme_color, line_width=1)
        self.window['GRAPH'].draw_rectangle((0, shift_y), (self.graph_len, 0),
                                            fill_color=self.theme_color, line_color=self.theme_color, line_width=1)

        for i in range(nx):
            for j in range(ny):
                x = i
                y = ny - 1 - j
                if self.field.field[j][i] == 1:
                    self.enable_cell(cell_px, x, y, shift_x, shift_y)
                else:
                    self.disable_cell(cell_px, x, y, shift_x, shift_y)

    def set_unset_point(self, x_px, y_px):
        nx = self.field.width
        ny = self.field.height

        cell_px = self.graph_len // max(nx, ny)

        shift_x = (self.graph_len - nx * cell_px) // 2
        shift_y = (self.graph_len - ny * cell_px) // 2

        _x = (x_px - shift_x) // cell_px
        _y = (self.graph_len - y_px - shift_y) // cell_px

        if self.field.field[_y][_x] == 0:
            self.field.set(_x, _y)
        else:
            self.field.unset(_x, _y)