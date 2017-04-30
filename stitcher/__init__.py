# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pkg_resources import get_distribution, DistributionNotFound
import os
import logging

from stitcher.composition import Composition
from stitcher.profiles.profile import Profile


__title__ = 'stitcher'
__author__ = 'George Brighton'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 George Brighton'

logger = logging.getLogger(__name__)


# adapted from http://stackoverflow.com/a/17638236
try:
    dist = get_distribution(__title__)
    path = os.path.normcase(dist.location)
    pwd = os.path.normcase(__file__)
    if not pwd.startswith(os.path.join(path, __title__)):
        raise DistributionNotFound()
    __version__ = dist.version
except DistributionNotFound:
    __version__ = 'unknown'


def join(paths, profile):
    """
    Stitches an ordered sequence of images together.

    :param paths: The paths of the images to join in order.
    :param profile: The profile dictionary of the device that produced the
                    images.
    :return: A PIL image representing the composite.
    """
    logger.info('Joining %d images using params %s', len(paths), profile)
    return Composition(Profile(profile)).process(paths)
