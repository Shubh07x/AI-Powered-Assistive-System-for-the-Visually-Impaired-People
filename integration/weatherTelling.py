import requests
import pyttsx3
import speech_recognition as sr
from googletrans import Translator
from num2words import num2words
def get_weather(city, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "imperial"
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            temperature_fahrenheit = data["main"]["temp"]
            temperature_celsius = round((temperature_fahrenheit - 32) * 5 / 9)
            weather_description = data["weather"][0]["description"]
            city_name = data["name"]

            umbrella_suggestion = ""
            if "rain" in weather_description.lower():
                umbrella_suggestion = " It's raining, so don't forget to take an umbrella if you're going outside."

            return f"The current weather in {city_name} is {weather_description} with a temperature of {temperature_celsius} degrees Celsius.{umbrella_suggestion}"
        else:
            return f"Error fetching weather data: {data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"An error occurred: {e}"


def speak_weather(weather_info,engine):
    engine.setProperty('rate', 150)


    engine.say(weather_info)
    engine.runAndWait()

def convert_numbers_to_words(text):
    """
    Convert any numeric digits in the text to their word equivalents.

    :param text: The input string with numbers
    :return: The string with numbers converted to words
    """
    words = text.split()
    converted_text = []

    for word in words:
        if word.isdigit():
            word = num2words(int(word), lang='en')
        converted_text.append(word)

    return ' '.join(converted_text)
def get_city_from_mic(engine,ask,sorry):
    engine.setProperty('rate', 150)
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source)
            city = recognizer.recognize_google(audio)
            print(f"You said: {city}")
            return city
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
            engine.say(sorry)
            engine.runAndWait()
            return None
        except sr.RequestError as e:
            print(f"Could not request results from the speech recognition service; {e}")
            return None


if __name__ == "__main__":
    api_key = "f86f09eb3cf07d0efca06deadb6df192"
    engine = pyttsx3.init()
    engine.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hiIN_HemantM")
    translator = Translator()
    say = translator.translate("Please tell the city name", dest='mr')
    sorry = translator.translate("Sorry, I couldn't understand the audio.", dest='mr')
    print(say.text)
    engine.say(say.text)
    engine.runAndWait()
    city = get_city_from_mic(engine,say.text,sorry.text)
    # city = "Kolhapur"
    if city:
        weather_info = get_weather(city, api_key)
        print(weather_info)
        newText=convert_numbers_to_words(weather_info)
        translated_text = translator.translate(newText, dest='mr')
        print(translated_text.text)
        speak_weather(translated_text.text,engine)
    else:
        print("City name could not be captured. Please try again.")