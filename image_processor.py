import PIL.Image
from PIL import ImageDraw
from PIL import JpegImagePlugin
from webcolors import rgb_to_name
from colorama import init
from termcolor import colored
import webcolors
import score_tracker
from math import sqrt


def resize_image(image: JpegImagePlugin.JpegImageFile, new_width=100):
    width, height = image.size
    ratio = height/width
    new_height = int(new_width * ratio)
    image.thumbnail((new_width, new_height))
    return(image)


def get_intensity_list_for_pixels(image):
    width, height = image.size
    pixel_matrices = []  # ht x width [0][1] => ht 0, width 1
    for y in range(height):
        pixel_matrices.append([])  # [[2,3,4], [12]]
        for x in range(width):
            rgb = image.getpixel((x, y))
            intensity = (rgb[0]+rgb[1]+rgb[2])//3
            pixel_matrices[-1].append(intensity)
    return(pixel_matrices)


def creating_different_images(path, ascii_image_filename, emoji_list, new_image_data):
    emoji_list_len = len((emoji_list))
    with open(ascii_image_filename, "w", encoding='utf-8') as file:
        for line in new_image_data:
            pixel = ''
            for intensity in line:
                pixel = emoji_list[intensity //
                                   (255//emoji_list_len) - 1]
                file.write(pixel)
            file.write('\n')
        file.close()


def process_image(path, ascii_image_filename, i, new_width=100):
    try:
        input_image = PIL.Image.open(path)
    except:
        print(path, " is not a valid pathname to an image.")
        return
    new_image_data = get_intensity_list_for_pixels((resize_image(input_image)))
    pixel_count = len(new_image_data)
    intensity_to_dots = [["🖤", "🌑", "🐺", "🐚", "▲", "🎶", "🌑", "🙈 ", "💿", "💀", "🌑"], ['👋🏿', '👋🏾', '👋🏽', '👋🏼', '🐚', '🖤'], [
        '🖤', '🌑', '✊🏾', '👋🏾', '🚙', '🥬', '👋🏿', '👋🏾', '🚗', '👋🏽', '🚖', '💞', '🐚', '🕋'], ["🌑", "🐺", "🐚", 'P', 'Q', '1']]
    creating_different_images(
        path, ascii_image_filename, intensity_to_dots[i], new_image_data)
