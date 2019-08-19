import npyscreen
from UI.CustomUI.CustomMultiSelect import CustomMultiSelect

class CustomBoxTitle(npyscreen.BoxTitle): 
    _contained_widget = CustomMultiSelect
    
