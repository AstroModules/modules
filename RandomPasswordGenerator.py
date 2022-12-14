__version__ = (2, 0, 0)

#               _             __  __           _       _
#     /\       | |           |  \/  |         | |     | |
#    /  \   ___| |_ _ __ ___ | \  / | ___   __| |_   _| | ___  ___
#   / /\ \ / __| __| '__/ _ \| |\/| |/ _ \ / _` | | | | |/ _ \/ __|
#  / ____ \\__ \ |_| | | (_) | |  | | (_) | (_| | |_| | |  __/\__ \
# /_/    \_\___/\__|_|  \___/|_|  |_|\___/ \__,_|\__,_|_|\___||___/
#
#                Β© Copyright 2022

#      https://t.me/Den4ikSuperOstryyPer4ik
#                      and
#             https://t.me/ToXicUse

#       π Licensed under the GNU AGPLv3
#    https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @AstroModules
# meta pic: https://img.icons8.com/clouds/500/000000/lock-2.png
# meta banner: https://i.imgur.com/rJScJY9.jpeg
# scope: inline
# scope: hikka_only
# scope: hikka_min 1.3.0

from .. import loader, utils
from telethon.tl.types import Message
import logging, random
from ..inline.types import InlineCall

logger = logging.getLogger(__name__)


@loader.tds
class PasswordGeneratorMod(loader.Module):
    """
    Random password/pincode generator
    You can configure the generator through the config
    """

    strings = {
        "name": "RandomPasswordGenerator",
        "_cfg_doc_pass_length": "set password length (in number of characters)",
        "_cfg_doc_pin_code_length": "set pincode length (in number of characters)",
        "_cfg_doc_simbols_in_pass": (
            "Will there be additional characters in the generated password"
            " (+-*!&$#?=@<>)?"
        ),
        "what_to_generate": "πWhat should be generated?",
        "new_random_pass": "π£ new random password π",
        "new_random_pincode": "π’ new random PIN-code π",
        "pass": "<b>π Your new password in {} characters:\n<code>{}</code></b>",
        "pincode": "<b>π Your new pincode in {} characters:\n<code>{}</code></b>",
        "menu": "π» Menu",
        "close": "π« Close",
    }

    strings_ru = {
        "_cls_doc": (
            "ΠΠ΅Π½Π΅ΡΠ°ΡΠΎΡ ΡΠ°Π½Π΄ΠΎΠΌΠ½ΠΎΠ³ΠΎ ΠΏΠ°ΡΠΎΠ»Ρ/ΠΏΠΈΠ½-ΠΊΠΎΠ΄Π°\nΠΠ°ΡΡΡΠΎΠΈΡΡ Π³Π΅Π½Π΅ΡΠ°ΡΠΎΡ ΠΌΠΎΠΆΠ½ΠΎ ΡΠ΅ΡΠ΅Π·"
            " ΠΊΠΎΠ½ΡΠΈΠ³"
        ),
        "_cfg_doc_pass_length": "Π²ΡΡΡΠ°Π²ΡΡΠ΅ Π΄Π»ΠΈΠ½Ρ ΠΏΠ°ΡΠΎΠ»Ρ(Π² ΠΊΠΎΠ»-Π²Π΅ ΡΠΈΠΌΠ²ΠΎΠ»ΠΎΠ²)",
        "_cfg_doc_pin_code_length": "Π²ΡΡΡΠ°Π²ΡΡΠ΅ Π΄Π»ΠΈΠ½Ρ ΠΠΈΠ½-ΠΠΎΠ΄Π°(Π² ΠΊΠΎΠ»-Π²Π΅ ΡΠΈΠΌΠ²ΠΎΠ»ΠΎΠ²)",
        "_cfg_doc_simbols_in_pass": (
            "ΠΠ°ΠΊΠΈΠ΅ ΡΠΈΠΌΠ²ΠΎΠ»Ρ Π΄ΠΎΠ»ΠΆΠ½Ρ Π±ΡΡΡ Π² ΡΠ³Π΅Π½Π΅ΡΠΈΡΠΎΠ²Π°Π½Π½ΠΎΠΌ ΠΏΠ°ΡΠΎΠ»Π΅?"
        ),
        "what_to_generate": "π Π§ΡΠΎ Π½Π°Π΄ΠΎ ΡΠ³Π΅Π½Π΅ΡΠΈΡΠΎΠ²Π°ΡΡ?",
        "new_random_pass": "π£ ΠΠΎΠ²ΡΠΉ ΡΠ°Π½Π΄ΠΎΠΌΠ½ΡΠΉ ΠΏΠ°ΡΠΎΠ»Ρ π",
        "new_random_pincode": "π’ ΠΠΎΠ²ΡΠΉ ΡΠ°Π½Π΄ΠΎΠΌΠ½ΡΠΉ PIN-ΠΊΠΎΠ΄ π",
        "pass": "<b>π ΠΠ°Ρ Π½ΠΎΠ²ΡΠΉ ΠΏΠ°ΡΠΎΠ»Ρ Π² {} ΡΠΈΠΌΠ²ΠΎΠ»ΠΎΠ²:\n<code>{}</code></b>",
        "pincode": "<b>π ΠΠ°Ρ Π½ΠΎΠ²ΡΠΉ ΠΏΠΈΠ½-ΠΊΠΎΠ΄ Π² {} ΡΠΈΠΌΠ²ΠΎΠ»ΠΎΠ²:</b>\n<code>{}</code>",
        "menu": "π» ΠΠ΅Π½Ρ",
        "close": "π« ΠΠ°ΠΊΡΡΡΡ",
    }

    @loader.command(ru_doc="β>ΠΊΠΎΠ½ΡΠΈΠ³ ΡΡΠΎΠ³ΠΎ ΠΌΠΎΠ΄ΡΠ»Ρ")
    async def generatorcfgcmd(self, message: Message):
        """β>config for this module"""
        name = self.strings("name")
        await self.allmodules.commands["config"](
            await utils.answer(message, f"{self.get_prefix()}config {name}")
        )

    def __init__(self):
        self._ratelimit = []
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "password_length",
                10,
                doc=lambda: self.strings("_cfg_doc_pass_length"),
                validator=loader.validators.Integer(minimum=6),
            ),
            loader.ConfigValue(
                "pincode_length",
                4,
                doc=lambda: self.strings("_cfg_doc_pin_code_length"),
                validator=loader.validators.Integer(minimum=4),
            ),
            loader.ConfigValue(
                "symbols_in_pass",
                "+-*!&$?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",
                doc=lambda: self.strings("_cfg_doc_simbols_in_pass"),
            ),
        )

    @loader.command(ru_doc="β>ΡΠ³Π΅Π½Π΅ΡΠΈΡΠΎΠ²Π°ΡΡ ΡΠ»ΡΡΠ°ΠΉΠ½ΡΠΉ ΠΏΠ°ΡΠΎΠ»Ρ/ΠΏΠΈΠ½-ΠΊΠΎΠ΄")
    async def igeneratorcmd(self, message: Message):
        """β>generate random password/pin"""
        await self.inline.form(
            self.strings("what_to_generate"),
            reply_markup=[
                [
                    {
                        "text": self.strings("new_random_pass"),
                        "callback": self.new_random_pass,
                    }
                ],
                [
                    {
                        "text": self.strings("new_random_pincode"),
                        "callback": self.new_random_pincode,
                    }
                ],
                [{"text": self.strings("close"), "action": "close"}],
            ],
            message=message,
        )

    async def igenerator(self, call: InlineCall):
        await call.edit(
            self.strings("what_to_generate"),
            reply_markup=[
                [
                    {
                        "text": self.strings("new_random_pass"),
                        "callback": self.new_random_pass,
                    }
                ],
                [
                    {
                        "text": self.strings("new_random_pincode"),
                        "callback": self.new_random_pincode,
                    }
                ],
                [{"text": self.strings("close"), "action": "close"}],
            ],
        )

    async def new_random_pass(self, call: InlineCall):
        symbols_in_pass = self.config["symbols_in_pass"]
        password_length = self.config["password_length"]
        length = int(password_length)
        password = ""
        for _ in range(length):
            password += random.choice(symbols_in_pass)
            await call.edit(
                self.strings["pass"].format(password_length, password),
                reply_markup=[
                    [{"text": self.strings("menu"), "callback": self.igenerator}],
                    [{"text": self.strings("close"), "action": "close"}],
                ],
            )

    async def new_random_pincode(self, call: InlineCall):
        pincode_length = self.config["pincode_length"]
        chars = "1234567890"
        length = int(self.config["pincode_length"])
        pincode = ""
        for _ in range(length):
            pincode += random.choice(chars)
            await call.edit(
                self.strings["pincode"].format(pincode_length, pincode),
                reply_markup=[
                    [{"text": self.strings("menu"), "callback": self.igenerator}],
                    [{"text": self.strings("close"), "action": "close"}],
                ],
            )
