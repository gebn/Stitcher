# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import six


@six.python_2_unicode_compatible
class Profile:
    """
    Represents a phone's configuration.
    """

    def __init__(self, config):
        """
        Initialise a new profile.

        :param config: A dictionary containing configuration parameters.
        :raises ValueError: If the configuration is malformed.
        """
        try:
            self.mode = config['mode']
            self.header_height = config['header_height']
            self.footer_height = config['footer_height']
            self.additional_message_gap = config['additional_message_gap']
            self.reply_message_gap = config['reply_message_gap']
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
        return 'Profile(mode: {0}, header: {1}px, footer: {2}px, ' + \
               'additional: {3}px, swap: {4}px)'.format(
                   self.mode, self.header_height, self.footer_height,
                   self.additional_message_gap, self.reply_message_gap)
