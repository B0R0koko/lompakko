# Main kivy imports
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, FadeTransition

# Main screens import
from src.screens.wallet_screen import WalletScreen
from src.screens.exchange_screen import ExchangeScreen
from src.screens.settings_screen import SettingScreen
from src.screens.option_screen import OptionScreen
from src.screens.summary_screen import SummaryScreen
from src.screens.asset_screen import AssetScreen

import kivymd_extensions.akivymd
import json


# All screens present in the app
SCREENS = [
    "walletscreen",
    "exchangescreen",
    "settingscreen",
    "optionscreen",
    "summaryscreen",
    "assetscreen",
]


Window.size = (414, 896)
# Window.borderless = True

LabelBase.register(
    name="raleway",
    fn_regular="props/fonts/raleway.ttf",
    fn_italic="props/fonts/raleway_italic.ttf",
    fn_bold="props/fonts/raleway_bold.ttf",
    fn_bolditalic="props/fonts/raleway_bold_italic.ttf",
)


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = FadeTransition(duration=0.1)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = [{"Python": 40, "Java": 30, "C++": 10, "PHP": 8, "Ruby": 12}]
        self.user_cfg = self.read_json("config/pref.json")  # Load user config
        self.app_cfg = self.read_json("config/assets.json")  # Load application props

    # Build application layout
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.accent_palette = "Purple"

        for screen in SCREENS:  # Load all defined screens into the builder
            Builder.load_file(f"styles/{screen}.kv")
        return Builder.load_file("styles/main.kv")

    def read_json(self, path):
        with open(path, "r") as file:
            data = json.load(file)
        return data

    # Commit changes pref.json file
    def save_cfg(self):
        with open("config/pref.json", "w") as file:
            json.dump(self.user_cfg, file)


if __name__ == "__main__":
    MainApp().run()
