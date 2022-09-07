#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from datetime import datetime

hours = [
    [(9, 2), (10, 2), (11, 2), (12, 2), (13, 2), (14, 2)],  # midday
    [(2, 0), (3, 0), (4, 0)],  # 1
    [(7, 0), (8, 0), (9, 0), (10, 0)],  # 2
    [(2, 2), (3, 2), (4, 2), (5, 2), (6, 2)],  # 3
    [(5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1)],  # 4
    [(2, 1), (3, 1), (4, 1), (5, 1)],  # 5
    [(6, 2), (7, 2), (8, 2)],  # 6
    [(11, 0), (12, 0), (13, 0), (14, 0)],  # 7
    [(11, 1), (12, 1), (13, 1), (14, 1)],  # 8
    [(3, 0), (4, 0), (5, 0), (6, 0)],  # 9
    [(8, 3), (9, 3), (10, 3)],  # 10
    [(2, 3), (3, 3), (4, 3), (5, 3)],  # 11
    [(6, 3), (7, 3), (8, 3), (9, 3)]  # midnight
]

hour = [(2, 4), (3, 4), (4, 4), (5, 4), (6, 4)]

quarters = [
    [],
    [(11, 5), (12, 5), (13, 5), (14, 5)],  # 5
    [(2, 6), (3, 6), (4, 6)],  # 10
    [(3, 5), (4, 5), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6)],  # 15
    [(5, 5), (6, 5), (7, 5), (8, 5), (9, 5)],  # 20
    [(5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (10, 5), (11, 5), (12, 5), (13, 5), (14, 5)],  # 25
    [(3, 5), (4, 5), (10, 6), (11, 6), (12, 6), (13, 6), (14, 6)],  # 30
    [(9, 4), (10, 4), (11, 4), (12, 4), (13, 4), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (10, 5), (11, 5), (12, 5),
     (13, 5), (14, 5)],  # - 25
    [(9, 4), (10, 4), (11, 4), (12, 4), (13, 4), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5)],  # - 20
    [(9, 4), (10, 4), (11, 4), (12, 4), (13, 4), (2, 5), (3, 5), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6)],  # - 15
    [(9, 4), (10, 4), (11, 4), (12, 4), (13, 4), (2, 6), (3, 6), (4, 6)],  # - 10
    [(9, 4), (10, 4), (11, 4), (12, 4), (13, 4), (11, 5), (12, 5), (13, 5), (14, 5)]  # - 5
]

gouter = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6)]

seconds = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7),
           (6, 7), (7, 7), (8, 7), (9, 7), (10, 7), (11, 7), (12, 7), (13, 7), (14, 7), (15, 7), (15, 6), (15, 5),
           (15, 4), (15, 3), (15, 2), (15, 1), (15, 0)]


def main():
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial,
                     cascaded=2,
                     block_orientation=-90,
                     rotate=0,
                     blocks_arranged_in_reverse_order=False)
    while True:
        now = datetime.now()
        h = now.hour
        s = now.second

        with canvas(device) as draw:
            if 4 <= h <= 5:
                draw.point(gouter, fill="white")

            draw.point(seconds[s % 30], fill="white")

            h %= 12 # because we don't use 24 format
            m = now.minute // 5  # we go from 5 to 5

            if m > 6:
                h += 1  # because we do the time backwards

            draw.point(hours[h], fill="white")  # write hour
            if 0 < h < 12:
                draw.point(hour, fill="white")  # add "hour"
                if h > 1:
                    draw.point((7, 4), fill="white")  # add a s
            draw.point(quarters[m], fill="white")  # write minute
            time.sleep(1)


if __name__ == "__main__":
    main()
