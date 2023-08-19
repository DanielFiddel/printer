import streamlit as st
from PIL import Image
import subprocess
import tempfile
import os

def resize_and_dither(image):
    # Resize the image to 696 width while maintaining the aspect ratio
    new_width = 696
    aspect_ratio = image.width / image.height
    new_height = int(new_width / aspect_ratio)
    resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

    # Convert the resized image to grayscale
    resized_grayscale_image = resized_image.convert("L")

    # Apply Floyd-Steinberg dithering
    dithered_image = resized_grayscale_image.convert("1", dither=Image.FLOYDSTEINBERG)
    
    return resized_image, dithered_image

def print_image(image):
    # Save the image to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        temp_file_path = temp_file.name
        image.save(temp_file_path, "PNG")
        
    # Construct the print command
    command = f"brother_ql -b pyusb --model QL-570 -p usb://0x04f9:0x2028/000M6Z401370 print -l 62 \"{temp_file_path}\""
    
    # Run the print command
    subprocess.run(command, shell=True)

# Streamlit app
st.title('Image Resizer and Dithering Tool')

uploaded_image = st.file_uploader("Choose an image file (png/jpg/gif)", type=['png', 'jpg', 'gif'])

if uploaded_image is not None:
    original_image = Image.open(uploaded_image).convert('RGB')
    resized_image, dithered_image = resize_and_dither(original_image)
    
    st.image(original_image, caption="Original Image")
    st.image(dithered_image, caption="Resized and Dithered Image")

    # Paths to save the original and dithered images in the 'temp' directory
    original_image_path = os.path.join('temp', 'original_image.png')
    dithered_image_path = os.path.join('temp', 'dithered_image.png')

    # Save both original and dithered images
    original_image.save(original_image_path, "PNG")
    dithered_image.save(dithered_image_path, "PNG")
    
    print(dithered_image_path)
    # Print options
    if st.button('Print Original Image'):
        print_image(original_image)
        st.success('Original image sent to printer!')

    if st.button('Print Dithered Image'):
        print_image(dithered_image)
        st.success('Dithered image sent to printer!')
