"""Cast external mp4 video to chromecast in the local network."""

import pychromecast
import sys


class CasterError(Exception):
    """Generic exception."""


class NoAvailableChromecasts(CasterError):
    """No ChromeCasts available."""


def choice(options, question=None):
    # if len(options) == 1:
    #     return 0
    if question:
        print(question)
    for idx, option in enumerate(options, start=1):
        print(f'{idx})\t{option}')

    user_choice = None
    while not user_choice:
        try:
            user_choice = int(input('Make your choice:'))
        except ValueError:
            continue
        if user_choice < 0 or user_choice > len(options):
            user_choice = None
    return user_choice-1


def get_target_chromecast():
    chromecasts = pychromecast.get_chromecasts()
    if not chromecasts:
        raise NoAvailableChromecasts
    return chromecasts[
        choice(
            [c.device.friendly_name for c in chromecasts],
            question='Choose target Chromecast'
        )
    ]


def get_target_video_url():
    return sys.argv[1]


def cast(chromecast, video_url):
    chromecast.wait()
    mc = chromecast.media_controller
    mc.play_media(video_url, 'video/mp4')
    mc.block_until_active()


def main():
    video_url = get_target_video_url()
    chromecast = get_target_chromecast()
    cast(chromecast, video_url)


if __name__ == '__main__':
    main()
