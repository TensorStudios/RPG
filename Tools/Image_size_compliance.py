from PIL import Image
import re
import os

# img = Image.new("RGBA", (384, 192), color=(0,0,0,0))
# existing_img = Image.open("Test.png")
#
# img.paste(existing_img,(96,0))
#
# img.save("test_a.png")

pattern = re.compile(r"\((\d+)\)")
path = "C:\\Users\\CDOSUser\\PycharmProjects\\RPG\\img\\Knight"
folders = [
    "Attack_Left",
    "Attack_Right",
    "Idle_Left",
    "Idle_Right",
    "Walk_Left",
    "Walk_Right",
]

for folder in folders:
    dir_in_str = f"{path}\\{folder}"
    directory = os.fsencode(dir_in_str)
    for file in os.listdir(directory):
        full_path = f"{dir_in_str}\\{os.fsdecode(file)}"
        temp_img = Image.open(full_path)
        size = temp_img.size
        if size == (192, 192):
            new_img = Image.new("RGBA", (384, 192), color=(0, 0, 0, 0))
            new_img.paste(temp_img, (96, 0))
            print(f"saving: {os.fsdecode(file)}")
            new_img.save(full_path)
