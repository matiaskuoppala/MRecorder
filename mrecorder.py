# PLAN:
# 
# Loop, keyboard.wait, read event, store event in list of tuples

# List of tuples: (Key, press/release, Time of press)

        
from pynput import keyboard, mouse
from pynput.keyboard import Key
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
            self.r.append(("keyboard", key, "press", time.time()))
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
        # TODO: Ask "do you want to overwrite?" for already existing files
        for action in self.r:
            for a in action:
                f.write(str(a))
                f.write(',')
            f.write('\n')    
        print("Macro saved as " + name + ".")

# Play macro from given file
class Player():

    def __init__(self, file):
        self.keyboard = keyboard.Controller()
        self.mouse = mouse.Controller()
        self.macro = file

    def play(self):
        prev_time = 0
        for line in self.macro:
            action = tuple(map(str, line.strip().split(',')))
            print(action)
            if action[0] == "keyboard":
                if action[2] == "press":
                    eval("self.keyboard.press(" + action[1] + ")")
                elif action[2] == "release":
                    print(action[1])
                    eval("self.keyboard.release(" + action[1] + ")")
            elif action[0] == "mouse":
                if action[2] == "press":
                    eval("self.mouse.press(" + action[1] + ")")
                elif action[2] == "release":
                    eval("self.mouse.release(" + action[1] + ")")
            if prev_time != 0:
                time.sleep(float(action[3]) - prev_time)
            prev_time = float(action[3])


# Program entry point
if __name__ == "__main__":
    while True:
        action = input("Record macro ('r') or play macro ('p')? : ")
        if action == 'r':
            recorder = Recorder()
            recorder.start()
        elif action =='p':
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

# 1.0: Run from command action
# 2.0: GUI

