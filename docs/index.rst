.. LEAP documentation master file, created by
   sphinx-quickstart on Sun Jul 22 18:32:05 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

LEAP Encryption Access Project Client
=====================================

Release v\ |version|. (`Impatient? jump to the` :ref:`Installation <install>` `section!`)

The **LEAP Client** is a :ref:`GPL3 Licensed <gpl3>` multiplatform client, written in python using PyQt4, that supports the features offered by :ref:`the LEAP Platform <leapplatform>`. Currently is being tested on Linux, support for OSX and Windows will come soon.

User Guide
----------

.. toctree::
   :maxdepth: 2

   user/intro
   user/install
   user/running

Tester Guide
------------

This part of the documentation details how to fetch the last development version and how to report bugs.

.. toctree::
   :maxdepth: 1

   testers/howto

Hackers Guide
---------------

If you want to contribute to the project, we wrote this for you.

.. toctree::
   :maxdepth: 1

   dev/environment
   dev/tests
   dev/resources
   dev/internationalization

.. dev/internals
   dev/authors
   dev/todo
   dev/workflow

Packager Guide
---------------

Docs related to the process of building and releasing a version of the client.

.. toctree::
   :maxdepth: 1

   pkg/debian
   pkg/osx
   pkg/win


Directories and Files
---------------------

Different directories and files used for the configuration of the client.

.. toctree::
   :maxdepth: 1

   config/files


API Documentation
-----------------

If you are looking for a reference to specific classes or functions, you are likely to find it here

.. note::
   when it's finished, that's it :)

.. toctree::
   :maxdepth: 2

   api