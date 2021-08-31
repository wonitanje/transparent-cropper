from PIL import Image
from os import listdir, makedirs
from os.path import exists

# Create result folder if not exist
if not exists('cropped'):
  makedirs('cropped')

# For each image in folder
for img_name in listdir():
  format = img_name[img_name.rfind('.') + 1:]
  if not format in ['png', 'jpg', 'jpeg']: continue
  try:
    img = Image.open(f'{img_name}').convert('RGBA')
  except:
    continue
  print(f'working with {img_name}')
  img.load()

  # Constants of box
  top = [0, 0]
  left = [0, 0]
  right = [el - 1 for el in img.size]
  bottom = [el - 1 for el in img.size]

  def strip_format(input: str):
    if '.' not in input:
      return None
    idx = input.rindex('.')
    return input[:idx]

  # Pixel check for color
  def pixel_is_colorized(color):
    try:
      if color[3] == 0: return False
    except:
      if color == (255, 255, 255): return False
    return True

  # Find top
  while not pixel_is_colorized(img.getpixel(tuple(top))):
    top[0] += 1
    if top[0] >= img.size[0]:
      top[0] = 0
      top[1] += 1

  # Find left
  while not pixel_is_colorized(img.getpixel(tuple(left))):
    left[1] += 1
    if left[1] >= img.size[1]:
      left[1] = 0
      left[0] += 1

  # Find right
  while not pixel_is_colorized(img.getpixel(tuple(right))):
    right[1] -= 1
    if right[1] <= 1:
      right[1] = img.size[1] - 1
      right[0] -= 1

  # Find bottom
  while not pixel_is_colorized(img.getpixel(tuple(bottom))):
    bottom[0] -= 1
    if bottom[0] <= 1:
      bottom[0] = img.size[0] - 1
      bottom[1] -= 1

  # Crop
  img_box = (left[0]-15, top[1]-15, right[0]+15, bottom[1]+15)
  print(f'{img.size=}\ncropping by {img_box}\n')
  cropped_size = (img_box[2] - img_box[0], img_box[3] - img_box[1])

  cropped = Image.new('RGBA', cropped_size, (255, 255, 255))

  img_pos = tuple(map(lambda x: -x, img_box[:2]))
  cropped.paste(img, img_pos, img)
  cropped.convert('RGB').save(f'cropped/{strip_format(img_name)}.jpg')