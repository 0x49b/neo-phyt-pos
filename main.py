import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatterlayout import ScatterLayout

kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.config import Config

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'resizable', False)
# Config.set('graphics', 'fullscreen', 1)

# for now, use a global for blink speed (better implementation TBD):
speed = 1.0

# Set up GPIO:
beepPin = 17
ledPin = 27
buttonPin = 22
flashLedPin = 10


# Define some helper functions:

# This callback will be bound to the LED toggle and Beep button:
def press_callback(obj):
    print("Button pressed,", obj.text)
    if obj.text == 'BEEP!':
        # turn on the beeper:

        # schedule it to turn off:
        Clock.schedule_once(buzzer_off, .1)
    if obj.text == 'LED':
        if obj.state == "down":
            print("button on")

        else:
            print("button off")


def buzzer_off(dt):
    print("buzzer off")


# Toggle the flashing LED according to the speed global
# This will need better implementation
def flash(dt):
    global speed
    Clock.schedule_once(flash, 1.0 / speed)


# This is called when the slider is updated:
def update_speed(obj, value):
    global speed
    print("Updating speed to:" + str(obj.value))
    speed = obj.value


# Modify the Button Class to update according to GPIO input:
class InputButton(Button):
    def update(self, dt):
        self.state = 'down'


class MyApp(App):

    def build(self):
        # Set up the layout:
        layout = GridLayout(cols=5, rows=1, spacing=30, padding=30)

        # Make the background gray:
        with layout.canvas.before:
            Color(.2, .2, .2, 5)
            self.rect = Rectangle(size=(800, 480), pos=layout.pos)

        # Instantiate the first UI object (the GPIO input indicator):
        inputDisplay = InputButton(text="Input")

        # Schedule the update of the state of the GPIO input button:
        Clock.schedule_interval(inputDisplay.update, 1.0 / 10.0)

        # Create the rest of the UI objects (and bind them to callbacks, if necessary):
        outputControl = ToggleButton(text="LED")
        outputControl.bind(on_press=press_callback)
        beepButton = Button(text="BEEP!", size=(50, 50))
        beepButton.bind(on_press=press_callback)
        wimg = Image(source='logo.png')
        speedSlider = Slider(orientation='vertical', min=1, max=30, value=speed)
        speedSlider.bind(on_touch_down=update_speed, on_touch_move=update_speed)

        # Add the UI elements to the layout:
        layout.add_widget(wimg)
        layout.add_widget(inputDisplay)
        layout.add_widget(outputControl)
        layout.add_widget(beepButton)
        layout.add_widget(speedSlider)

        # Start flashing the LED
        Clock.schedule_once(flash, 1.0 / speed)

        return layout


if __name__ == '__main__':
    MyApp().run()
