from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.app import App
from kivy.properties import BooleanProperty
from src.screens.wallet_screen import CoinBox


class OptionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        Clock.schedule_once(lambda *args: self.load_options(), 0.2)

    def load_options(self):
        assets = self.app.app_cfg["assets"]  # Load all available assets
        for id, asset in assets.items():  # Add all of these options to optionscreen.kv
            self.ids.asset_options_container.add_widget(
                AssetOption(
                    id=id,
                    asset_name=asset["name"],
                    asset_short=asset["short"],
                    icon_source=f"props/icons/{asset['name']}.png",
                    attached=self,
                )
            )

    # Function managing changes to assets chosen by the user
    def manage_options(self, checkbox, option):

        wallet = self.manager.get_screen("wallet_screen")

        # If checkbox is active and asset is displayed in wallet menu -> delete it
        if not checkbox.active:
            if option.id in wallet.ids:
                focus_asset = wallet.ids[option.id]
                wallet.ids.asset_container.remove_widget(focus_asset)
                self.app.user_cfg["assets_pref"].remove(option.id)
                del wallet.ids[option.id]

        # Otherwise if it is not displayed already add it to the menu
        else:
            if option.id not in wallet.ids:
                asset = CoinBox(
                    id=option.id,
                    asset_name=option.asset_name,
                    asset_short=option.asset_short,
                    icon_source=option.icon_source,
                )
                wallet.ids.asset_container.add_widget(asset)
                wallet.ids[option.id] = asset
                self.app.user_cfg["assets_pref"].append(option.id)
        self.app.save_cfg()


# BoxLayout defined in optionscreen.kv responsible for asset option layout
class AssetOption(BoxLayout):

    is_active = BooleanProperty()

    def __init__(self, id, asset_name, asset_short, icon_source, attached, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.asset_name = asset_name
        self.asset_short = asset_short
        self.icon_source = icon_source
        self.is_active = id in attached.app.user_cfg["assets_pref"]
