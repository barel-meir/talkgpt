import threading
import PySimpleGUI as sg
from analyzer import Analyzer

button_image_play = b'iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAABmJLR0QA/wD/AP+gvaeTAAAByElEQVRoge3ZMWsUQRjG8Z8RFSKCgoJp0qSJjVpoZ2clkk8g5CtYpU+TD5DSUkvbVCFNYiM2dhZqY6GFQooEISGai8Xu4HgmcnM3c+su+4fj2L2dmedhb+Z95x16enp6hljBxaZF5OAE7/GoaSGTchJ9tnCrWTnjE0zs19+HWMPlJkWNQzAyh2c4rq+/YBnnmpOWRjASuIfX0f0d3GlAVzLDRmBG9Ta+1r8d4wVuTFdaGqcZCVzFOn7Uz+ziKc5PR1oa/zISWMRm9OxbPCisK5lRjASW8Clqs4H5MrLSSTECs1jFQd3ue319KbewVFKNBBbwMmr/EY8z6kpmXCOBh3gX9dNYdjCpEbigWs326r6OVKvdlQn7TSKHkcCcKt4MNJAd5DQSuI83Ud87uJ15jL8oYYTf2cE3f2YH1wuMhXJGAtdU8+WnwtlBaSOBu3gVjZc9O5iWEapJ/wSf6zEHeI6bZzWYmY6u/4v+rzUirZ/snVh+hwPitpYFxNanKJ1IGk9L4xcz6Eom18bqg5ZtrDqx1Y2LDwPVG2lV8aH15aDWF+jOKpkWi8o5GKWIXTwq56BzxwqdOejpxNFbJw5DO3M83dPT02J+AbN50HbYDxzCAAAAAElFTkSuQmCC'
_message = _answer = _is_success = None


def analyze():
    global _message
    global _answer
    global _is_success

    message, is_success = Analyzer.speech2text()
    _message = message
    _is_success = is_success
    _answer = Analyzer.text2speech(message)


def run():
    sg.theme('DarkAmber')  # Add a touch of color
    # All the stuff inside your window.
    layout = [[sg.Text("Press 'listen' to start talking with ChatGPT")],
              [sg.Multiline(default_text='', size=(50, 10), key='-INPUT-', disabled=True)],
              [sg.Button(image_data=button_image_play, key='listen', button_color=sg.theme_background_color(),
                         border_width=0)]]

    # Create the Window
    window = sg.Window('TalkGpT', layout, layout, enable_close_attempted_event=True,
                       location=sg.user_settings_get_entry('-location-', (None, None)))
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in ('Exit', sg.WINDOW_CLOSE_ATTEMPTED_EVENT):
            sg.user_settings_set_entry('-location-',
                                       window.current_location())  # The line of code to save the position before exiting
            break
        if event == 'listen':
            thread1 = threading.Thread(target=analyze)
            thread1.start()
            # thread1.join()
            window['-INPUT-'].update(value=f"Message: \n{_message} \nChatGpt answer: \n{_answer}")

        # print('You entered ', values[0])

    window.close()
