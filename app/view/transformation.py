import os


path_images_directory = os.path.abspath('images')
path_xml_directory = os.path.abspath('xml')
files = os.listdir(path_images_directory)
for file in files:
    if file.endswith(".png"):
        file_png_path = os.path.join(path_images_directory, file)
        file_tsx = open(os.path.join(path_xml_directory, file.split('.png')[0] + '.tsx'), mode='w')
        template = f'''<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.11.1" name="{file.split('.')[0]}" tilewidth="32" tileheight="32" tilecount="275" columns="11">
 <image source="{file_png_path}" width="382" height="805"/>
</tileset>
'''
        file_tsx.write(template)



