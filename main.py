
import speech_recognition as sr  # recognize speech
import time
import webbrowser  # open browser (default browser of computer)
import playsound  # to play an audio file
import os  # to remove created audio files
import random
from random import randint
import ssl
import certifi
from gtts import gTTS  # google text to speech
from time import ctime  # time details


class Person:
    name = ''

    def setName(self, name):
        self.name = name


def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True


r = sr.Recognizer()  # initialize a recognizer


# listen for audio and convert it into text:
def record_audio(ask=False):
    with sr.Microphone() as source:  # microphone is source
        if ask:
            adonis_speak(ask)
        audio = r.listen(source)  # listen for audio thru source
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)  # convert audio to text
        except sr.UnknownValueError:  # error; recognizer doesn't understand
            adonis_speak("Sorry, I didn't catch that")
        except sr.RequestError: # error; recognizer is not connected
            adonis_speak("Sorry, speech service is down")
        print(f">> {voice_data.lower()}")  # print what user said
        return voice_data.lower()


# get string and create an audio file to be played
def adonis_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')  # text to speech
    r = random.randint(1, 20000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)  # save as an mp3
    playsound.playsound(audio_file)  # play audio file
    print(audio_string)  # print what has been said
    os.remove(audio_file)  # remove audio file


def respond(voice_data):
    # 1: greeting
    if there_exists(['hey', 'hi', 'hello']):
        greetings = [f"hey, how can I help you {person_obj.name}", f"hey, what's up? {person_obj.name}",
                     f"I'm listening {person_obj.name}", f"how can I help you? {person_obj.name}",
                     f"hello {person_obj.name}"]
        greet = greetings[random.randint(0, len(greetings) - 1)]
        adonis_speak(greet)

    # 2: name
    if there_exists(["what is your name", "what's your name", "tell me your name"]):
        if person_obj.name:
            adonis_speak("My amazingly beautiful name is Adonis")
        else:
            adonis_speak("My name is Adonis. What's your name?")

    if there_exists(["my name is"]):
        person_name = voice_data.split("is")[-1].strip()
        adonis_speak(f"okay, i will remember that {person_name}")
        person_obj.setName(person_name)  # remember name in person object

    # 3: greeting two
    if there_exists(['how are you', 'how are you doing']):
        adonis_speak(f"I'm very well, thanks for asking {person_obj.name}")

    # 4: time
    if there_exists(["what time is it", "what's the time", "tell me the time and date"]):
        time = ctime()
        adonis_speak(time)

    # 5: search google
    if there_exists(["search for"]) and 'youtube' not in voice_data:
        search_term = voice_data.split("for")[-1]
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        adonis_speak(f'Here is what I found for {search_term} on google')

    # 6: search youtube
    if there_exists(["youtube"]):
        search_term = voice_data.split("for")[-1]
        url = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        adonis_speak(f'Here is what I found for {search_term} on youtube')

    # 7: location
    if there_exists(['find location for']):
        search_term = voice_data.split("for")[1]
        url = f"https://google.nl/maps/place/{search_term}/&amp;"
        webbrowser.get().open(url)
        adonis_speak(f"Here is the location of {search_term}")

    # 8: flip a coin
    if there_exists(["toss", "flip", "coin"]):
        moves = ["head", "tails"]
        computer_move = random.choice(moves)
        adonis_speak("The computer chose " + computer_move)

    # 9: game (rock-paper-scissors)
    if there_exists(["Let's play"]):
        voice_data = record_audio("choose among rock paper or scissor")
        moves = ["rock", "paper", "scissor"]

        computer_move = moves[randint(0, 2)]
        player_move = voice_data

        adonis_speak("The computer chose " + computer_move)
        adonis_speak("You chose " + player_move)
        # engine_speak("hi")
        if player_move == computer_move:
            adonis_speak("the match is draw")
        elif player_move == "rock" and computer_move == "scissor":
            adonis_speak("Player wins")
        elif player_move == "rock" and computer_move == "paper":
            adonis_speak("Computer wins")
        elif player_move == "paper" and computer_move == "rock":
            adonis_speak("Player wins")
        elif player_move == "paper" and computer_move == "scissor":
            adonis_speak("Computer wins")
        elif player_move == "scissor" and computer_move == "paper":
            adonis_speak("Player wins")
        elif player_move == "scissor" and computer_move == "rock":
            adonis_speak("Computer wins")

    # 10: quit
    if there_exists(['exit', 'quit', 'goodbye']):
        adonis_speak(f"Going offline, goodbye {person_obj.name}")
        exit()

time.sleep(1)
person_obj = Person()
while 1:
    voice_data = record_audio()  # get voice input
    respond(voice_data)  # respond

