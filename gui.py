import threading
from typing import Union, Any
import PySimpleGUI as sg
from analyzer import Analyzer


class Gui:
    def __init__(self):
        self._window = None
        self._output = None
        self._message = None
        self._answer = None
        self.button_image_play = b"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAQAAADZc7J/AAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6\
        AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QA/4ePzL8AAAAJcEhZcwAACxgAAAsYAYmptRAAAAAHdElNRQfnBAEXERtKfB82AAACFUlEQVRIx+3USUjU\
        YRjH8c/MqKMNtrmjtkmUEpV1aRHCKA06COGpQ8ulc1TQQahLRR0i6maEly51sCK6RgtB0YJY0YpFStgiSblh89fpUAhjf2061+/2Pu/zfJ/n4eF5CFfEEif\
        1SEn56KxaUX+lNW5I6vPIfb0CDzWKZB6+yE1J7TYpV6ZOmxGdajMNj2oRuKR8wjJXqzFnxDMDFLrli4Y022rvPLUoLFsYoFK3Z2m2Lq+UKc0MkCPHsO9ptq\
        RhWWEt/OVw/gP+AUBUQtYfI2ISYuGAZVo1TbxSUwA2OGddOGCpZg1ikgI5sifljRsXoE6zleGAbwLF4vp9UGFBGqDcQn0+iSmT8jUc0OOTxUp9dluRnWZN/\
        OTZrspd3eaoMeBteHczXTJiB1Z4bMgp1RJmqHLYF+/UY4t+d8LW+qd2GXFdBZq8EHjpsnZPfNdtt5g5LggcnHr4Ja5JOiFf1Fpt3hgwqNtFm2WLO2DYPVXT\
        TXmD1wYcUYw8NRo0Wi4fs+zXp9e26a9zVLMuo67YquBXqVGz1TtvSK89ctIDfqfFbNRivUEdOr03rtRyqxTocNzVSacuVBHz7HNHv6QxYwLfPHDIkrDip+o\
        npki1VfZKOO2u53oFf879+1QeeGvpdC7h25etRNy4YrmyVRoVlfTRaKYt1DtmtpQslWJ6jIoYcVR7phXkmq9QCuPGlIuIGJQIc/0B0/KQ+d6PyJgAAAAldE\
        VYdGRhdGU6Y3JlYXRlADIwMjMtMDQtMDFUMjA6MTc6MjcrMDM6MDAl78HIAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIzLTA0LTAxVDIwOjE3OjI3KzAzOjAwV\
        LJ5dAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAAASUVORK5CYII="
        sg.theme('DarkAmber')  # Add a touch of color
        # All the stuff inside your window.
        layout = [[sg.Text("Press 'listen' to start talking with ChatGPT")],
                  [sg.Multiline(default_text=self._update_output(), size=(100, 10), key='-INPUT-', disabled=True)],
                  [sg.Button(image_data=self.button_image_play, key='listen', button_color=sg.theme_background_color(),
                             border_width=0)]]

        # Create the Window
        self._window = sg.Window('TalkGpT', layout, layout, enable_close_attempted_event=True,
                            location=sg.user_settings_get_entry('-location-', (None, None)))

    def _update_output(self):
        if self._message is None and self._answer is None:
            self._output = "Waiting for input."
        else:
            self._output = f"Message: \n{self._message} \n\n\n" \
                           f"ChatGpt answer: \n{self._answer}"

        return self._output

    def _analyze(self):
        message: Union[str, Any]
        message, is_success = Analyzer.speech2text()
        self._message = message
        self._window['-INPUT-'].update(value=self._update_output())
        self._answer = Analyzer.ask_gpt(message)
        self._window['-INPUT-'].update(value=self._update_output())
        self._answer = Analyzer.text2speech(self._answer)
        self._window['-INPUT-'].update(value=self._update_output())

    def run(self):
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = self._window.read()
            self._window['-INPUT-'].update(value=self._update_output())
            if event in ('Exit', sg.WINDOW_CLOSE_ATTEMPTED_EVENT):
                sg.user_settings_set_entry('-location-',
                                           self._window.current_location())
                break

            if event == 'listen':
                thread1 = threading.Thread(target=self._analyze)
                thread1.start()

        self._window.close()
