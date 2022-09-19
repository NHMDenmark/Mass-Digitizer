import PySimpleGUI as sg

class GUI():
    def __init__(self):
        self.data = [(10), (20), (30), (40), (50), (60), (70), (80), (90), (100), 11, 12, 13]
        self.dataEnum = []
        for count, value in enumerate(self.data):
            dataTup = (count+1, value)
            self.dataEnum.append(dataTup)
        print('dataTup : ', self.dataEnum)
        self.work_order_currrent_selection_index = 1
        self.num_rows = 6
        self.stepMover = 0
        self.steplist = []

    def run(self):
        layout = [[sg.Listbox(values=self.data, size=(35, self.num_rows), select_mode='browse', enable_events=True, key='selected_key')]]
        # Create the Window
        self.testWindow = sg.Window('Test', layout, return_keyboard_events=True, finalize=True)

        while True:
            event, values = self.testWindow.Read()
            if event is None:
                break
            if event.startswith('Up'):
                print('type steplist: ', type(self.steplist))
                stepCopy = self.steplist.copy()
                # self.steplist = reversed(stepCopy)
                print('Up press index: ', self.work_order_currrent_selection_index)
                if self.work_order_currrent_selection_index != 0 and self.work_order_currrent_selection_index % 3 == 0:
                    print('modded indx at: ', self.work_order_currrent_selection_index % 3)
                    # self.stepMover = (self.work_order_currrent_selection_index / 35) - 0.1
                    stepSkip = stepCopy.pop()
                    print('stepSkip is now: ', stepSkip)
                    # self.testWindow['selected_key'].Widget.yview_moveto(self.stepMover)
                    self.testWindow['selected_key'].Widget.yview_moveto(stepSkip)
                # self.testWindow['selected_key'].Widget.yview_moveto(self.stepMover)
                self.work_order_currrent_selection_index = (self.work_order_currrent_selection_index - 1) % len(self.data)
                print('enum -- ', self.dataEnum[self.work_order_currrent_selection_index], self.dataEnum[self.work_order_currrent_selection_index][0])
                modded = self.work_order_currrent_selection_index % self.num_rows
                if modded == 0:
                    verticalPosition = self.work_order_currrent_selection_index
                # self.testWindow['selected_key'].Update(set_to_index=self.work_order_currrent_selection_index, scroll_to_index=modded )

            elif event.startswith('Down'):
                enumenor = self.dataEnum[self.work_order_currrent_selection_index][0]
                print('enum -- ', self.dataEnum[self.work_order_currrent_selection_index], enumenor)
                if self.work_order_currrent_selection_index != 0 and enumenor % 3 == 0:
                    print('modded indx at: ', enumenor)
                    # self.stepMover = (self.work_order_currrent_selection_index/20)+0.1
                    self.stepMover = (enumenor / 35) + 0.1
                    self.steplist.append(self.stepMover)
                    print('stepmover is now: ', self.stepMover)
                    self.testWindow['selected_key'].Widget.yview_moveto(self.stepMover)
                self.work_order_currrent_selection_index = (self.work_order_currrent_selection_index + 1) % len(self.data)

                # print(self.work_order_currrent_selection_index)
                # modded = self.work_order_currrent_selection_index % self.num_rows
                # if modded == 0:
                #     verticalPosition = self.work_order_currrent_selection_index - 3
                # self.testWindow['selected_key'].Update(set_to_index=self.work_order_currrent_selection_index, scroll_to_index=modded)
            # self.testWindow.Element('selected_key').Update(set_to_index=self.work_order_currrent_selection_index)
        self.testWindow.Close()

if __name__ == '__main__':
    app = GUI()
    app.run()