from PIL import Image
import statistics

# Load the image
image_path = "saved_photos/latka.png"  # change to your actual file name/path
img = Image.open(image_path).convert("RGB")
pixels = list(img.getdata())

# Separate the channels
reds = [p[0] for p in pixels]
greens = [p[1] for p in pixels]
blues = [p[2] for p in pixels]

# Compute mean RGB
mean_r = sum(reds) / len(reds)
mean_g = sum(greens) / len(greens)
mean_b = sum(blues) / len(blues)
mean_rgb = (int(mean_r), int(mean_g), int(mean_b))

# Compute median RGB
median_r = int(statistics.median(reds))
median_g = int(statistics.median(greens))
median_b = int(statistics.median(blues))
median_rgb = (median_r, median_g, median_b)

# Compute mode RGB
mode_r = statistics.mode(reds)
mode_g = statistics.mode(greens)
mode_b = statistics.mode(blues)
mode_rgb = (mode_r, mode_g, mode_b)

# Find min and max RGB
min_r = min(reds)
min_g = min(greens)
min_b = min(blues)
min_rgb = (min_r, min_g, min_b)

max_r = max(reds)
max_g = max(greens)
max_b = max(blues)
max_rgb = (max_r, max_g, max_b)

def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(rgb[0], rgb[1], rgb[2])

print("Mean RGB:", mean_rgb, "Hex:", rgb_to_hex(mean_rgb))
print("Median RGB:", median_rgb, "Hex:", rgb_to_hex(median_rgb))
print("Mode RGB:", mode_rgb, "Hex:", rgb_to_hex(mode_rgb))
print("Min RGB:", min_rgb, "Hex:", rgb_to_hex(min_rgb))
print("Max RGB:", max_rgb, "Hex:", rgb_to_hex(max_rgb))
