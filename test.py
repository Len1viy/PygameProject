# from PIL import Image
#
#
# img = Image.open("data/imgs/archive/Cells_with_borders.png")
# for x in range(img.width // 32):
#     new_img = img.crop((x * 32, 0, (x + 1) * 32, 32))
#     new_img.save(f"file{x + 1}.png")