import npyscreen

class CustomInputBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLineEditableBoxed

    def when_value_edited(self):
        self.parent.parentApp.queue_event(npyscreen.Event("event_value_edited"))