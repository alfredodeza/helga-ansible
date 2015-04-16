An Ansible plugin for helga chat bot
====================================

About
-----

Helga is a Python chat bot. Full documentation can be found at
http://helga.readthedocs.org.

This Ansible plugin allows Helga to run Ansible playbooks from IRC and return
information when they succeed or fail.
For example::

  03:14 < alfredodeza> !ansible release-ceph version=0.80.8.1 branch=rhcs-v0.80.8 release=stable clean=true
  03:14 < helgabot> running: ansible-playbook -vv tasks/setup.yml -i hosts --extra-vars "version=0.80.8.1 branch=rhcs-v0.80.8 release=stable clean=true"
  03:14 < helgabot> build running from example.com at /opt/helga/ansible-build/release-ceph/2015-04-16T12:16:30


Failed builds will report back minimal information with an optional paste of
the log::

  03:17 < helgabot> alfredodeza: release-ceph/2015-04-16T12:16:30 ansible build failed. Details at http://fpaste.org/{ID}

Successful runs will also report back to the user::

  03:19 < helgabot> alfredodeza: release-ceph/2015-04-16T12:16:30 ansible build succeeded!

Installation
------------
This Ansible plugin is `available from PyPI
<https://pypi.python.org/pypi/ansible-ansible>`_, so you can simply install it
with ``pip``::

  pip install helga-ansible

If you want to hack on the helga-ansible source code, in your virtualenv where
you are running Helga, clone a copy of this repository from GitHub and run
``python setup.py develop``.

Configuration
-------------
In your ``settings.py`` file (or whatever you pass to ``helga --settings``),
you can configure a few general things like (listed with some defaults)::

  # The parent directory where to create builds
  ANSIBLE_BUILD_DIR = "/opt/helga/ansible-build"

  # wether to send failed log output to fpaste.org
  ANSIBLE_USE_FPASTE = True


Play-books need to be specified via configuration, so for anything that this
plugin will run, it will need to be configured properly::

  # repositories of ansible repos for projects
  ANSIBLE_BUILDS = {
    "ceph-release": {
        "git-url": "http://github.com/alfredodeza/ceph-jenkins-build",
        "directory": "ceph",
        "command": "ansible-playbook -vv tasks/setup.yml -i hosts",
    },
    "ceph-deploy-release": {
        "git-url": "http://github.com/alfredodeza/ceph-jenkins-build",
        "directory": "ceph-deploy",
        "command": "ansible-playbook -vv tasks/setup.yml -i hosts",
    }
  }
