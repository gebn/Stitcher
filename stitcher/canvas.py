# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from PIL import Image


logger = logging.getLogger(__name__)


class Canvas:
    """
    Represents the final composite image.
    Think of this as a kind of std::vector for images.
    """

    def __init__(self, profile, upper):
        """
        Initialise a new canvas.

        :param profile: The profile of the device that generated the images
                        we'll receive.
        :param upper: The header and body will be used to start the canvas.
        """
        logger.debug('Initialising new canvas using profile %s with upper %s',
                     profile, upper)
        self._profile = profile
        self.image = Image.new(self._profile.mode,
                               (upper.width,
                                upper.height - self._profile.footer_height))
        self.image.paste(upper.crop(
            (0, 0, upper.width, upper.height - self._profile.footer_height)),
            (0, 0))

    def append(self, join):
        """
        Add a join to this canvas.

        :param join: The lower image will be added. The upper image in the join
                     should be either the one passed in the constructor if this
                     is the first join, or the lower in the last append() call.
        """

        new_height = (self.image.height - join.lower_crop) + join.spacing + (
            join.lower.height - join.upper_crop)
        extended = Image.new(self._profile.mode,
                             (self.image.width, new_height))

        # add the old content (including the join's upper image), cut short if
        # necessary
        extended.paste(self.image, (0, 0, self.image.width,
                                    self.image.height - join.lower_crop))

        # add the lower image from the join
        extended.paste(join.lower.crop((0, join.upper_crop, join.lower.width,
                                        join.lower.height)),
                       (0, self.image.height - join.lower_crop + join.spacing))
        self.image = extended

    def finalise(self, lower):
        """
        End this canvas.

        :param lower: The image containing the footer to borrow.
        """

        footer = self._profile.footer(lower)
        extended = Image.new(self._profile.mode,
                             (self.image.width,
                              self.image.height + footer.height))
        extended.paste(self.image, (0, 0))
        extended.paste(footer, (0, self.image.height))
        self.image = extended
