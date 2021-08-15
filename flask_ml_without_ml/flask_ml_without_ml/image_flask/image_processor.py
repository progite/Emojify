import PIL.Image
from PIL import ImageDraw
from PIL import JpegImagePlugin
from webcolors import rgb_to_name
from colorama import init
from termcolor import colored
import webcolors
import SCORE
from math import sqrt


def resize_image(image1: JpegImagePlugin.JpegImageFile, new_width=100):
    width, height = image1.size
    ratio = height/width
    new_height = int(new_width * ratio)
    image1.thumbnail((new_width,new_height))
    return(image1)


def get_intensity_list_for_pixels(image1):
    width, height = image1.size
    pixel_matrices = []  # ht x width [0][1] => ht 0, width 1
    for y in range(height):
        pixel_matrices.append([])  # [[2,3,4], [12]]
        for x in range(width):
            rgb = image1.getpixel((x, y))
            intensity = (rgb[0]+rgb[1]+rgb[2])//3
            pixel_matrices[-1].append(intensity)
    return(pixel_matrices)

# def get_intensity_list_for_emojis(intensity_to_dots):
#     for x in intensity_to_dots:
#         rgb = image1.getpixel((x, y))
#         intensity = (rgb[0]+rgb[1]+rgb[2])//3
def creating_different_images(path, ascii_image_filename,emoji_list,new_image_data):
    emoji_list_len=len((emoji_list))
    with open(ascii_image_filename, "w",encoding='utf-8') as f:
        for line in new_image_data:
            pixel = ''
            for intensity in line:
                pixel = emoji_list[intensity //
                                          (255//emoji_list_len) - 1]
                f.write(pixel)
            f.write('\n')
        f.close()
        
def process_image(path, ascii_image_filename,i,new_width=100):
    try:
        input_image = PIL.Image.open(path)
    except:
        print(path, " is not a valid pathname to an image.")
        return
    new_image_data = get_intensity_list_for_pixels((resize_image(input_image)))
    pixel_count = len(new_image_data)
    intensity_to_dots=[["🖤", "🌑", "🐺", "🐚", "▲", "🎶", "🌑", "🙈 ", "💿", "💀", "🌑"],['👋🏿','👋🏾','👋🏽','👋🏼','🐚','🖤'],['🖤','🌑','✊🏾','👋🏾','🚙','🥬','👋🏿','👋🏾','🚗','👋🏽','🚖','💞','🐚','🕋'],["🌑", "🐺", "🐚",'P','Q','1']]
    creating_different_images(path, ascii_image_filename,intensity_to_dots[i],new_image_data)
    

