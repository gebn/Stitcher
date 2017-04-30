#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import sys
import argparse
import logging

import stitcher
from stitcher import util
from stitcher.profiles.profile import Profile


logger = logging.getLogger(__name__)


def _parse_args(args):
    """
    Interpret command line arguments.

    :param args: `sys.argv`
    :return: The populated argparse namespace.
    """

    parser = argparse.ArgumentParser(prog='stitch',
                                     description='Join Messenger conversation '
                                                 'screenshots.')
    parser.add_argument('-V', '--version',
                        action='version',
                        version='%(prog)s ' + stitcher.__version__)
    parser.add_argument('-v', '--verbosity',
                        help='increase output verbosity',
                        action='count',
                        default=0)
    parser.add_argument('profile',
                        type=util.decode_cli_arg,
                        help='the profile to use for stitching; valid values '
                             'are: ' + ', '.join(Profile.MAPPINGS.keys()))
    parser.add_argument('outfile',
                        type=util.decode_cli_arg,
                        help='the name of the file to save the composition to')
    parser.add_argument('images',
                        type=util.decode_cli_arg,
                        nargs='+',
                        help='paths of images to combine')
    return parser.parse_args(args[1:])


def main(args):
    """
    stitcher's entry point.

    :param args: Command-line arguments, with the program in position 0.
    """

    args = _parse_args(args)

    # sort out logging output and level
    level = util.log_level_from_vebosity(args.verbosity)
    root = logging.getLogger()
    root.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    root.addHandler(handler)

    logger.debug(args)

    try:
        profile = Profile.from_identifier(args.profile)
        image = stitcher.join(args.images, profile)
        image.save(args.outfile)
    except ValueError as e:
        util.print_error('Error: {0}'.format(e))
        return 1

    return 0


def main_cli():
    """
    stitcher's command-line entry point.

    :return: The return code of the program.
    """
    status = main(sys.argv)
    logger.debug('Returning exit status %d', status)
    return status


if __name__ == '__main__':
    sys.exit(main_cli())
