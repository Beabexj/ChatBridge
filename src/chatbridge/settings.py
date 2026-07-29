import tkinter as tk
from tkinter import ttk
from chatbridge.config import load_config, save_config
from chatbridge.widgets import create_labeled_combobox, create_labeled_checkbox

LANGUAGES = {
    "English": "en",
    "Thai": "th",
    "Japanese": "ja"
}
LANGUAGES_REVERSE = {v: k for k, v in LANGUAGES.items()}

HOTKEYS = [f"F{i}" for i in range(1, 13)] + ["Ctrl+Shift+T", "Alt+T"]

class SettingsWindow:
    def __init__(self, on_save_callback=None):
        self.on_save_callback = on_save_callback
        self.config = load_config()
        
        self.root = tk.Tk()
        self.root.title("ChatBridge Settings")
        self.root.geometry("320x250")
        self.root.resizable(False, False)
        
        # Center window
        self.root.eval('tk::PlaceWindow . center')
        
        # Main padding frame
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Hotkey
        _, self.cb_hotkey = create_labeled_combobox(
            main_frame, "Hotkey", HOTKEYS, self.config.get("hotkey", "F8")
        )
        
        # Target Lang
        current_lang = self.config.get("target_lang", "en")
        current_lang_name = LANGUAGES_REVERSE.get(current_lang, "English")
        _, self.cb_lang = create_labeled_combobox(
            main_frame, "Target Lang", list(LANGUAGES.keys()), current_lang_name
        )
        
        # Checkboxes
        _, self.var_auto_send = create_labeled_checkbox(
            main_frame, "Auto Send (Press Enter)", self.config.get("auto_send", False)
        )
        
        _, self.var_startup = create_labeled_checkbox(
            main_frame, "Start with Windows", self.config.get("start_with_windows", False)
        )
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=15)
        
        btn_save = ttk.Button(btn_frame, text="Save", command=self.save_settings)
        btn_save.pack(side=tk.LEFT, expand=True, padx=5)
        
        btn_cancel = ttk.Button(btn_frame, text="Cancel", command=self.root.destroy)
        btn_cancel.pack(side=tk.RIGHT, expand=True, padx=5)

    def save_settings(self):
        # Update config dictionary
        self.config["hotkey"] = self.cb_hotkey.get()
        self.config["target_lang"] = LANGUAGES.get(self.cb_lang.get(), "en")
        self.config["auto_send"] = self.var_auto_send.get()
        self.config["start_with_windows"] = self.var_startup.get()
        
        # Save to file
        save_config(self.config)
        
        # Callback if defined
        if self.on_save_callback:
            self.on_save_callback(self.config)
            
        self.root.destroy()
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SettingsWindow()
    app.run()
