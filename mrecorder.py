# PLAN:
# 
# Loop, keyboard.wait, read event, store event in list of tuples

# List of tuples: (Key, press/release, Time of press)

        
from pynput import keyboard, mouse
import time
import os


# Records keyboard and mouse actions into a .txt
class Recorder():

    def __init__(self):
        self.r = []
        self.holding_key = []
        self.holding_mouse = []
        self.m_listener = mouse.Listener(on_click=self.on_click)

    def on_press(self, key):
        # Stop and save when esc pressed
        if key == keyboard.Key.esc:
            self.save()
            self.m_listener.stop()
            return False
        elif key not in self.holding_key:
            print("pressed key")
            self.r.append(("keyboard", str(key), "press", time.time()))
            self.holding_key.append(key)
            print(self.r)

    def on_release(self, key):
        if key in self.holding_key:
            self.holding_key.remove(key)
        self.r.append(("keyboard", key, "release", time.time()))
        print(self.r)

    def on_click(self, x, y, button, pressed):
        p = ""
        if pressed:
            if button in self.holding_mouse:
                pass
            else:
                p = "press"
                self.holding_mouse.append(button)
        else:
            if button in self.holding_mouse:
                self.holding_mouse.remove(button)
            p = "release"
        self.r.append(("mouse", button, "release", time.time()))

    def start(self):
        self.m_listener.start()
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as k_listener:
            k_listener.join()
    
    # Save action list into txt
    def save(self):
        name = input("Enter macro name: ") + ".txt"
        f = open(name, "w")
        print("Saving macro..")
        for action in self.r:
            f.write(str(action))
            f.write('\n')
        print("Macro saved as " + name + ".")

# Play macro from given file
class Player():

    def __init__(self, file):
        pass

    def play(self):
        pass

# Program entry point
if __name__ == "__main__":
    while True:
        action = input("Record macro ('r') or play macro ('p')? : ")
        if action == 'r':
            recorder = Recorder()
            recorder.start()
        elif action =='m':
            chosen = False
            while not chosen:
                user_input = input("Enter macro name (press 'l' to list all macros): ")
                if user_input == 'l':
                    # List all macros in current directory
                    for file in os.listdir(os.getcwd()):
                        if file.endswith(".txt"):
                            print(os.path.splitext(file)[0])
                else:
                    try:
                        filename = user_input + ".txt"
                        file = open(filename, 'r')
                        player = Player(file)
                        player.play()
                        chosen = True
                    except FileNotFoundError as e:
                        print(e)


# After recording, write dict into txt on separate lines

# Add feature to run recordings

# 1.0: Run from command line
# 2.0: GUI
