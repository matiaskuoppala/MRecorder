from pynput import keyboard, mouse
from pynput.keyboard import Key
from pynput.mouse import Button
import time
import os


# Records keyboard and mouse actions into a .txt
class Recorder():

    def __init__(self):
        self.actions = []
        self.holding_key = []
        self.holding_mouse = []
        self.m_listener = mouse.Listener(on_click=self.on_click)
        self.recording = False
        print("Press 'r' again to start recording. Press esc to stop recording.")

    # Format action times into intervals between each action.
    # Exclude the last action which is always pressing esc.
    def format_times(self):
        length = len(self.actions)
        actions_formatted = []
        for i in range(len(self.actions) - 1):
            cur_time = self.actions[i][1]
            next_time = self.actions[i + 1][1]
            actions_formatted.append((self.actions[i][0], next_time - cur_time))
        return actions_formatted

    def on_press(self, key):
        if key not in self.holding_key and self.recording:
            self.actions.append(("self.keyboard.press("+str(key)+")", time.time()))
            self.holding_key.append(key)

    def on_release(self, key):
        # Stop and save when esc pressed
        if key == keyboard.Key.esc:
            self.m_listener.stop()
            print("Recording finished.")
            return False
        elif not self.recording:
            if key == keyboard.KeyCode.from_char('r'):
                self.recording = True
        elif self.recording:
            if key in self.holding_key:
                self.holding_key.remove(key)
            self.actions.append(("self.keyboard.release("+str(key)+")", time.time()))

    def on_click(self, x, y, button, pressed):
        if self.recording:
            if pressed:
                if button in self.holding_mouse:
                    pass
                else:
                    self.holding_mouse.append(button)
                    self.actions.append(("self.mouse.press("+str(button)+")", time.time()))
            else:
                if button in self.holding_mouse:
                    self.holding_mouse.remove(button)
                    self.actions.append(("self.mouse.release("+str(button)+")", time.time()))
            

    def run(self):
        self.m_listener.start()
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as k_listener:
            k_listener.join()

        actions_formatted = self.format_times()
        self.save(actions_formatted)

    # Save action list into txt
    def save(self, actions):
        name = input("Enter macro name: ") + ".txt"
        if name in os.listdir(os.getcwd()):
            print("A macro named " + name + " already exists.")
            choice = input("Do you want to overwrite (y/n)?")
            if (choice == "n"):
                self.save(actions)
        f = open(name, "w")
        print("Saving macro..")
        
        for action in actions:
            for a in action:
                f.write(str(a))
                f.write(',')
            f.write('\n')    
        print("Macro saved as " + name + ".")


# Plays a macro from a txt file.
class Player():

    def __init__(self, file):
        self.keyboard = keyboard.Controller()
        self.mouse = mouse.Controller()
        self.macro = file

        print("Press 'p' again to play macro.")
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as k_listener:
            k_listener.join()

    def on_press(self, key):
        pass

    def on_release(self, key):
        if key == keyboard.KeyCode.from_char('p'):
           self.play()
           return False

    def play(self):
        for line in self.macro:
            action = tuple(line.strip().split(','))
            print(action)
            print(action[0])
            eval(action[0])
            time.sleep(float(action[1]))
        

# Program entry point
if __name__ == "__main__":
    while True:
        action = input("Record macro ('r') or play macro ('p')? : ")
        if action == 'r':
            recorder = Recorder()
            recorder.run()
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
                        chosen = True
                    except FileNotFoundError as e:
                        print(e)
