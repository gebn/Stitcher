# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import six

from stitcher.profiles import apple, lg, nokia


@six.python_2_unicode_compatible
class Profile:
    """
    Represents a phone's configuration.
    """

    """
    Mappings from device names to profiles.
    This is used by the command line utility.
    """
    MAPPINGS = {
        'IPHONE_5S': apple.IPHONE_5S,
        'LG_G3': lg.G3,
        'LUMIA_925': nokia.LUMIA_925
    }

    @staticmethod
    def from_identifier(identifier):
        """
        Retrieve a profile by its unique identifier.

        :param identifier: The identifier to look up.
        :return: The corresponding profile.
        :raises ValueError: If no profile exists with the provided identifier.
        """
        if identifier not in Profile.MAPPINGS:
            raise ValueError('Unrecognised profile: ' + identifier)

        return Profile.MAPPINGS[identifier]

    def __init__(self, config):
        """
        Initialise a new profile.

        :param config: A dictionary containing configuration parameters.
        :raises ValueError: If the configuration is malformed.
        """
        try:
            self.mode = config['mode'] \
                if 'mode' in config \
                else 'RGBA'
            self.header_height = config['header_height']
            self.footer_height = config['footer_height'] \
                if 'footer_height' in config \
                else config['header_height']
            self.additional_message_gap = config['additional_message_gap']
            self.reply_message_gap = config['reply_message_gap'] \
                if 'reply_message_gap' in config \
                else config['additional_message_gap']
        except KeyError as e:
            raise ValueError('Malformed configuration: {0}'.format(e))

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
        """
        Ensures an image taken by this profile's device has a predictable set
        of basic parameters, allowing operations like copying pixels between
        different images.

        :param image: The image to normalise.
        :return: The normalised image.
        """
        return image.convert(self.mode)

    def __str__(self):
        return 'Profile(mode: {0}, header: {1}px, footer: {2}px, '.format(
            self.mode, self.header_height, self.footer_height) + \
               'additional: {0}px, swap: {1}px)'.format(
                   self.additional_message_gap, self.reply_message_gap)
