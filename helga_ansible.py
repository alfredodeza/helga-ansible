import requests
import re
from helga.plugins import command
from helga import log, settings

logger = log.getLogger(__name__)


@command('ansible', aliases=['an'], help='run ansible playbooks', priority=0)
def helga_ansible(client, channel, nick, message, cmd, args):
    pass
