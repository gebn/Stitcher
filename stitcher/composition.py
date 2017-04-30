# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from PIL import Image

from stitcher.join import Join
from stitcher.canvas import Canvas


logger = logging.getLogger(__name__)


class Composition:
    """
    Joins a series of images together.
    """

    def __init__(self, profile):
        """
        Initialise a new composition.

        :param profile: A profile for the device that produced the images that
                        will be combined.
        """
        logger.debug('Initialising new composition using profile %s', profile)
        self._profile = profile

    def _prepare(self, path):
        """
        Opens and normalises an image.

        :param path: The path of the image to open.
        :return: The opened, normalised image.
        """
        image = Image.open(path)
        return self._profile.normalise(image)

    def process(self, paths):
        """
        Produces a composition.

        :param paths: Paths of images to join.
        :return: The final composition as a PIL image.
        :raises ValueError: If no paths are provided.
        :raises IOError: If a path does not correspond to an image.
        """

        # if we have a list, turn it into an iterator
        paths = iter(paths)

        try:
            upper = self._prepare(next(paths))

            # as we're compatible with generators, we have no means of knowing
            # how many more images there will be - we can only expand the
            # canvas with each image we uncover
            canvas = Canvas(self._profile, upper)

            try:
                while True:
                    lower = self._prepare(next(paths))
                    join = Join.calculate(self._profile,
                                          self._profile.body(upper),
                                          self._profile.body(lower))
                    canvas.append(join)
                    upper = lower
            except StopIteration:
                # reached the end of the generator - add the footer
                canvas.finalise(upper)
                return canvas.image
        except StopIteration:
            raise ValueError('Please pass at least two images')
