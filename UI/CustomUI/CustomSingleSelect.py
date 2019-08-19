import npyscreen

class CustomSingleSelect(npyscreen.SelectOne): 

    def display_value(self, vl):       
        return vl.name;