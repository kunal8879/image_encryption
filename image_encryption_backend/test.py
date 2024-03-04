import requests

url = 'http://127.0.0.1:8000/image/encrypt'

image_path = 'images/06.jpg'

with open(image_path, 'rb') as f:
    image_data = f.read()

file = {'image': image_data}

response = requests.post(url, files=file, data={'extention': '.jpg'})
print(response.text)
print(response)

if response.status_code == 200:
    print("Image uploaded successfully")
else:
    print("Failed to upload image:", response.text) 