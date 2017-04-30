# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

import six
from PIL import Image, ImageChops, ImageDraw


logger = logging.getLogger(__name__)


@six.python_2_unicode_compatible
class Join:
    """
    Describes the join between two images.
    """

    @property
    def image(self):
        """
        Create an image visualising this join.

        :return: The two images joined.
        """

        upper_height = self.upper.height - self.lower_crop
        lower_height = self.lower.height - self.upper_crop
        canvas = Image.new(self.upper.mode,
                           (self.upper.width,
                            upper_height + self.spacing + lower_height),
                           'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(self.upper.crop((0, 0, self.upper.width, upper_height)),
                     (0, 0))
        draw.line([(0, upper_height - 1), (100, upper_height - 1)], 'black')
        canvas.paste(self.lower.crop((0,
                                      self.upper_crop,
                                      self.lower.width,
                                      self.lower.height)),
                     (0,
                      upper_height + self.spacing))
        draw.line([(self.lower.width - 100, upper_height + self.spacing),
                   (self.lower.width, upper_height + self.spacing)],
                  'black')
        return canvas

    def __init__(self, upper, lower, lower_crop, spacing, upper_crop):
        """
        Initialise a new join.

        :param upper: The first image.
        :param lower: The second image.
        :param lower_crop: The number of pixels to crop off the upper image.
        :param spacing: The spacing to leave blank between the images.
        :param upper_crop: The number of pixels to crop off the lower image.
        """

        self.upper = upper
        self.lower = lower
        self.lower_crop = lower_crop
        self.spacing = spacing
        self.upper_crop = upper_crop

    @staticmethod
    def calculate(profile, upper, lower):
        """
        Calculates the join between two images.

        :param profile: The device configuration for these images.
        :param upper: The first image.
        :param lower: The second image.
        :return: A Join instance representing the join.
        """

        def prepare(image):
            return Join._trim_whitespace(image)

        return Join._calculate_join(profile,
                                    prepare(upper),
                                    prepare(lower))

    @staticmethod
    def _trim_whitespace(image):
        """
        Trim background from the top and bottom of a cropped image.

        :param image: The image to crop. This must already be cropped according
                      to the profile of the device that produced it.
        :return: The cropped image.
        """

        bg = Image.new(image.mode, image.size, image.getpixel((0, 0)))
        box = ImageChops.difference(image, bg).getbbox()
        return image.crop((0, box[1], image.width, box[3]))

    @staticmethod
    def _calculate_join(profile, upper, lower, overlap=2):
        """
        Calculate where two images join together if the first is placed above
        the second.

        :param profile: The device configuration for these images.
        :param upper: The first image.
        :param lower: The second image.
        :param overlap: The number of pixels to match before considering the
                        images overlapped. If either of the input images'
                        heights is less than this figure, it will be reduced to
                        the tallest possible height. On the flip-side, if more
                        pixels are available and the needle produced by the
                        passed overlap is poor, it will be increased.
        :return: An integer indicating the number of pixels to crop off the top
                 of the second image.
        """

        shortest_height = min(upper.height, lower.height)
        if overlap > shortest_height:
            # we need to tone down the overlap
            overlap = shortest_height
            needle = Join._extract_slice(lower, 0, overlap)
            logger.debug('The overlap is more than the shortest height '
                         '- shrunk needle height to %dpx', needle.height)
        else:
            # the match area is smaller than the shortest image - we have some
            # vertical pixels to play with
            breathing = shortest_height - overlap
            needle = Join._find_needle(lower, overlap, overlap + breathing)
            overlap = needle.height
            logger.debug('Using a needle height of %dpx for this join',
                         overlap)

        # work our way up the first image, extracting slices and matching them
        # against the needle area above
        for offset in range(upper.height - overlap + 1, -1, -1):
            trial = Join._extract_slice(upper, offset, overlap)

            # we can't use `ImageChops.difference()` as Android doesn't always
            # render the same areas of messages in the same way - there are
            # minor (but problematic) differences in RGB values
            if Join._are_identical(needle.getdata(), trial.getdata()):

                # the rectangles are identical
                logger.debug('Found intersection starting %d pixels into the '
                             'first image', offset)
                return Join(upper, lower, 0, 0, upper.height - offset)

        # now we're into guesswork
        upper_bottom_modal = Join._modal_colour(
            Join._extract_slice(upper, upper.height - 1, 1))
        lower_top_modal = Join._modal_colour(Join._extract_slice(lower, 0, 1))

        # assume the same person was the last to comment in upper and the first
        # to comment in lower
        if upper_bottom_modal == lower_top_modal:
            # now we need to find out if the same message crosses the border,
            # of if it's two different ones
            if Join._count_colour(upper_bottom_modal,
                                  Join._extract_slice(upper,
                                                      upper.height - 1,
                                                      1)) == \
                    Join._count_colour(upper_bottom_modal,
                                       Join._extract_slice(upper,
                                                           upper.height - 2,
                                                           1)):
                # it's the same
                # TODO adjust overlap - use the background colour
                return Join(upper, lower, 0, 0, 0)

            # it's different
            return Join(upper, lower, 0, profile.additional_message_gap, 0)

        # assume the commenter was different
        return Join(upper, lower, 0, profile.reply_message_gap, 0)

    @staticmethod
    def _are_identical(first, second, tolerance=5):
        """
        Determines whether two images are the same within a given tolerance.

        :param first: The first image.
        :param second: The second image.
        :param tolerance: The maximum amount a single RGB(A) value can differ
                          by for the images to still be considered identical.
        :return: True if the images can be considered identical, false
                 otherwise.
        """

        for pixel_a, pixel_b in zip(first, second):  # pixels
            for value_a, value_b in zip(pixel_a, pixel_b):  # RGB(A) values
                if abs(value_a - value_b) > tolerance:
                    return False
        return True

    @staticmethod
    def _modal_colour(image):
        """
        Find the most popular colour in an image.

        :param image: The image to analyse.
        :return: The colour that appears most frequently in the image.
        """

        w, h = image.size
        pixels = image.getcolors(w * h)
        modal = pixels[0]

        for count, colour in pixels:
            if count > modal[0]:
                modal = (count, colour)

        return modal[1]

    @staticmethod
    def _count_colour(colour, image):
        """
        Counts the number of pixels of a certain colour in an image.

        :param colour: The colour to look for.
        :param image: The image to look for the colour in.
        :return: The number of pixels in `image` of colour `colour`.
        """
        return len([1 for pixel in image.getdata() if pixel == colour])

    @staticmethod
    def _guess_bubble_backgrounds(image):
        frequencies = image.getcolors(image.width * image.height)
        ordered = sorted(frequencies, key=lambda frequency: frequency[0])

        # most common is probably the app background, so ignore
        # second and third most common are likely to be the message backgrounds
        return [ordered[1][1], ordered[2][1]]

    @staticmethod
    def _find_needle(image, lower, upper, threshold=5):
        """
        Determines and extracts the top area of the lower image that we will
        try to find in the upper one.

        This method exists to attempt to eradicate the unreliable situation
        where we are determining where to stitch based on areas of the images
        which lack text.

        :param image: The second image in the join pair.
        :param lower: The minimum height of the needle area.
        :param upper: The maximum height of the needle area.
        :param threshold: The minimum number of unique colours a viable match
                          area contains.
        :return: The decided needle image.
        """

        assert lower <= upper <= image.height

        # take taller and taller areas of the image until we find one diverse
        # enough that it is suitable to match against
        for offset in range(lower, upper + 1):
            crop = image.crop((0, 0, image.width, offset))

            # if there are >=`threshold` colours, return the crop area
            if not crop.getcolors(threshold - 1):
                return crop

        # worse case scenario - all we can do is use the largest area possible
        return image.crop((0, 0, image.width, upper))

    @staticmethod
    def _extract_slice(image, start, rows):
        """
        Returns the first `rows` rows of pixels from `image`, starting at the
        `start`th row.
        The full width of the image is used.

        :param image: The image to extract a slice from.
        :param start: The first row to extract, 0-based (i.e. to start at the
                      first row, pass 0).
        :param rows: The number of rows of pixels to extract.
        :return: The first `rows` rows of pixels from the image, starting at
                 the `start`th row.
        """

        return image.crop((0, start, image.width, start + rows))

    def __str__(self):
        return 'Join(lower_crop: {0}px, spacing: {1}px, upper_crop: {2}px)' \
            .format(self.lower_crop, self.spacing, self.upper_crop)
