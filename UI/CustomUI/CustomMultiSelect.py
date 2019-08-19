import npyscreen


class CustomMultiSelect(npyscreen.MultiSelect):

    def display_value(self, vl):
        return vl.name
