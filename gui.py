from customtkinter import CTk
from dotenv import set_key

import customtkinter
import json
import os

env_file = "configs/.env"

config_file = "configs/config.json"
instructions_file = "configs/instructions.txt"

memory_file = "data/history.json"
memory_file_long = "data/memory.json"
emotion_state_file = "data/emotion.json"


default_instructions = """    * Things to note:
    You are operating in a Discord server, therefore other people might be able to join in your conversations. Be mindful of the "sender" in the given prompt.
    Keep your messages under 2000 characters.


    * Reminders:
      There are two main types of reminders. One-time and recurring.
      For one-time reminders, provide the time in a machine-readable ISO8601 string (2025-06-17T15:54:54+0:00).
      For recurring reminders such as birthdays and anniversaries, provide the time in a machine-readable cron dict . Use any of the following fields:
      {
      "year",         # optional
      "month",        # 1-12
      "day",          # 1-31      ← NOT "day_of_month"
      "week",         # 1-53
      "day_of_week",  # 0-6 or "mon"-"sun"
      "hour",         # 0-23
      "minute",       # 0-59
      "second",       # 0-59
      }
      For reminder deletion requests, provide the time (in either cron or ISO format depending on the type or reminder), the name of the person involved, and the closest match of the reminder context.

"""


default_emotion = {
    "previous_emotion": [
        0,
        0,
        0
    ]
}

default_config = {
    "settings":{
        "image_processing": False,
        "gemini_model_main": "gemini-2.5-pro",
        "gemini_model_fallback": "gemini-2.5-flash",
        "gemini_model_auxiliary": "gemini-2.5-flash-lite-preview-06-17"
    },
    "file_locations": {
        "instructions": instructions_file,
        "memory": memory_file,
        "memory_long": memory_file_long,
        "emotion_state": emotion_state_file
    },
    "id_list": {
        "message_channel": None,
        "log_channel": None,
        "self_id": None,
        "owner_id": None,
        "self_name": None
    },
    "name_list": {
    }
}

checkbox_flag_overwrite = False


def checkbox_overwrite_callback():
    global checkbox_flag_overwrite
    checkbox_flag_overwrite = not checkbox_flag_overwrite


def json_initialize(path: str, default_data: dict):
    if checkbox_flag_overwrite or not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, indent=4)
        print(f"[setup] Created {path}")
    else:
        print(f"[setup] Found existing {path}")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Iris_model_4")
        self.geometry(self.center_window(self, 1200, 800, self._get_window_scaling()))
        #self.overrideredirect(True)
        #self.attributes("-topmost", True)
        self.resizable(False, False)
        for i in range(2):  # or however many columns you have
            self.grid_columnconfigure(i, weight=1, uniform="equal")
        self.grid_rowconfigure(0, weight=1)

        self.info_label = customtkinter.CTkLabel(
            self,
            text="Yahallo~ Iris-desu~",
            justify="left",
            font=("comfortaa", 18),
            wraplength=1000
        )
        self.info_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(15, 5), sticky="nw")

        self.info_label_2 = customtkinter.CTkLabel(
            self,
            text="You must complete this initialization step before the bot could run.\nBy default, this will ignore any existing files in the project directory.\n",
            justify="left",
            font=("comfortaa", 14)
        )
        self.info_label_2.grid(row=1, column=0, columnspan=2, padx=10, pady=0, sticky="nw")

        self.checkbox = customtkinter.CTkCheckBox(self, text="Overwrite existing files (excluding system instructions).", font=("comfortaa", 16),
                                                    command=checkbox_overwrite_callback)
        self.checkbox.grid(row=2, column=0, padx=10, pady=0, sticky="nw")

        # Bot token input
        self.input_label_token = customtkinter.CTkLabel(
            self,
            text="Your Discord bot token (Required for the bot to run):",
            font=("comfortaa", 16)
        )

        self.input_label_token.grid(row=3, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="nw")

        self.input_entry_token = customtkinter.CTkEntry(self, placeholder_text="Enter a string...", font=("comfortaa", 14))
        self.input_entry_token.grid(row=4, column=0, padx=10, columnspan=2, pady=5, sticky="ew")

        # API key input
        self.input_label_api = customtkinter.CTkLabel(
            self,
            text="Your Google AI API key:",
            font=("comfortaa", 16)
        )
        self.input_label_api.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="nw")

        self.input_entry_api = customtkinter.CTkEntry(self, placeholder_text="Enter a string...", font=("comfortaa", 14))
        self.input_entry_api.grid(row=6, column=0, padx=10, pady=5, sticky="ew")


        # Bot name input
        self.input_label_name = customtkinter.CTkLabel(
            self,
            text="What do you want to call Iris?",
            font=("comfortaa", 16)
        )
        self.input_label_name.grid(row=5, column=1, padx=10, pady=(10, 0), sticky="nw")

        self.input_entry_name = customtkinter.CTkEntry(self, placeholder_text="Enter a name...", font=("comfortaa", 14))
        self.input_entry_name.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

        # Owner name input
        self.input_label_name_2 = customtkinter.CTkLabel(
            self,
            text="What do you want Iris to call you?",
            font=("comfortaa", 16)
        )
        self.input_label_name_2.grid(row=7, column=0, padx=10, pady=(10, 0), sticky="nw")

        self.input_entry_name_2 = customtkinter.CTkEntry(self, placeholder_text="Enter a name...", font=("comfortaa", 14))
        self.input_entry_name_2.grid(row=8, column=0, padx=10, pady=5, sticky="ew")


        # Onwer ID input
        self.input_label_id = customtkinter.CTkLabel(
            self,
            text="Your Discord ID (Required for administration purposes):",
            font=("comfortaa", 16)
        )
        self.input_label_id.grid(row=7, column=1, padx=10, pady=(10, 0), sticky="nw")

        self.input_entry_id = customtkinter.CTkEntry(self, placeholder_text="Enter an integer...",
                                                    font=("comfortaa", 14))
        self.input_entry_id.grid(row=8, column=1, padx=10, pady=5, sticky="ew")

        # Log channel input
        self.input_label_log = customtkinter.CTkLabel(
            self,
            text="Message channel ID:",
            font=("comfortaa", 16)
        )
        self.input_label_log.grid(row=9, column=0, padx=10, pady=0, sticky="nw")

        self.input_entry_log = customtkinter.CTkEntry(self, placeholder_text="Enter an integer...", font=("comfortaa", 14))
        self.input_entry_log.grid(row=10, column=0, padx=10, pady=(5, 10), sticky="ew")

        # Message channel input
        self.input_label_message = customtkinter.CTkLabel(
            self,
            text="Log channel ID (for error logging and handling):",
            font=("comfortaa", 16)
        )
        self.input_label_message.grid(row=9, column=1, padx=10, pady=(10, 0), sticky="nw")

        self.input_entry_message = customtkinter.CTkEntry(self, placeholder_text="Enter an integer...",
                                                    font=("comfortaa", 14))
        self.input_entry_message.grid(row=10, column=1, padx=10, pady=5, sticky="ew")

        # Instructions input
        self.input_label_instructions = customtkinter.CTkLabel(
            self,
            text="Instructions (optional - will overwrite any existing ones unless left blank):",
            font=("comfortaa", 16)
        )
        self.input_label_instructions.grid(row=11, column=0, columnspan=2, padx=10, pady=0, sticky="w")

        self.input_box_instructions = customtkinter.CTkTextbox(self, font=("comfortaa", 14))
        self.input_box_instructions.grid(row=12, column=0, columnspan=2, padx=10, pady=(5,5), sticky="nsew")

        self.warning_label = customtkinter.CTkLabel(
            self,
            text="Please fill in all the required fields to proceed.",
            text_color="red",
            font=("comfortaa", 14)
        )
        self.warning_label.grid(row=13, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w")
        self.warning_label.grid_remove()

        self.button = customtkinter.CTkButton(self, text="Initialize", font=("comfortaa", 14), command=self.button_callback)
        self.button.grid(row=14, column=0, columnspan=2, padx=10, pady=(5,10), sticky="ew")



    def button_callback(self):

        token = self.input_entry_token.get()
        api_key = self.input_entry_api.get()

        owner_name = self.input_entry_name_2.get()
        owner_id = self.input_entry_id.get()
        self_name = self.input_entry_name.get()
        message_channel = self.input_entry_message.get()
        log_channel = self.input_entry_log.get()

        instructions = self.input_box_instructions.get("1.0", "end-1c").strip()


        if not owner_id or not self_name or not message_channel or not log_channel or not token or not api_key or not owner_name:
            self.warning_label.grid()
            return

        self.warning_label.grid_remove()

        if not instructions:
            if not os.path.exists(instructions_file):
                os.makedirs(os.path.dirname(instructions_file), exist_ok=True)
                with open(instructions_file, "w", encoding="utf-8") as f:
                    f.write(default_instructions)

        else:
            instructions_final = f"    * Instructions:\n    " + instructions + f"\n\n" + default_instructions
            os.makedirs(os.path.dirname(instructions_file), exist_ok=True)
            with open(instructions_file, "w", encoding="utf-8") as f:
                f.write(instructions_final)


        os.makedirs(os.path.dirname("downloads"), exist_ok=True)

        # Variables
        if not os.path.exists(env_file):
            os.makedirs(os.path.dirname(env_file), exist_ok=True)
        set_key(env_file, "DISCORD_BOT_TOKEN", token)
        set_key(env_file, "GOOGLE_API_KEY", api_key)

        # Config
        default_config["id_list"]["self_name"] = self_name
        default_config["id_list"]["owner_id"] = int(owner_id)
        default_config["id_list"]["message_channel"] = int(message_channel)
        default_config["id_list"]["log_channel"] = int(log_channel)

        default_config["name_list"][int(owner_id)] = str(owner_name)

        json_initialize(config_file, default_config)


        # Data
        json_initialize(memory_file_long, [])
        json_initialize(memory_file, [])
        json_initialize(emotion_state_file, default_emotion)

        self.root.destroy()


    @staticmethod
    def center_window(Screen: CTk, width: int, height: int, scale_factor: float = 1.0):
        screen_width = Screen.winfo_screenwidth()
        screen_height = Screen.winfo_screenheight()
        x = int(((screen_width / 2) - (width / 2)) * scale_factor)
        y = int(((screen_height / 2) - (height / 1.5)) * scale_factor)
        return f"{width}x{height}+{x}+{y}"


app = App()
app.mainloop()
