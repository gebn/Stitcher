stitcher
========

.. image:: https://img.shields.io/pypi/status/stitcher.svg
   :target: https://pypi.python.org/pypi/stitcher
.. image:: https://img.shields.io/pypi/v/stitcher.svg
   :target: https://pypi.python.org/pypi/stitcher
.. image:: https://img.shields.io/pypi/pyversions/stitcher.svg
   :target: https://pypi.python.org/pypi/stitcher
.. image:: https://travis-ci.org/gebn/stitcher.svg?branch=master
   :target: https://travis-ci.org/gebn/stitcher
.. image:: https://coveralls.io/repos/github/gebn/stitcher/badge.svg?branch=master
   :target: https://coveralls.io/github/gebn/stitcher?branch=master
.. image:: https://landscape.io/github/gebn/stitcher/master/landscape.svg?style=flat
   :target: https://landscape.io/github/gebn/stitcher/master

Stitcher is a command-line utility for joining Messenger conversation screenshots.

Installation
------------

::

    $ pip install stitcher

Usage
-----

General usage:

::

    $ stitch <profile> <outfile> <images>...

Combine ``IMG_0001.PNG`` and ``IMG_0002.PNG`` taken on an iPhone 5S, saving the result to ``composition.png``:

::

    $ stitch IPHONE_5S composition.png IMG_0001.PNG IMG_0002.PNG IMG_0003.PNG

Combine all ``.png`` files in the present working directory using the profile for LG’s G3 phone, outputting to ``combined.png``:

::

    $ stitch LG_G3 combined.png *.png

Profiles
--------

Profiles define parameters used by Stitcher to join images. They are stored within the ``profiles`` directory, organised by device manufacturer. The following options can be specified:

+--------------+---------------------------------------+-------+------------------+
| Name         | Description                           | Requi | Default          |
|              |                                       | red   |                  |
+==============+=======================================+=======+==================+
| ``mode``     | The image format                      | No    | RGBA             |
+--------------+---------------------------------------+-------+------------------+
| ``header_hei | The number of pixels of vertical      | Yes   |                  |
| ght``        | height to crop from the top of the    |       |                  |
|              | image                                 |       |                  |
+--------------+---------------------------------------+-------+------------------+
| ``footer_hei | The number of pixels of vertical      | No    | Same as          |
| ght``        | height to crop from the bottom of the |       | ``header_height` |
|              | image                                 |       | `                |
+--------------+---------------------------------------+-------+------------------+
| ``additional | The vertical spacing between messages | Yes   |                  |
| _message_gap | from the same sender                  |       |                  |
| ``           |                                       |       |                  |
+--------------+---------------------------------------+-------+------------------+
| ``reply_mess | The vertical spacing between two      | No    | Same as          |
| age_gap``    | messages sent by different            |       | ``additional_mes |
|              | participants                          |       | sage_gap``       |
+--------------+---------------------------------------+-------+------------------+

If you’d like to add a missing a profile for your device, create a new file if necessary, and add a dictionary with the device’s details. Please consider contributing it in a pull request so others may benefit!
