import os
from PIL import Image, ExifTags
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def correct_image_orientation(img):
    # Check if the image has EXIF metadata
    if hasattr(img, '_getexif'):
        exif = img._getexif()
        if exif is not None:
            for tag, value in exif.items():
                tag_name = ExifTags.TAGS.get(tag)
                if tag_name == 'Orientation':
                    # Rotate the image based on the orientation tag
                    if value == 3:
                        img = img.rotate(180, expand=True)
                    elif value == 6:
                        img = img.rotate(270, expand=True)
                    elif value == 8:
                        img = img.rotate(90, expand=True)
                    break

    return img

def get_image_dimensions(img, max_width, max_height):
    img_width, img_height = img.size

    # Calculate the scaling factor for width and height
    width_scale = max_width / img_width
    height_scale = max_height / img_height

    # Use the smaller scaling factor to maintain the image's aspect ratio
    scale = min(width_scale, height_scale)

    # Calculate the new dimensions
    new_width = int(img_width * scale)
    new_height = int(img_height * scale)

    return new_width, new_height

# Prevents same files from being overridden when saved to same destination 
def find_next_file_number(output_dir):
    # Get a list of files in the output directory
    existing_files = os.listdir(output_dir)
    file_numbers = []

    # Extract the file numbers from the existing filenames
    for file in existing_files:
        if file.lower().endswith(".pdf"):
            file_name, file_ext = os.path.splitext(file)
            try:
                file_number = int(file_name.split("file")[-1])
                file_numbers.append(file_number)
            except ValueError:
                pass

    # Find the next available file number
    next_file_number = max(file_numbers, default=0) + 1
    return next_file_number

def convert_jpg_to_pdf(input_dir, output_dir):
    images = [file for file in os.listdir(input_dir) if file.lower().endswith(".jpg")]

    if not images:
        print("No JPG images found in the input directory.")
        return

    for image in images:
        image_path = os.path.join(input_dir, image)
        img = Image.open(image_path)

        # Correct the image orientation if needed
        img = correct_image_orientation(img)

        # Get the PDF page size
        page_width, page_height = letter

        # Get the new image dimensions to fit within the PDF page
        img_width, img_height = get_image_dimensions(img, page_width, page_height)

        # Calculate margins to center the image on the page
        x_margin = (page_width - img_width) / 2
        y_margin = (page_height - img_height) / 2

        # Use the original filename (without extension) as the PDF name
        pdf_name = os.path.splitext(image)[0]
        output_path = os.path.join(output_dir, pdf_name + ".pdf")

        c = canvas.Canvas(output_path, pagesize=letter)
        c.drawImage(image_path, x_margin, y_margin, width=img_width, height=img_height)
        c.showPage()
        c.save()

    print("PDFs generated successfully.")


if __name__ == "__main__":
    input_directory = "/Users/jonathan/Desktop/JPG2PDF/JPG"
    output_directory = "/Users/jonathan/Desktop/JPG2PDF/PDF"
   

    convert_jpg_to_pdf(input_directory, output_directory)
