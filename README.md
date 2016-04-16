# Stitcher

Stitcher is a command-line utility for joining sequences of Messenger
conversation screenshots.

## Dependencies

Compatible with Python 2.7.x and 3.

 - [Six](https://pypi.python.org/pypi/six) (1.9+)
 - [Pillow](https://pypi.python.org/pypi/Pillow)

## Usage

General usage:

    stitch <profile> <outfile> <images>...

Combine `IMG_0001.PNG` and `IMG_0002.PNG` taken on an iPhone 5S, saving the
result to `composition.png`:

    stitch IPHONE_5S composition.png IMG_0001.PNG IMG_0002.PNG IMG_0003.PNG

Combine all `.png` files in the present working directory using the profile
for LG's G3 phone, outputting to `combined.png`:

    stitch LG_G3 combined.png *.png

## Profiles

Profiles define parameters used by Stitcher to join images. They are stored
within the `profiles` directory, organised by device manufacturer. The
following options can be specified:

| Name                     | Description                                                                  | Required | Default                          |
|--------------------------|------------------------------------------------------------------------------|----------|----------------------------------|
| `mode`                   | The image format                                                             | No       | RGBA                             |
| `header_height`          | The number of pixels of vertical height to crop from the top of the image    | Yes      | -                                |
| `footer_height`          | The number of pixels of vertical height to crop from the bottom of the image | No       | Same as `header_height`          |
| `additional_message_gap` | The vertical spacing between messages from the same sender                   | Yes      | -                                |
| `reply_message_gap`      | The vertical spacing between two messages sent by different participants     | No       | Same as `additional_message_gap` |

If you'd like to add a missing a profile for your device, create a new file if
necessary, and add a dictionary with the device's details. Please consider
contributing it in a pull request so others may benefit!
