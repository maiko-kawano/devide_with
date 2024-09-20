import cv2
import os
import shutil
from PIL import Image, ImageEnhance
import pyocr
import pyocr.builders
from pathlib import Path

print(os.getcwd())

def get_paths(input_dir, exts=None):
    paths = sorted([x for x in input_dir.glob("**/*")])
    if exts:
        paths = list(filter(lambda x: x.suffix in exts, paths))

    return paths

input_dir = Path(r"D:\kanoi\APEX\Outplayed\Apex Legends")

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

for path in get_paths(input_dir, exts=[".mp4"]):

    def save_frame_sec(video_path, sec, result_path):
        cap = cv2.VideoCapture(str(path))
        print(str(path))

        if not cap.isOpened():
            return

        os.makedirs(os.path.dirname(result_path), exist_ok=True)

        fps = cap.get(cv2.CAP_PROP_FPS)

        cap.set(cv2.CAP_PROP_POS_FRAMES, round(fps * sec))

        ret, frame = cap.read()

        if ret:
            cv2.imwrite(result_path, frame)
            return frame

   
    save_frame_sec(str(path), 11, r"D:\kanoi\APEX\APEX.jpg")
    
    path_tesseract = r"C:\Program Files\Tesseract-OCR"
    if path_tesseract not in os.environ["Path"].split(os.pathsep):
        os.environ["Path"] += os.pathsep + path_tesseract

    tools = pyocr.get_available_tools()
    tool = tools[0]

    builder = pyocr.builders.TextBuilder(tesseract_layout=6)
    img = Image.open(r"D:\kanoi\APEX\APEX.jpg")
    for n in range(20):
        img_box = img.crop((133, 768+n, 285, 875))
        new_img = img_box.resize((304, 174))
        img_g = new_img.convert('L')
        enhancer= ImageEnhance.Contrast(img_g)
        img_con = enhancer.enhance(1.0)
        img_rgb = img_con.convert("RGB")
        img_rgb.save(r"D:\kanoi\APEX\APEX_1.jpg")
        pixels = img_rgb.load()
        c_max = 155
        for j in range(img_rgb.size[1]):
            for i in range(img_rgb.size[0]):
                if (pixels[i, j][0] > c_max or pixels[i, j][1] > c_max or
                        pixels[i, j][0] > c_max):
                    pixels[i, j] = (255, 255, 255)
        enhancer= ImageEnhance.Contrast(img_rgb)
        img_con = enhancer.enhance(2.0)
        builder = pyocr.builders.TextBuilder(tesseract_layout=6)
        result = tool.image_to_string(img_con , lang='jpn+eng', builder=builder)
        result = result.replace(" ", "")
        print(result)

        if "クリバに" in result or "クリバ" in result:
            shutil.move(str(path), r"D:\kanoi\APEX\Buney")
            break

        if "POC" in result:
            shutil.move(str(path), r"D:\kanoi\APEX\POC")
            break


shutil.move(r"D:\kanoi\APEX\APEX.jpg", r"D:\kanoi\APEX\dustbox")
shutil.move(r"D:\kanoi\APEX\APEX_1.jpg", r"D:\kanoi\APEX\dustbox")
