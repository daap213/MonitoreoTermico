import cv2
import os

input_images_path = "D:/ESPOL/Tesis/prueba_opencv/img_train_org"
files_names = os.listdir(input_images_path)
print(files_names)

output_images_path = "D:/ESPOL/Tesis/prueba_opencv/modelo/p"
if not os.path.exists(output_images_path):
    os.makedirs(output_images_path)
    print("Directorio creado: ", output_images_path)

count = 0
for file_name in files_names:
    print(file_name)

    image_path = input_images_path + "/" + file_name
    print(image_path)
    image = cv2.imread(image_path)
    if not(image is None):

        image = cv2.resize(image, (640, 480)) 
        flip0 = cv2.flip(image,0) 
        flip1 = cv2.flip(image,1) 
        flip_1 = cv2.flip(image,-1) 
        
        cv2.imwrite(output_images_path + "/image" + str(count) + ".jpg", image)
        cv2.imwrite(output_images_path + "/image_180_" + str(count) + ".jpg", flip0)
        cv2.imwrite(output_images_path + "/image_esp_" + str(count) + ".jpg", flip1)
        cv2.imwrite(output_images_path + "/image_180esp_" + str(count) + ".jpg", flip_1)
        count += 1
        
cv2.destroyAllWindows()