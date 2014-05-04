import pygame
import os
import argparse
import fnmatch


def get_image_files(image_dir):

    files = []
    file_types = ["*.png", "*.jpeg", "*.jpg"]
    for dirpath, dirnames, filenames in os.walk(image_dir):
        for file_pattern in file_types:
            files.extend([os.path.join(dirpath, fname) for fname in fnmatch.filter(filenames, file_pattern)])

        for dirname in dirnames:
            files.extend(get_image_files(os.path.join(dirpath, dirname)))

    return files


def display_image(img, screen, delay):

    scale_ratio = float(img.get_height()) / float(screen.get_height())
    new_w = int(img.get_width() / scale_ratio)
    new_h = int(img.get_height() / scale_ratio)
    scaled = pygame.transform.scale(img, (new_w, new_h))

    for ii in range(scaled.get_width() + screen.get_width(), 0, -5):
        screen.blit(scaled, (-1 * ii , 0))
        pygame.time.wait(delay)
        pygame.display.flip()




def main():
    parser = argparse.ArgumentParser("Raspberry Pi Photo slides show")
    parser.add_argument("--image-dir", type=str, help="location of images.")
    parser.add_argument("--on-pi", action="store_true", default=False)
    parser.add_argument("--background-colour", default="250,250,250", help="background colour")
    parser.add_argument("--resolution", default="1024x768", help="screen resolution.")
    parser.add_argument("--delay", default=5, type=int)
    parser.add_argument("--scroll-delay", default=3, type=int, help="Millieconds to wait between image scroll.")

    opts = parser.parse_args()

    if opts.on_pi:
        os.putenv('SDL_VIDEODRIVER', 'fbcon')

    pygame.init()

    screen = pygame.display.set_mode([int(x) for x in opts.resolution.split('x')])

    background = pygame.Surface(screen.get_size()).convert()
    background.fill([int(x) for x in opts.background_colour.split(',')])

    screen.blit(background, (0,0))
    while True:
        for image_file in get_image_files(opts.image_dir):
            img = pygame.image.load(image_file).convert()
            display_image(img, screen, opts.scroll_delay)
            pygame.time.wait(opts.delay * 1000)


if __name__ == "__main__":
    main()

