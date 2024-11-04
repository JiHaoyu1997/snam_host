import cv2

def resize_images_to_same_height(images):
    heights = [img.shape[0] for img in images]
    min_height = 480

    resized_images = []
    for img in images:
        scale = min_height / img.shape[0]
        new_width = int(img.shape[1] * scale)
        resized_img = cv2.resize(img, (new_width, min_height))
        resized_images.append(resized_img)
    
    return resized_images