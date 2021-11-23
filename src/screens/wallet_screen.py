from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.app import App


class WalletScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        Clock.schedule_once(lambda *args: self.load_assets(), 0.05)

    def load_assets(self):
        chosen_assets = self.app.user_cfg["assets_pref"]
        for asset_id in chosen_assets:
            checked_asset = self.app.app_cfg["assets"][asset_id]
            asset = CoinBox(
                id=asset_id,
                asset_name=checked_asset["name"],
                asset_short=checked_asset["short"],
                icon_source=f"props/icons/{checked_asset['name']}.png",
            )
            self.ids.asset_container.add_widget(asset)
            self.ids[asset_id] = asset


# Class defining Portfolio holdings
class CoinBox(BoxLayout):
    def __init__(
        self,
        id,
        asset_name,
        asset_short,
        icon_source,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.id = id
        self.asset_name = asset_name
        self.asset_short = asset_short
        self.icon_source = icon_source
