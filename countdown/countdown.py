from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader, Sound
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout


class MainWidget(BoxLayout):
    time_left = 0
    display = StringProperty('__:__')
    sound: Sound = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.alarm = None
        self.event = None
        self.sound = SoundLoader.load(
            'assets/alarm.wav'
        )
        self.alarm_animation = ['!_:!_', '_!:_!']
        self.alarm_animation_index = 0

    def start(self, value):
        self.time_left = value
        if self.event is not None:
            self.event.cancel()
        self.event = Clock.schedule_interval(self.update, 1)

    def stop(self):
        self.stop_countdown()
        self.stop_alarm()

    def stop_countdown(self):
        if self.event is None:
            return
        self.event.cancel()
        self.event = None
        self.time_left = 0

    def add(self, value):
        self.time_left += value

    def update(self, dt):
        self.time_left = round(self.time_left - dt)
        if self.time_left < 1:
            self.end_countdown()
        else:
            self.update_display()

    def update_display(self):
        minutes = int(self.time_left / 60)
        seconds = int(self.time_left % 60)
        if minutes == 0 and seconds == 0:
            self.display = '__:__'
        else:
            self.display = f'{minutes:02}:{seconds:02}'

    def end_countdown(self):
        self.stop_countdown()
        self.start_alarm()

    def start_alarm(self):
        if self.alarm is not None:
            self.alarm.cancel()
        self.display = '!!:!!'
        self.play_alarm(0)
        self.alarm = Clock.schedule_interval(self.play_alarm,
                                             self.sound.length)

    def play_alarm(self, _dt):
        self.display = self.alarm_animation[
            self.alarm_animation_index]
        self.alarm_animation_index = (
            self.alarm_animation_index + 1) % len(
            self.alarm_animation)
        self.sound.play()

    def stop_alarm(self):
        if self.alarm is None:
            return
        self.alarm.cancel()
        self.alarm = None
        self.sound.stop()
        self.display = '__:__'


class CountdownApp(App):
    pass
