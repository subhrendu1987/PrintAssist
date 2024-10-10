import os
import argparse
import sys
from PyPDF2 import PdfReader, PdfWriter
########################################################################
def extract_path_and_filename(full_path):
    directory = os.path.dirname(full_path)
    filename = os.path.basename(full_path)
    return directory, filename
########################################################################
def create_folder_for_pdf(pdf_path):
    # Get the directory and the filename without the extension
    folder_name = os.path.splitext(os.path.basename(pdf_path))[0]
    folder_path = os.path.join(os.path.dirname(pdf_path), folder_name)

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_name}' created at '{folder_path}'")
    else:
        print(f"Folder '{folder_name}' already exists.")
    return(folder_path)
########################################################################
def split_odd_even_pages(pdf_file, output_file="ALL.pdf",start=0,end=None):
    path,op_filename=extract_path_and_filename(output_file)
    try:
        # Open the PDF file
        reader = PdfReader(pdf_file)
        writer = PdfWriter()

        # Get the total number of pages in the PDF
        num_pages = len(reader.pages)
        if(output_file==None):
            return(num_pages)
        end=num_pages if(end==None) else None
        # Collect even-numbered pages in reverse order
        odd_pages= [page for page in range(start,end) if (page) % 2 != 0]
        # Collect even-numbered pages in reverse order
        even_pages = [page for page in range(end,start,-1) if (page + 1) % 2 == 0]

        # Add the reversed even pages to the writer
        for page_num in even_pages:
            writer.add_page(reader.pages[page_num])

        # Write the even pages to the output PDF file
        with open(output_file, "wb") as output_pdf:
            writer.write(output_pdf)

        print(f"Even pages in reverse order saved to '{output_file}'")

    except Exception as e:
        print(f"Error processing PDF file: {e}")
########################################################################
########################################################################
if __name__ == "__main__":
    # Parse the command-line argument
    parser = argparse.ArgumentParser(description="Prepare Large PDF file for both side printing in a single function printer.")
    parser.add_argument("-f", "--file", help="Path to the PDF file")
    parser.add_argument("-b", "--batch", type=int, default=None, help="Print page size for each batch")
    parser.add_argument("-p", "--print", action="store_true", help="Print the files one after another and wait till it completes")

    args = parser.parse_args()
    args.file="Input/Wrox.Professional.Linux.Kernel.Architecture.Oct.2008.pdf"

    Target_folder=create_folder_for_pdf(args.file)
    extract_even_pages_in_reverse(args.file,Target_folder+"/ALL.pdf")
