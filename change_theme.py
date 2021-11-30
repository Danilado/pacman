from datetime import datetime

import global_vars


class ChangeThemeApi:
    @staticmethod
    def set_common_textures():
        global_vars.texture_modifier = ""

    @staticmethod
    def set_alt_textures():
        global_vars.texture_modifier = "r_"

    def tick(self):
        current_time = datetime.now()
        if current_time.hour >= 18 or current_time.hour <= 5:
            self.set_alt_textures()
        else:
            self.set_common_textures()
