.. _testhowto:

Howto for Testers
=================

This document covers a how-to guide to:

#. Quickly fetching latest development code, and
#. Reporting bugs.

Let's go!

.. _fetchinglatest:

Fetching latest development code
---------------------------------

To allow rapid testing in different platforms, we have put together a quick script that is able to fetch latest development code. It more or less does all the steps covered in the :ref:`Setting up a Work Enviroment <environment>` section, only that in a more compact way suitable (ahem) also for non developers. 

Install dependencies
^^^^^^^^^^^^^^^^^^^^
First, install all the base dependencies plus git, virtualenv and development files needed to compile several extensions::

   apt-get install openvpn git-core libgnutls-dev python-dev python-qt4 python-setuptools python-virtualenv


Bootstrap script
^^^^^^^^^^^^^^^^
.. note:: getting latest version of this script.
   At some moment we will publish an url  from where you can download this script. For now, you can copy and paste this.

.. note::
   This will fetch the *develop* branch. If you want to test another branch, just change it in the line starting with *pip install...*. Alternatively, bug kali so she add an option branch to a decent script.

Then copy and paste this script somewhere in your path, in the parent folder where you want your testing build to be downloaded. For instance, to `/tmp/leap_client_bootstrap`:

.. code-block:: bash
   :linenos:

        #!/bin/bash

        # Installs requirements, and
        # clones the latest leap-client

        # depends on:
        # openvpn git-core libgnutls-dev python-dev python-qt4 python-setuptools python-virtualenv

        # Escape code
        esc=`echo -en "\033"`

        # Set colors
        cc_green="${esc}[0;32m"
        cc_yellow="${esc}[0;33m"
        cc_blue="${esc}[0;34m"
        cc_red="${esc}[0;31m"
        cc_normal=`echo -en "${esc}[m\017"`

        echo "${cc_yellow}"
        echo "~~~~~~~~~~~~~~~~~~~~~~"
        echo "LEAP                  "
        echo "client bootstrapping  "
        echo "~~~~~~~~~~~~~~~~~~~~~~"
        echo ""
        echo "${cc_green}Creating virtualenv...${cc_normal}"

        mkdir leap-client-testbuild
        virtualenv leap-client-testbuild
        source leap-client-testbuild/bin/activate

        echo "${cc_green}Installing leap client...${cc_normal}"

        # Clone latest git (develop branch)
        # change "develop" for any other branch you want.


        pip install -e 'git://leap.se/leap_client@develop#egg=leap-client'

        cd leap-client-testbuild

        # symlink the pyqt libraries to the system libs
        ./src/leap-client/pkg/postmkvenv.sh 

        echo "${cc_green}leap-client installed! =)"
        echo "${cc_yellow}"
        echo "Launch it with: "
        echo "~~~~~~~~~~~~~~~~~~~~~~"
        echo "bin/leap-client"
        echo "~~~~~~~~~~~~~~~~~~~~~~"
        echo "${cc_normal}"

and then source it::

    $ cd /tmp
    $ source leap_client_bootstrap

Tada! If everything went well, you should be able to run the client by typing::

    bin/leap-client

Noticed that your prompt changed? That was *virtualenv*. Keep reading...

Activating the virtualenv
^^^^^^^^^^^^^^^^^^^^^^^^^
The above bootstrap script has fetched latest code inside a virtualenv, which is an isolated, *virtual* python local environment that avoids messing with your global paths. You will notice you are *inside* a virtualenv because you will see a modified prompt reminding it to you (*leap-client-testbuild* in this case).

Thus, if you forget to *activate your virtualenv*, the client will not run from the local path, and it will be looking for something else in your global path. So, **you have to remember to activate your virtualenv** each time that you open a new shell and want to execute the code you are testing. You can do this by typing::

    $ source bin/activate

from the directory where you *sourced* the bootstrap script.

Refer to :ref:`Using virtualenv <virtualenv>` to learn more about virtualenv.

Config files
^^^^^^^^^^^^

If you want to start fresh without config files, just move them. In linux::

    $ mv ~/.config/leap ~/.config/leap.old

Pulling latest changes
^^^^^^^^^^^^^^^^^^^^^^

You should be able to cd into the downloaded repo and pull latest changes::

    (leap-client-testbuild)$ cd src/leap-client
    (leap-client-testbuild)$ git pull origin develop

However, as a tester you are encouraged to run the whole bootstrap process from time to time to help us catching install and versioniing bugs too.

Testing the packages
^^^^^^^^^^^^^^^^^^^^
When we have a release candidate for the supported platforms (Debian stable, Ubuntu 12.04 by now), we will announce also the URI where you can download the rc for testing in your system. Stay tuned!


Reporting bugs
--------------

.. admonition:: Reporting better bugs

   There is a great text on the art of bug reporting, that can be found `online <http://www.chiark.greenend.org.uk/~sgtatham/bugs.html>`_.

We use the `LEAP Client Bug Tracker <https://leap.se/code/projects/eip-client>`_, although you can also use `Github issues <https://github.com/leapcode/leap_client/issues>`_.