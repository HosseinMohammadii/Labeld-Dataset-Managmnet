from PIL import Image

input_ad = '/home/hossein/yolo/raw_datasets/TestIJCNN2013/TestIJCNN2013/'
output_ad = '/home/hossein/yolo/gtsdb/converted_test/'

i = 0

for i in range(0, 300):
    if i > -1 and i < 10:
        s = '0000'
    elif i > 9 and i < 100:
        s = '000'
    elif i > 99 and i < 1000:
        s = '00'


      
    name = s + str(i) 
    im = Image.open(input_ad + name + ".ppm")
    
    name2 = "gtsdb-00" + str(i + 600)
    im2 = im.resize((1360, 800))
    im2.save(output_ad + name2 + ".png")
    
    print("image", i, "proccesed")


