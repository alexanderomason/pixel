import numpy as np
from PIL import Image
import argparse

def convert_to_graeyscale_uint8(ray, perceptual_vector = [0.2989, 0.5870, 0.1140]):
    return ray[ : , : , 0:3].dot(perceptual_vector).astype(np.uint8)

def shrunk_grey_invt_to_printable_string(ray, character_gradient = ' .:-=+*#%@'):
    transformer = lambda value : pixel_value_char_map(value, character_gradient = character_gradient )
    return('\n'.join([''.join(map(transformer , x )) for x in ray]))
def shrink_grey_scale_image_invt(gs_array, block_size = 4, invert_flag = True):
    uninverted_array = np.array(
        [ [gs_array[ j : j + block_size , i : i + block_size ].sum()/(block_size**2) for i in np.arange(0 , gs_array.shape[1]-block_size , block_size)] for j in  np.arange(0 , gs_array.shape[0]-block_size , block_size)]
    )
    if invert_flag == False:
        return uninverted_array
    else:
        return 255 - uninverted_array 
def pixel_value_char_map(val, character_gradient = ' .:-=+*#%@'):
    return character_gradient[ int( val // ( 256 / len( character_gradient ) ) ) ]   

def pixel_pipe(filepath:str, block_size  = 4, character_gradient = ' .:-=+*#%@', invert_flag = True):
    with Image.open(filepath) as image_object:
        image_var = np.array(image_object)
    
    grey_scale_array_fullsize = convert_to_graeyscale_uint8(image_var)
    
    shrunk_and_inverted = shrink_grey_scale_image_invt(grey_scale_array_fullsize, block_size = block_size, invert_flag=invert_flag)

    printable_string = shrunk_grey_invt_to_printable_string(shrunk_and_inverted, character_gradient = character_gradient)

    return printable_string

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Convert an image to ASCII art."
    )

    parser.add_argument(
        "filepath",
        help="Path to the image file"
    )

    parser.add_argument(
        "-b",
        "--block-size",
        type=int,
        default=4,
        help="Pixel block size used when shrinking the image (default: 4)"
    )

    parser.add_argument(
        "-c",
        "--character-gradient",
        default=" .:-=+*#%@",
        help="Characters used to represent pixel intensity"
    )

    parser.add_argument(
        "-i",
        "--invert",
        action=argparse.BooleanOptionalAction,
        default=True
    )
    args = parser.parse_args()

    result = pixel_pipe(
        filepath=args.filepath,
        block_size=args.block_size,
        character_gradient=args.character_gradient,
        invert_flag = args.invert
    )

    print(result)


