import os
import subprocess
import hashlib
import shutil

CURRENT_PATH = os.path.normpath(os.path.dirname(__file__))
VOLUME_PATH = os.path.join(CURRENT_PATH, 'volume')

model = 'realesrgan-x4plus-anime'
chainFolders = ['x4', 'x16']

executor = os.path.join(CURRENT_PATH, 'realesrgan-ncnn-vulkan.exe')

def files(path):
    return next(os.walk(path))[2]

names = files(os.path.join(VOLUME_PATH, 'input'))
hashes = {}

def encode(name):
    return hashlib.md5(name.encode()).hexdigest() + '.' +  name.split('.')[-1]

for name in names:
    hashes[encode(name)] = name

def createFolder(name):
    if not os.path.exists(name):
        os.makedirs(name, exist_ok=True)


createFolder(os.path.join(VOLUME_PATH, 'renamed'))

for name in names:
    respath = os.path.join(VOLUME_PATH, 'renamed', encode(name))
    if not os.path.exists(respath):
        shutil.copyfile(src=os.path.join(VOLUME_PATH, 'input', name), dst=respath)

prevscale = 'renamed'
for scalename in chainFolders:
    in_path = os.path.join(VOLUME_PATH, prevscale)
    out_path = os.path.join(VOLUME_PATH, scalename)
    createFolder(out_path)
    for name in files(in_path):
        output_file_name = os.path.join(out_path, name)
        input_file_name = os.path.join(in_path, name)
        if not os.path.exists(output_file_name):
            subprocess.call([executor, '-i', input_file_name, '-o',output_file_name, '-n', model])
    prevscale = scalename


final_folder = os.path.join(VOLUME_PATH, prevscale)
response_folder = os.path.join(VOLUME_PATH, 'response' + prevscale)
createFolder(response_folder)

for name in files(final_folder):
    if name in hashes:
        resp_file = os.path.join(response_folder, hashes[name])
        if not os.path.exists(resp_file):
            shutil.copyfile(src=os.path.join(final_folder, name), dst=resp_file)
