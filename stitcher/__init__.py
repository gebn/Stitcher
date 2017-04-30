# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from stitcher.composition import Composition
from stitcher.profiles.profile import Profile


__title__ = 'stitcher'
__version__ = '0.0.1'
__author__ = 'George Brighton'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 George Brighton'


def join(paths, profile):
    """
    Stitches an ordered sequence of images together.

    :param paths: The paths of the images to join in order.
    :param profile: The profile dictionary of the device that produced the
                    images.
    :return: A PIL image representing the composite.
    """

    return Composition(Profile(profile)).process(paths)
