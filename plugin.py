###
# Copyright (c) 2011, Alex Wood
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.ircmsgs as ircmsgs
import supybot.callbacks as callbacks
import pyfiglet
import os
import random

class Figlet(callbacks.Plugin):
    """
    This plugin offers the ability to pipe text through the figlet library in
    order to turn words into ASCII art.
    """
    threaded = False

    def _FindFont(self, dir):
        fonts = [font[:-4] for font in os.walk(dir).next()[2] if
                font.endswith('.flf')]
        return random.choice(fonts)

    def figlet(self, irc, msg, args, text):
        """<text>
        Transform incoming text to ASCII art.
        """
        dir = self.registryValue('fontDirectory')
        font = self._FindFont(dir)
        
        fig = pyfiglet.Figlet(dir=dir, font=font)        
        
        output = fig.renderText(text)
        lines = output.split('\n')
        lines = lines[:-1] #Drop the last line since it is empty

        for line in lines:
            #msg.args[0] is the originating channel
            irc.sendMsg(ircmsgs.privmsg(msg.args[0], line))
            irc.noReply()

        print "Figlet run for '%s' in %s font" % (text, font)

    figlet = wrap(figlet, ['text'])

Class = Figlet

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
