from collections import Counter


def chunk_pixels(pixels, size):
    for i in range(0, len(pixels), size):
        yield pixels[i:i + size]

def multiply_ones_and_twos(pixel_values):
    min_zeroes = None
    result = 0
    for chunk in chunk_pixels(pixel_values, 25 * 6):
        counted = Counter(chunk)
        if min_zeroes is None or counted['0'] < min_zeroes:
            min_zeroes = counted['0']
            result = counted['1'] * counted['2']
    return result


def chunk_to_layer(chunk, height, width):
    layer = []
    for row in chunk_pixels(chunk, width):
        layer.append(row)
    assert len(layer) == height
    return layer


def get_layers(pixel_values):
    layers = []
    for chunk in chunk_pixels(pixel_values, 25 * 6):
        layers.append(chunk_to_layer(chunk, 6, 25))
    return layers


def get_pixel_from_layers(layers, y, x):
    for layer in layers:
        if str(layer[y][x]).strip() != '2':
            return layer[y][x]
    return 2


def print_image(pixel_values):
    layers = get_layers(pixel_values)
    for i in range(6):
        line = ""
        for j in range(25):
            pixel = str(get_pixel_from_layers(layers, i, j)).strip()
            if pixel == '2':
                line += ' '
            elif pixel == '0':
                line += '⬛️'
            else:
                line += '⬜️'
        print(line)


if __name__ == "__main__":
    with open("../Day8/part1.txt") as file:
        pixel_values = file.readline()
        print(multiply_ones_and_twos(pixel_values))
        print_image(pixel_values)


