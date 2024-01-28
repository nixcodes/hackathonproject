import os
import boto3
import subprocess
import openpyxl
import pytesseract
from PIL import Image


# Initialize S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id='AKIAXYNPLMJNG52VCO6B',
    aws_secret_access_key='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'
)

bucket_name = 'loanprocessingapp'
source_directory_path = 'documents/'
destination_directory_path = 'ProcessedDocuments/'

temp_dir = 'temp_images'
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

extracted_data = []

def download_images_from_s3(bucket_name, directory_path):
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=directory_path)

    for obj in response.get('Contents', []):
        key = obj['Key']
        filename = os.path.basename(key)
        download_path = os.path.join(temp_dir, filename)
        
        s3.download_file(bucket_name, key, download_path)
        print(f"Downloaded file: {filename}")
        
        process_image(download_path)

def process_image(image_path):
    try:
        # Use pytesseract to perform OCR on the image
        text = pytesseract.image_to_string(Image.open(image_path))
        
        print(f"Text extracted from {image_path}:\n{text}")
        
        fn_index = text.find("FN")
        ln_index = text.find("LN")
        if fn_index != -1 and ln_index != -1:
            fn_value = text[fn_index + 3:ln_index].strip()
            ln_value = text[ln_index + 3:].strip()
            extracted_data.append({'First Name': fn_value, 'Last Name': ln_value})
    except Exception as e:
        print(f"Error processing image {image_path}: {str(e)}")

def write_to_excel(data):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['First Name', 'Last Name'])
    for item in data:
        ws.append([item['First Name'], item['Last Name']])
    excel_file = os.path.join(temp_dir, 'extracted_data.xlsx')
    wb.save(excel_file)
    print(f"Excel file saved: {excel_file}")
    return excel_file

def upload_to_s3(bucket_name, file_path):
    s3.upload_file(file_path, bucket_name, f"{destination_directory_path}{os.path.basename(file_path)}")
    print(f"Uploaded file to S3: {destination_directory_path}{os.path.basename(file_path)}")

if __name__ == "__main__":
    download_images_from_s3(bucket_name, source_directory_path)
    excel_file_path = write_to_excel(extracted_data)
    upload_to_s3(bucket_name, excel_file_path)
