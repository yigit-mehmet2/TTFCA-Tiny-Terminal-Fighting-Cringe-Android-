import os
import subprocess
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.textinput import TextInput

Window.softinput_mode = 'below_target'

BANNER = """TTFCA v1.0 (Tiny Terminal Fighting with Cringe Android)
Type 'exit' to quit.
------------------------------------------------------
"""

class SingleTerminalInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = BANNER + f"{os.getcwd()} $ "
        self.protected_len = len(self.text)
        self.cursor = self.get_cursor_from_index(len(self.text))

    def insert_text(self, substring, from_undo=False):
        if self.cursor_index() < self.protected_len:
            self.cursor = self.get_cursor_from_index(len(self.text))
        return super().insert_text(substring, from_undo=from_undo)

    def do_backspace(self, from_undo=False, mode='bkspc'):
        if self.cursor_index() <= self.protected_len:
            return
        super().do_backspace(from_undo=from_undo, mode=mode)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] in ('enter', 'numpadenter'):
            full_text = self.text
            cmd = full_text[self.protected_len:].strip()
            self.text += "\n"
            
            self.process_command(cmd)
            return True
        
        if keycode[1] == 'left' and self.cursor_index() <= self.protected_len:
            return True

        return super().keyboard_on_key_down(window, keycode, text, modifiers)

    def process_command(self, cmd):
        if cmd == "exit":
            App.get_running_app().stop()
            return

        if cmd:
            token = cmd.split()
            try:
                if (len(token) > 1 and token[1] == "~") or cmd == "cd":
                    home_path = os.environ.get("HOME", "/data/data/com.termux/files/home")
                    os.chdir(home_path)
                elif cmd.startswith("cd "):
                    target_dir = cmd[3:].strip()
                    os.chdir(target_dir)
                else:
                    result = subprocess.run(
                        cmd, 
                        shell=True, 
                        capture_output=True, 
                        text=True
                    )
                    if result.stdout:
                        self.text += result.stdout
                    if result.stderr:
                        self.text += result.stderr

            except IndexError:
                self.text += "Error: Missing required argument.\n"
            except FileNotFoundError:
                self.text += "Error: No such file or directory.\n"
            except Exception as e:
                self.text += f"Error: {str(e)}\n"

        new_prompt = f"{os.getcwd()} $ "
        self.text += new_prompt
        self.protected_len = len(self.text)
        self.cursor = self.get_cursor_from_index(len(self.text))


class TTFCAApp(App):
    def build(self):
        return SingleTerminalInput(
            background_color=(0, 0, 0, 1),      
            foreground_color=(1, 1, 1, 1),      
            cursor_color=(1, 1, 1, 1),          
            font_size='14sp',
            multiline=True,
            focus=True
        )

if __name__ == '__main__':
    TTFCAApp().run()
