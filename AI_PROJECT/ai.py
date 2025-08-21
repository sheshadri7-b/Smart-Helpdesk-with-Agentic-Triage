import fitz  # PyMuPDF
import json
import os
from PIL import Image
import io

def analyze_pdf_content(pdf_path, output_dir):
    """
    Analyzes a PDF to extract text and images, and organizes the output
    into a structured JSON file as per the assignment requirements.

    Args:
        pdf_path (str): The file path for the input PDF.
        output_dir (str): The directory to save extracted images and the JSON file.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # The main list that will hold our structured data
    structured_output = []

    try:
        # Open the provided PDF file
        doc = fitz.open(pdf_path)
        print(f"Successfully opened '{pdf_path}'. Processing {len(doc)} pages...")

        # Part 1: PDF Content Extraction [cite: 10]
        # Loop through each page of the document
        for page_num, page in enumerate(doc):
            page_data = {
                "page": page_num + 1,
                "text": "",
                "images": []
            }

            # 1. Text Extraction [cite: 13]
            page_data["text"] = page.get_text("text").strip()

            # 2. Image Extraction [cite: 14]
            image_list = page.get_images(full=True)

            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                # Create an image file name
                image_filename = f"page{page_num + 1}_image{img_index + 1}.png"
                image_path = os.path.join(output_dir, image_filename)

                # Save the image as a separate file [cite: 15]
                try:
                    image = Image.open(io.BytesIO(image_bytes))
                    image.save(open(image_path, "wb"), format='PNG')
                    # Add the file path to our page data
                    page_data["images"].append(image_path)
                except Exception as e:
                    print(f"Warning: Could not save image on page {page_num + 1}. Error: {e}")

            # Add the processed page data to our main list
            structured_output.append(page_data)

        # 3. Structured Output: Create a JSON file [cite: 16]
        json_output_path = os.path.join(output_dir, "extracted_content.json")
        with open(json_output_path, 'w') as f:
            json.dump(structured_output, f, indent=4)

        print(f"\n✅ Processing complete!")
        print(f"Images and JSON file saved in the '{output_dir}' directory.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'doc' in locals():
            doc.close()

# --- Main execution ---
if __name__ == "__main__":
    # Per the assignment, the script should process this specific file 
    PDF_FILE = "IMO class 1 Maths Olympiad Sample Paper 1 for the year 2024-25.pdf"
    OUTPUT_FOLDER = "output"

    if os.path.exists(PDF_FILE):
        analyze_pdf_content(PDF_FILE, OUTPUT_FOLDER)
    else:
        print(f"Error: The file '{PDF_FILE}' was not found.")
        print("Please place the PDF in the same directory as this script and run again.")
