import os
import argparse
import sys
from PyPDF2 import PdfReader, PdfWriter
########################################################################
def modify_filename(full_path, prefix="", suffix=""):
    # Extract directory, filename without extension, and the extension
    directory = os.path.dirname(full_path)
    filename, ext = os.path.splitext(os.path.basename(full_path))
    
    # Add the prefix and suffix to the filename
    modified_filename = f"{prefix}{filename}{suffix}{ext}"
    
    # Combine the directory and the modified filename
    modified_full_path = os.path.join(directory, modified_filename)
    
    return modified_full_path
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
def split_odd_even_pages(pdf_file, output_file="output.pdf",start=0,end=None):
    return_files=[]
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


        # Odd Page processing
        odd_pages= [page for page in range(start,end) if (page) % 2 != 0]
        odd_output_file=modify_filename(output_file,"Odd_","_%d-%d"%(start,end))
        # Add the reversed even pages to the writer
        for page_num in odd_pages:
            writer.add_page(reader.pages[page_num])

        with open(odd_output_file, "wb") as output_pdf:
            writer.write(output_pdf)
        #print(f"Odd pages are saved to '{odd_output_file}'")
        return_files.append(odd_output_file)

        # Even page Processing
        reader = PdfReader(pdf_file)
        writer = PdfWriter()

        even_pages = [page for page in range(end-1,start,-1) if (page) % 2 == 0]
        # Add the reversed even pages to the writer
        for page_num in even_pages:
            writer.add_page(reader.pages[page_num])
        # Write the even pages to the output PDF file
        even_output_file=modify_filename(output_file,"Even_","_%d-%d_rev"%(start,end))
        with open(even_output_file, "wb") as output_pdf:
            writer.write(output_pdf)
        #print(f"Even pages in reverse order are saved to '{even_output_file}'")
        return_files.append(even_output_file)

    except Exception as e:
        print(f"Error processing PDF file: {e}")
    return(return_files)
########################################################################
########################################################################
if __name__ == "__main__":
    # Parse the command-line argument
    parser = argparse.ArgumentParser(description="Prepare Large PDF file for both side printing in a single function printer.")
    parser.add_argument("-f", "--file", help="Path to the PDF file")
    parser.add_argument("-b", "--batch", type=int, default=None, help="Print page size for each batch")
    parser.add_argument("-p", "--print", action="store_true", help="Print the files one after another and wait till it completes")

    args = parser.parse_args()
    #args.file="Input/Wrox.Professional.Linux.Kernel.Architecture.Oct.2008.pdf"

    Target_folder=create_folder_for_pdf(args.file)
    ListOfFiles=split_odd_even_pages(args.file,Target_folder+"/ALL.pdf")
    print(ListOfFiles)
