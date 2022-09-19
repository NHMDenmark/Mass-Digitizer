import PySimpleGUI as sg

class GUI():
    def __init__(self):
        self.data = [(10), (20), (30), (40), (50), (60), (70), (80), (90), (100)]
        self.work_order_currrent_selection_index = 0

    def run(self):
        layout = [[sg.Listbox(values=self.data, size=(35, 3), enable_events=True, key='selected_key')]]
        # Create the Window
        self.testWindow = sg.Window('Test', return_keyboard_events=True).Layout(layout).Finalize()
        # self.testWindow.Maximize()
        self.testWindow.Element('selected_key').Update(set_to_index=0)
        # Event Loop to process "events"
        while True:
            event, values = self.testWindow.Read()
            if event in('Up:111', '16777235'):
                if(hasattr(self, 'testWindow')):
                    self.work_order_currrent_selection_index = (self.work_order_currrent_selection_index - 1) % len(self.data)
                    self.testWindow.Element('selected_key').Update(set_to_index=self.work_order_currrent_selection_index)
            elif event in ('Down:116',' 16777237'):
                if(hasattr(self, 'testWindow')):
                    self.work_order_currrent_selection_index = (self.work_order_currrent_selection_index + 1) % len(self.data)
                    self.testWindow.Element('selected_key').Update(set_to_index=self.work_order_currrent_selection_index)

        self.testWindow.Close()

if __name__ == '__main__':
    app = GUI()
    app.run()