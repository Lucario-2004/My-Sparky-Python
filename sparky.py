import speech_recognition as sr
import pyautogui
import datetime
import webbrowser
import os

def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

def process_speech_commands(transcription):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    if "hii lucario" in transcription:
        print("hii lucario. how can i help you?")

    elif "search" in transcription:
        search_query = transcription.replace("search", "")
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        print("searching...")

    elif "time" in transcription:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"the current time is {current_time}")

    elif "open" in transcription:
        app_name = transcription.replace("open", "")
        os.startfile(f"{app_name}.exe")
        print(f"opening {app_name}...")

    elif "navigate" in transcription:
        place = transcription.replace("navigate", "")
        webbrowser.open(f"https://www.google.com/maps/place/{place}")
        print(f"navigating to {place}...")

    elif "activate visual commanding" in transcription:
        print("activating visual commanding...")
        while True:
            x, y = pyautogui.position()
            print(f"cursor position: x={x}, y={y}")

            if pyautogui.locateOnScreen("single_movement_gesture.png", confidence=0.8):
                pyautogui.click()
                print("single click performed")

            elif pyautogui.locateOnScreen("double_movement_gesture.png", confidence=0.8):
                pyautogui.doubleClick()
                print("double click performed")

            else:
                print("no gesture detected")

            if pyautogui.locateOnScreen("stop_visual_commanding.png", confidence=0.8):
                print("stopping visual commanding...")
                break

    else:
        print("unknown command")

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        print("listening...")
        response = recognize_speech_from_mic(recognizer, microphone)

        if response["success"]:
            print(f"transcription: {response['transcription']}")
            process_speech_commands(response["transcription"])
        else:
            print(f"error: {response['error']}")

if __name__ == "__main__":
    main()