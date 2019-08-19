import npyscreen
from UI.CustomUI.CustomSingleSelect import CustomSingleSelect

class CustomBoxTitleSingleSelect(npyscreen.BoxTitle): 
    _contained_widget = CustomSingleSelect
    
