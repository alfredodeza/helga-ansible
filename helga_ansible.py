import requests
from datetime import datetime
import os
from helga.plugins import command
from helga import log, settings

logger = log.getLogger(__name__)

import subprocess
import sys
from select import select


def run(cmd, **kw):
    build_directory = kw.pop('build_directory')
    stdout_log = os.path.join(build_directory, 'stdout_log')
    stderr_log = os.path.join(build_directory, 'stderr_log')
    status_file = os.path.join(build_directory, 'status')

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True,
        **kw
    )

    while True:
        reads, _, _ = select(
            [process.stdout.fileno(), process.stderr.fileno()],
            [], []
        )

        for descriptor in reads:
            if descriptor == process.stdout.fileno():
                read = process.stdout.readline()
                if read:
                    with open(stdout_log) as log:
                        log.write(read)
                    sys.stdout.flush()

            if descriptor == process.stderr.fileno():
                read = process.stderr.readline()
                if read:
                    with open(stderr_log) as log:
                        log.write(read)
                    sys.stderr.flush()

        if process.poll() is not None:
            break

    returncode = process.wait()
    if returncode != 0:
        with open(status_file, 'w') as s:
            s.write(returncode)


def build_dir(name):
    """
    Ensure there is a build dir, regardless if it is configured or not,
    defaulting to some `/tmp/` location
    """
    directory = getattr(settings, 'ANSIBLE_BUILD_DIR', '/tmp/helga/ansible-build/')
    now = datetime.utcnow().isoformat()[:-4]
    directory = os.path.join(directory, name)
    directory = os.path.join(directory, now)

    def _mkdir_recursive(path):
        sub_path = os.path.dirname(path)
        if not os.path.exists(sub_path):
            _mkdir_recursive(sub_path)
        if not os.path.exists(path):
            os.mkdir(path)

    _mkdir_recursive(directory)
    return directory


@command('ansible', aliases=['an'], help='run ansible playbooks', priority=0)
def helga_ansible(client, channel, nick, message, cmd, args):
    commands = getattr(settings, 'ANSIBLE_BUILDS', {}).items()
    host = socket.gethostname()
    cmd = args.pop(0)
    if cmd not in commands:
        return "I don't have %s configured as an ansible playbook to run" % cmd

    options = commands[cmd]
    build_directory = build_dir(cmd)

    # go to the build_directory we need
    os.chdir(build_directory)
    if options.get('directory'):
        os.chdir(options['directory'])

    if args:
        args = ['--extra-vars', "%s" % ' '.join(args)]
        cmd = cmd.extend(args)

    run(cmd, build_directory=build_directory)
    msg = [
        'running: %s' % ' '.join(cmd),
        'build running from %s at %s' % (host, build_directory),
    ]
    return msg
