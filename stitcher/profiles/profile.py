# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from stitcher.mixins import UnicodeStrMixin


class Profile(UnicodeStrMixin):
    """
    Represents a phone's viewport configuration.
    """

    def __init__(self, config):
        """
        Initialise a new profile.

        :param config: A dictionary containing configuration.
        :raises ValueError: If the configuration is malformed.
        """
        try:
            self.mode = config['mode']
            self.header_height = config['header_height']
            self.footer_height = config['footer_height']
        except KeyError as e:
            raise ValueError('Malformed configuration: ' + e.message)

    def header(self, image):
        """
        Extract the header of an image according to the rules of this profile.

        :param image: The image to crop.
        :return: The header.
        """
        return image.crop((0, 0, image.width, self.header_height))

    def body(self, image):
        """
        Extract the body of an image according to the rules of this profile.

        :param image: The image to crop.
        :return: The image with header and footer removed.
        """
        return image.crop((0,
                           self.header_height,
                           image.width,
                           image.height - self.footer_height))

    def body_height(self, image):
        """
        Calculates the largest possible height a single image produced by this
        device could occupy in the final composition.

        :param image: A sample image. We assume all images produced by a device
                      will have the same dimensions.
        :return: The maximum height in pixels.
        """
        return image.height - self.header_height - self.footer_height

    def footer(self, image):
        """
        Extract the footer of an image according to the rules of this profile.

        :param image: The image to crop.
        :return: The footer.
        """
        return image.crop((0,
                           image.height - self.footer_height,
                           image.width,
                           image.height))

    def normalise(self, image):
        return image.convert(self.mode)

    def __unicode__(self):
        return 'Profile(header: {0}px, footer: {1}px)'.format(
            self.header_height, self.footer_height)
