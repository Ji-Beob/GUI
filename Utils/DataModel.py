class SymbolModel:
    def __init__(self, parsed_data):
        super().__init__()
        self.check = None

        self.data = parsed_data
        self.selectedDataIndex = None
        self.selectedDataIndexLine = None


    def setLayerSignal(self, notify_selected_to_layer):
        self.notify_selected_to_layer = notify_selected_to_layer


    def setTableSignal(self, notify_selected_to_table):
        self.notify_selected_to_table = notify_selected_to_table


    def setSelectedDataIndex(self, index, flag):
        self.selectedDataIndex = index
        if flag == 0:               # table로 시그널 보냄
            self.notify_selected_to_table(self.selectedDataIndex)
        elif flag == 1:             # layer로 시그널 보냄
            self.notify_selected_to_layer(self.selectedDataIndex)


    def getBoxData(self, idx=None):
        if idx is None:
            return self.data
        else:
            return self.data[idx]


class LineModel:
    def __init__(self, parsed_data, parsed_arrow_data):
        super().__init__()
        self.data = parsed_data
        self.arrow_data = parsed_arrow_data
        self.selectedDataIndex = None
        self.selectedDataIndexLine = None

    
    def setLayerSignalLine(self, notify_selected_to_layer):
        self.notify_selected_to_layer = notify_selected_to_layer


    def setTableSignalLine(self, notify_selected_to_table):
        self.notify_selected_to_table = notify_selected_to_table


    def setSelectedDataIndexLine(self, index, flag):
        self.selectedDataIndexLine = index
        if flag == 0:               # table로 시그널 보냄
            self.notify_selected_to_table(self.selectedDataIndexLine)
        elif flag == 1:             # layer로 시그널 보냄
            self.notify_selected_to_layer(self.selectedDataIndexLine)


    def getLineData(self, idx=None):
        if idx is None:
            return self.data
        else:
            return self.data[idx]


    def setLineData(self, i, new_data):
        self.data[i] = new_data