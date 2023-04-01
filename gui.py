import logging
import threading
from typing import Union, Any
import PySimpleGUI as sg
from analyzer import Analyzer
from openai_connector import chatgpt


class Gui:
    def __init__(self):
        self._window = None
        self._message = None
        self._answer = None
        self.is_api_key_valid = chatgpt.ChatGptConnector.is_api_key_initiated()
        button_image_play = b"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAQAAADZc7J/AAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6\
        AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QA/4ePzL8AAAAJcEhZcwAACxgAAAsYAYmptRAAAAAHdElNRQfnBAEXERtKfB82AAACFUlEQVRIx+3USUjU\
        YRjH8c/MqKMNtrmjtkmUEpV1aRHCKA06COGpQ8ulc1TQQahLRR0i6maEly51sCK6RgtB0YJY0YpFStgiSblh89fpUAhjf2061+/2Pu/zfJ/n4eF5CFfEEif\
        1SEn56KxaUX+lNW5I6vPIfb0CDzWKZB6+yE1J7TYpV6ZOmxGdajMNj2oRuKR8wjJXqzFnxDMDFLrli4Y022rvPLUoLFsYoFK3Z2m2Lq+UKc0MkCPHsO9ptq\
        RhWWEt/OVw/gP+AUBUQtYfI2ISYuGAZVo1TbxSUwA2OGddOGCpZg1ikgI5sifljRsXoE6zleGAbwLF4vp9UGFBGqDcQn0+iSmT8jUc0OOTxUp9dluRnWZN/\
        OTZrspd3eaoMeBteHczXTJiB1Z4bMgp1RJmqHLYF+/UY4t+d8LW+qd2GXFdBZq8EHjpsnZPfNdtt5g5LggcnHr4Ja5JOiFf1Fpt3hgwqNtFm2WLO2DYPVXT\
        TXmD1wYcUYw8NRo0Wi4fs+zXp9e26a9zVLMuo67YquBXqVGz1TtvSK89ctIDfqfFbNRivUEdOr03rtRyqxTocNzVSacuVBHz7HNHv6QxYwLfPHDIkrDip+o\
        npki1VfZKOO2u53oFf879+1QeeGvpdC7h25etRNy4YrmyVRoVlfTRaKYt1DtmtpQslWJ6jIoYcVR7phXkmq9QCuPGlIuIGJQIc/0B0/KQ+d6PyJgAAAAldE\
        VYdGRhdGU6Y3JlYXRlADIwMjMtMDQtMDFUMjA6MTc6MjcrMDM6MDAl78HIAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIzLTA0LTAxVDIwOjE3OjI3KzAzOjAwV\
        LJ5dAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAAASUVORK5CYII="
        button_image_api_key = b"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"
        sg.theme('DarkAmber')  # Add a touch of color
        # All the stuff inside your window.
        layout = [[sg.Text("Press 'listen' to start talking with ChatGPT")],
                  [sg.Multiline(default_text=self._update_output(), size=(100, 10), key='-INPUT-', disabled=True)],
                  [sg.Button(image_data=button_image_play, key='listen',
                             button_color=sg.theme_background_color(),border_width=0),
                   sg.Button(image_data=button_image_api_key, key='upload-key',
                             button_color=sg.theme_background_color(), border_width=0)]]

        # Create the Window
        self._window = sg.Window('TalkGpT', layout, layout, enable_close_attempted_event=True,
                                 location=sg.user_settings_get_entry('-location-', (None, None)))

    def _update_output(self):
        if not self.is_api_key_valid:
            output = "Please set Open Ai API KEY."
        elif self._message is None and self._answer is None:
            output = "Waiting for input."
        else:
            output = f"Message: \n{self._message} \n\n\n" \
                           f"ChatGpt answer: \n{self._answer}"

        return output

    def _analyze(self):
        if self.is_api_key_valid:
            message: Union[str, Any]
            message, is_success = Analyzer.speech2text()
            self._message = message
            self._window['-INPUT-'].update(value=self._update_output())
            self._answer = Analyzer.ask_gpt(message)
            self._window['-INPUT-'].update(value=self._update_output())
            self._answer = Analyzer.text2speech(self._answer)
            self._window['-INPUT-'].update(value=self._update_output())
        else:
            logging.error("open ai key was not set")

    def _set_api_key(self):
        api_key = sg.popup_get_text('Enter your api key:')
        chatgpt.ChatGptConnector.set_api_key(api_key)
        self.is_api_key_valid = True

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
            elif event == 'upload-key':
                self._set_api_key()



        self._window.close()
