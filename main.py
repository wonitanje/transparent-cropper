from PIL import Image
from os import listdir, makedirs
from os.path import exists
from functools import reduce

def strip_format(input: str):
  if '.' not in input:
    return None
  idx = input.rindex('.')
  return input[:idx].lower()

if __name__ == '__main__':
  skipped = []
  broken = []
  success = 0
  result_folder_name = 'cropped'

  # Create result folder if not exist
  if not exists(result_folder_name):
    makedirs(result_folder_name)

  folder_list = listdir()
  print(' Выберите режим работы')
  print(' [1] Обработать все изображения (по умолчанию)')
  print(' [2] Обработать только новые изображения')
  if input('- Введите 1 или 2: ').strip() == '2':
    print(f" Обрабатываю только недостающие в папке '{result_folder_name}' изображения")
    processed_list = [strip_format(item) for item in listdir(result_folder_name)]
    folder_list = [item for item in folder_list if strip_format(item) not in processed_list]

  # For each image in folder
  for img_name in folder_list:
    format = img_name.lower()[img_name.rfind('.') + 1:]
    if not format in ['png', 'jpg', 'jpeg']:
      skipped.append(img_name)
      continue
    try:
      img = Image.open(f'{img_name}').convert('RGBA')
    except:
      broken.append(img_name)
      continue
    print(f' Обрабатываю файл {img_name}')
    success += 1
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
      return reduce(lambda sum, deep: sum + deep % 255, color, 0) > 10

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
    cropped_size = (img_box[2] - img_box[0], img_box[3] - img_box[1])

    cropped = Image.new('RGBA', cropped_size, (255, 255, 255))
    print(f' Перевожу\nИз: {img.size}\nВ: {cropped.size}\n Координаты обрезки: {img_box}\n\n')

    img_pos = tuple(map(lambda x: -x, img_box[:2]))
    cropped.paste(img, img_pos, img)
    cropped.convert('RGB').save(f'cropped/{strip_format(img_name)}.jpg')
    img.close()
    cropped.close()

  print(' Программа завершила работу')
  print(f' {success} изображений отредактированно')
  print(f' {len(broken)} изображений не удалось отредактировать')
  print(f' {len(skipped)} файлов прощенно')

  if '1' in input("\n- Введите '1', чтобы показать неотредактированные и пропущенные файлы: "):
    print('\n Неотредактированные изображения:')
    for (idx, item) in enumerate(broken):
      print(f'{idx}: {item}')

    print('\n Пропущенные файлы:')
    for (idx, item) in enumerate(skipped):
      print(f'{idx}: {item}')

  input("\n- Нажмите 'Enter', чтобы закрыть программу ")