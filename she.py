#!/usr/bin/env python3
"""
SHEHARA - Python Voice Assistant
A simple but functional voice assistant in a single file
"""

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import sys
import subprocess
import json
import requests
import random
import wikipedia
import pyjokes
import time
import threading
from pygame import mixer
import urllib.parse

class Shehara:
    def __init__(self):
        """Initialize Shehara Voice Assistant"""
        print("""
        ╔══════════════════════════════════════════╗
        ║         SHEHARA VOICE ASSISTANT          ║
        ║            Initializing...               ║
        ╚══════════════════════════════════════════╝
        """)
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.setup_voice()
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        
        # Assistant properties
        self.name = "Shehara"
        self.user_name = "User"
        self.is_listening = True
        
        # Greeting messages
        self.greetings = [
            "Hello! I'm Shehara, your voice assistant.",
            "Hi there! Shehara at your service.",
            "Greetings! I'm Shehara, ready to help.",
            "Hello! Shehara here. How can I assist you today?"
        ]
        
        # Commands mapping
        self.commands = {
            'time': self.get_time,
            'date': self.get_date,
            'search': self.search_web,
            'open': self.open_website,
            'play': self.play_music,
            'joke': self.tell_joke,
            'weather': self.get_weather,
            'news': self.get_news,
            'calculate': self.calculate,
            'wiki': self.search_wikipedia,
            'reminder': self.set_reminder,
            'shutdown': self.shutdown_assistant,
            'help': self.show_help,
            'stop': self.stop_listening
        }
        
        # Websites mapping
        self.websites = {
            'youtube': 'https://youtube.com',
            'google': 'https://google.com',
            'github': 'https://github.com',
            'facebook': 'https://facebook.com',
            'twitter': 'https://twitter.com',
            'instagram': 'https://instagram.com',
            'linkedin': 'https://linkedin.com',
            'gmail': 'https://gmail.com',
            'amazon': 'https://amazon.com',
            'netflix': 'https://netflix.com'
        }
        
        # Music directory (change this to your music folder)
        self.music_dir = os.path.join(os.path.expanduser("~"), "Music")
        
        # Initialize pygame mixer for music
        try:
            mixer.init()
        except:
            print("Music playback may not work properly")
        
        print(f"{self.name}: Initialization complete!")
        self.speak("Initialization complete!")
    
    def setup_voice(self):
        """Configure the voice settings"""
        voices = self.engine.getProperty('voices')
        
        # Try to set a female voice if available
        for voice in voices:
            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        else:
            # Use the default voice
            pass
        
        # Set speech rate and volume
        self.engine.setProperty('rate', 180)  # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"{self.name}: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Listen for voice commands using microphone"""
        with sr.Microphone() as source:
            print("\n" + "─" * 50)
            print(f"{self.name}: Listening... (Say 'Shehara' to activate)")
            print("─" * 50)
            
            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                command = self.recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")
                return command
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                print(f"{self.name}: Sorry, I didn't catch that.")
                return None
            except sr.RequestError as e:
                print(f"{self.name}: Could not request results; {e}")
                return None
    
    def process_command(self, command):
        """Process the voice command"""
        if not command:
            return False
        
        # Check if user called Shehara
        if self.name.lower() in command:
            command = command.replace(self.name.lower(), "").strip()
            self.speak("Yes? How can I help you?")
            return True
        
        # Process specific commands
        command_lower = command.lower()
        
        # Check for greetings
        if any(greet in command_lower for greet in ['hello', 'hi', 'hey', 'greetings']):
            greeting = random.choice(self.greetings)
            self.speak(greeting)
            return True
        
        # Check for user name
        if 'my name is' in command_lower:
            name = command_lower.split('my name is')[-1].strip()
            self.user_name = name.capitalize()
            self.speak(f"Nice to meet you, {self.user_name}!")
            return True
        
        # Check for 'what is your name'
        if any(phrase in command_lower for phrase in ['what is your name', 'who are you', 'your name']):
            self.speak(f"My name is {self.name}, your personal voice assistant.")
            return True
        
        # Process command categories
        for key in self.commands:
            if key in command_lower:
                self.commands[key](command_lower)
                return True
        
        # If no command matched
        self.speak("I'm not sure how to help with that. Try saying 'help' for available commands.")
        return False
    
    def get_time(self, command=""):
        """Get current time"""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The current time is {current_time}")
    
    def get_date(self, command=""):
        """Get current date"""
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        self.speak(f"Today's date is {current_date}")
    
    def search_web(self, command):
        """Search the web"""
        if 'search for' in command:
            query = command.split('search for')[-1].strip()
        elif 'search' in command:
            query = command.split('search')[-1].strip()
        else:
            query = command.replace('search', '').strip()
        
        if query:
            url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            webbrowser.open(url)
            self.speak(f"Searching the web for {query}")
        else:
            self.speak("What would you like me to search for?")
    
    def open_website(self, command):
        """Open a website"""
        for site, url in self.websites.items():
            if site in command:
                webbrowser.open(url)
                self.speak(f"Opening {site}")
                return
        
        # If no known website found
        if 'open' in command:
            website = command.split('open')[-1].strip()
            if website:
                url = f"https://{website}.com"
                try:
                    webbrowser.open(url)
                    self.speak(f"Opening {website}")
                except:
                    self.speak(f"Sorry, I couldn't open {website}")
            else:
                self.speak("Which website would you like me to open?")
    
    def play_music(self, command=""):
        """Play music from the music directory"""
        if not os.path.exists(self.music_dir):
            self.speak("Music directory not found. Please set your music folder path.")
            return
        
        music_files = [f for f in os.listdir(self.music_dir) 
                      if f.endswith(('.mp3', '.wav', '.m4a', '.flac'))]
        
        if not music_files:
            self.speak("No music files found in your music directory.")
            return
        
        # Play random music
        random_music = random.choice(music_files)
        music_path = os.path.join(self.music_dir, random_music)
        
        try:
            mixer.music.load(music_path)
            mixer.music.play()
            self.speak(f"Playing {os.path.splitext(random_music)[0]}")
            
            # Create a thread to wait for music to finish
            def wait_for_music():
                while mixer.music.get_busy():
                    time.sleep(1)
            
            threading.Thread(target=wait_for_music, daemon=True).start()
        except Exception as e:
            self.speak(f"Sorry, I couldn't play the music. Error: {str(e)}")
    
    def stop_music(self):
        """Stop currently playing music"""
        if mixer.music.get_busy():
            mixer.music.stop()
            self.speak("Music stopped")
    
    def tell_joke(self, command=""):
        """Tell a joke"""
        try:
            joke = pyjokes.get_joke()
            self.speak(joke)
        except:
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the scarecrow win an award? He was outstanding in his field!",
                "What do you call a bear with no teeth? A gummy bear!",
                "Why don't eggs tell jokes? They'd crack each other up!"
            ]
            self.speak(random.choice(jokes))
    
    def get_weather(self, command=""):
        """Get weather information"""
        # You need to get a free API key from openweathermap.org
        # Replace 'YOUR_API_KEY' with your actual API key
        api_key = "YOUR_API_KEY"  # Get from https://openweathermap.org/api
        
        if api_key == "YOUR_API_KEY":
            self.speak("Weather service is not configured. Please get an API key from openweathermap.org")
            return
        
        # Default city (change as needed)
        city = "London"
        
        if 'in' in command:
            # Try to extract city from command
            parts = command.split('in')
            if len(parts) > 1:
                city = parts[-1].strip()
        
        try:
            base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(base_url)
            data = response.json()
            
            if data["cod"] != "404":
                main = data["main"]
                temperature = main["temp"]
                humidity = main["humidity"]
                weather_desc = data["weather"][0]["description"]
                
                self.speak(f"The temperature in {city} is {temperature} degrees Celsius. "
                          f"Humidity is {humidity} percent. The weather is {weather_desc}.")
            else:
                self.speak(f"Sorry, I couldn't find weather information for {city}.")
        except Exception as e:
            self.speak("Sorry, I couldn't fetch weather information at the moment.")
    
    def get_news(self, command=""):
        """Get latest news headlines"""
        # Using NewsAPI (get free API key from newsapi.org)
        api_key = "YOUR_API_KEY"  # Get from https://newsapi.org
        
        if api_key == "YOUR_API_KEY":
            self.speak("News service is not configured. Please get an API key from newsapi.org")
            return
        
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
            response = requests.get(url)
            data = response.json()
            
            if data["status"] == "ok":
                articles = data["articles"][:5]  # Get top 5 headlines
                self.speak("Here are the latest news headlines:")
                
                for i, article in enumerate(articles, 1):
                    title = article["title"]
                    self.speak(f"Headline {i}: {title}")
                    time.sleep(1)
            else:
                self.speak("Sorry, I couldn't fetch news at the moment.")
        except Exception as e:
            self.speak("Sorry, I couldn't fetch news at the moment.")
    
    def calculate(self, command):
        """Perform simple calculations"""
        try:
            # Extract mathematical expression
            if 'calculate' in command:
                expression = command.split('calculate')[-1].strip()
            elif 'what is' in command:
                expression = command.split('what is')[-1].strip()
            else:
                expression = command
            
            # Replace words with symbols
            expression = (expression.replace('plus', '+')
                         .replace('add', '+')
                         .replace('minus', '-')
                         .replace('subtract', '-')
                         .replace('times', '*')
                         .replace('multiply', '*')
                         .replace('divided by', '/')
                         .replace('divide', '/')
                         .replace('to the power of', '**')
                         .replace('power', '**'))
            
            # Remove any non-math characters
            import re
            expression = re.sub(r'[^0-9+\-*/().\s]', '', expression)
            
            if expression:
                result = eval(expression)
                self.speak(f"The result is {result}")
            else:
                self.speak("I couldn't understand the calculation.")
        except:
            self.speak("Sorry, I couldn't perform that calculation.")
    
    def search_wikipedia(self, command):
        """Search Wikipedia"""
        if 'wikipedia' in command or 'wiki' in command:
            query = command.replace('wikipedia', '').replace('wiki', '').replace('search', '').strip()
            
            if query:
                try:
                    summary = wikipedia.summary(query, sentences=2)
                    self.speak(f"According to Wikipedia: {summary}")
                except wikipedia.exceptions.DisambiguationError as e:
                    self.speak("There are multiple results. Please be more specific.")
                except wikipedia.exceptions.PageError:
                    self.speak(f"Sorry, I couldn't find information about {query} on Wikipedia.")
                except:
                    self.speak("Sorry, I couldn't access Wikipedia at the moment.")
            else:
                self.speak("What would you like me to search on Wikipedia?")
    
    def set_reminder(self, command):
        """Set a simple reminder"""
        self.speak("Reminder feature is currently under development.")
        self.speak("For now, I suggest using your phone or calendar app for reminders.")
    
    def shutdown_assistant(self, command=""):
        """Shutdown the assistant"""
        self.speak("Shutting down. Goodbye!")
        print(f"\n{self.name}: Shutting down...")
        self.is_listening = False
    
    def show_help(self, command=""):
        """Show available commands"""
        help_text = """
        Here are the commands I understand:
        - Say my name 'Shehara' to activate me
        - Greetings like 'hello', 'hi'
        - 'What time is it?' or 'Tell me the time'
        - 'What is today's date?'
        - 'Search for [something]' to search the web
        - 'Open [website]' to open a website
        - 'Play music' to play random music
        - 'Tell me a joke'
        - 'What's the weather?' or 'Weather in [city]'
        - 'Get news' for latest headlines
        - 'Calculate [expression]' for calculations
        - 'Wikipedia [topic]' to search Wikipedia
        - 'Help' to show this message
        - 'Stop' or 'Goodbye' to shut me down
        """
        print(help_text)
        self.speak("I've displayed the available commands on screen.")
    
    def stop_listening(self, command=""):
        """Stop listening temporarily"""
        self.speak("I'll stop listening now. Say my name to activate me again.")
        print(f"\n{self.name}: Waiting for activation...")
    
    def run(self):
        """Main loop to run the voice assistant"""
        # Initial greeting
        greeting = random.choice(self.greetings)
        self.speak(greeting)
        
        # Main interaction loop
        while self.is_listening:
            command = self.listen()
            
            if command:
                # Check for exit commands
                if any(exit_cmd in command for exit_cmd in ['exit', 'quit', 'goodbye', 'bye', 'stop']):
                    self.shutdown_assistant()
                    break
                
                # Process the command
                self.process_command(command)
            
            # Small delay to prevent CPU overuse
            time.sleep(0.1)
        
        print(f"\n{self.name} has been shut down. Have a great day!")

# Installation helper function
def check_and_install_dependencies():
    """Check and install required packages"""
    required_packages = [
        'speechrecognition',
        'pyttsx3',
        'pygame',
        'wikipedia',
        'pyjokes',
        'requests'
    ]
    
    import importlib
    import subprocess
    import sys
    
    print("Checking dependencies...")
    
    for package in required_packages:
        try:
            # Special handling for packages with different import names
            if package == 'speechrecognition':
                importlib.import_module('speech_recognition')
            else:
                importlib.import_module(package)
            print(f"✓ {package} is already installed")
        except ImportError:
            print(f"✗ {package} is not installed. Installing...")
            try:
                # Install using pip
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✓ Successfully installed {package}")
            except subprocess.CalledProcessError:
                print(f"✗ Failed to install {package}")
                print(f"Please install it manually using: pip install {package}")
    
    print("\n" + "="*50)
    print("Dependency check complete!")
    print("="*50 + "\n")

# Main execution
if __name__ == "__main__":
    # Display banner
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                   SHEHARA VOICE ASSISTANT                ║
    ║                     Version 1.0                          ║
    ║                                                          ║
    ║  A simple voice assistant created with Python            ║
    ║                                                          ║
    ║  Commands:                                               ║
    ║    • Say 'Shehara' to activate                           ║
    ║    • 'Help' for list of commands                         ║
    ║    • 'Stop' or 'Goodbye' to exit                         ║
    ║                                                          ║
    ║  Make sure your microphone is connected and working!     ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Ask if user wants to check dependencies
    response = input("Do you want to check and install dependencies? (y/n): ").lower()
    if response == 'y':
        check_and_install_dependencies()
    
    # Create and run Shehara
    try:
        shehara = Shehara()
        
        # Ask for user name
        print("\n" + "─" * 50)
        name_response = input("What's your name? (Press Enter to skip): ").strip()
        if name_response:
            shehara.user_name = name_response.capitalize()
            shehara.speak(f"Nice to meet you, {shehara.user_name}!")
        
        # Start the assistant
        input("\nPress Enter to start Shehara...")
        shehara.run()
        
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please check your microphone and try again.")
    
    print("\nThank you for using Shehara Voice Assistant!")