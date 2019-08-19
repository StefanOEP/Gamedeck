import npyscreen


class CustomButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.when_pressed()
