from datetime import datetime

import globalvars


class ChangeThemeApi:
    @staticmethod
    def set_common_textures():
        globalvars.texture_modifier = ""

    @staticmethod
    def set_alt_textures():
        globalvars.texture_modifier = "r_"

    def tick(self):
        current_time = datetime.now()
        if current_time.hour >= 18 or current_time.hour <= 5:
            self.set_alt_textures()
        else:
            self.set_common_textures()
