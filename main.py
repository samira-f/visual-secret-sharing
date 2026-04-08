from PIL import Image
import random
import os


def binarize_image(image_path, threshold=128):
    img = Image.open(image_path).convert("L")
    binary = img.point(lambda p: 255 if p > threshold else 0)
    return binary


def generate_shares(binary_img):
    width, height = binary_img.size

    share1 = Image.new("1", (width * 2, height))
    share2 = Image.new("1", (width * 2, height))

    pixels = binary_img.load()
    s1 = share1.load()
    s2 = share2.load()

    patterns = [
        [(0, 1), (0, 1)],
        [(1, 0), (1, 0)],
        [(0, 1), (1, 0)],
        [(1, 0), (0, 1)],
    ]

    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            p = random.choice(patterns[:2])

            if pixel == 255:  # white
                s1[2 * x, y] = p[0][0]
                s1[2 * x + 1, y] = p[0][1]
                s2[2 * x, y] = p[1][0]
                s2[2 * x + 1, y] = p[1][1]
            else:  # black
                p = random.choice(patterns[:2])
                comp = (1 - p[0][0], 1 - p[0][1])

                s1[2 * x, y] = p[0][0]
                s1[2 * x + 1, y] = p[0][1]
                s2[2 * x, y] = comp[0]
                s2[2 * x + 1, y] = comp[1]

    return share1.convert("L"), share2.convert("L")


def overlay_shares(share1, share2):
    width, height = share1.size
    result = Image.new("1", (width, height))

    p1 = share1.convert("1").load()
    p2 = share2.convert("1").load()
    pr = result.load()

    for y in range(height):
        for x in range(width):
            pr[x, y] = p1[x, y] & p2[x, y]

    return result.convert("L")


def main():
    input_path = "input/secret.png"
    os.makedirs("output", exist_ok=True)

    binary_img = binarize_image(input_path)
    share1, share2 = generate_shares(binary_img)
    recovered = overlay_shares(share1, share2)

    binary_img.save("output/binary_secret.png")
    share1.save("output/share1.png")
    share2.save("output/share2.png")
    recovered.save("output/recovered.png")

    print("Done.")
    print("Saved:")
    print("- output/binary_secret.png")
    print("- output/share1.png")
    print("- output/share2.png")
    print("- output/recovered.png")


if __name__ == "__main__":
    main()
