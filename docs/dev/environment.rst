.. _environment:

Setting up a development environment
====================================

This document covers how to get an enviroment ready to contribute code to the LEAP Client.

Cloning the repo
----------------
.. note::
   Stable releases will be in *master* branch (nothing there yet, move on!).
   Development code lives in *develop* branch.

::

    git clone git://leap.se/leap_client 

Base Dependencies
------------------
Leap client depends on these libraries:

* `python 2.6 or 2.7`
* `qt4` libraries (see also :ref:`Troubleshooting PyQt install <pyqtvirtualenv>` about how to install inside your virtualenv)
* `openssl`
* `openvpn <http://openvpn.net/index.php/open-source/345-openvpn-project.html>`_

Debian
^^^^^^
In debian-based systems::

  $ apt-get install openvpn python-qt4 python-crypto python-openssl

To install the software from sources::

  $ apt-get install python-pip python-dev

.. _virtualenv:

Working with virtualenv
-----------------------

Intro
^^^^^^^^^^^^^^^^^^^

*Virtualenv* is the *Virtual Python Environment builder*.

It is a tool to create isolated Python environments.

The basic problem being addressed is one of dependencies and versions, and indirectly permissions. Imagine you have an application that needs version 1 of LibFoo, but another application requires version 2. How can you use both these applications? If you install everything into /usr/lib/python2.7/site-packages (or whatever your platform's standard location is), it's easy to end up in a situation where you unintentionally upgrade an application that shouldn't be upgraded.

Read more about it in the `project documentation page <http://pypi.python.org/pypi/virtualenv/>`_. 


Create and activate your dev environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

    $ virtualenv </path/to/new/environment>
    $ source </path/to/new/environment>/bin/activate

Install python dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can install python dependencies with pip. If you do it inside your working environment, they will be installed avoiding the need for administrative permissions::

    $ pip install -r pkg/requirements.pip

.. _pyqtvirtualenv:

Troubleshooting PyQt install inside a virtualenv
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you attempt to install PyQt inside a virtualenv using pip, it will fail because PyQt4 does not use the standard setup.py mechanism.

As a workaround, you can run the following script after creating your virtualenv. It will symlink to your global PyQt installation (*this is the recommended way if you are running a debian-based system*)::

    $ pkg/postmkvenv.sh

A second option if that does not work for you would be to install PyQt globally and pass the ``--site-packages`` option when you are creating your virtualenv::

    $ apt-get install python-qt4
    $ virtualenv --site-packages .

Or, if you prefer, you can also `download the official PyQt tarball <http://www.riverbankcomputing.com/software/pyqt/download>`_ and execute ``configure.py`` in the root folder of their distribution, which generates a ``Makefile``::

    $ python configure.py
    $ make && make install

.. note::
   this section could be completed with useful options that can be passed to the virtualenv command (e.g., to make portable paths, site-packages, ...).


.. _copyscriptfiles:

Copy script files
-----------------

The openvpn invocation expects some files to be in place. If you have not installed `leap-client` from a debian package, you must copy these files manually::

    $ sudo mkdir -p /etc/leap
    $ sudo cp pkg/linux/resolv-update /etc/leap 

.. _policykit:

Running openvpn without root privileges
---------------------------------------

In linux, we are using ``policykit`` to be able to run openvpn without root privileges, and a policy file is needed to be installed for that to be possible.
The setup script tries to install the policy file when installing the client system-wide, so if you have installed the client in your global site-packages at least once it should have copied this file for you. 

If you *only* are running the client from inside a virtualenv, you will need to copy this file by hand::

    $ sudo cp pkg/linux/polkit/net.openvpn.gui.leap.policy /usr/share/polkit-1/actions/


Missing Authentication agent
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are running a desktop other than gnome or unity, you might get an error saying that you are not running the authentication agent. You can launch it like this::

    /usr/lib/policykit-1-gnome/polkit-gnome-authentication-agent-1 &
