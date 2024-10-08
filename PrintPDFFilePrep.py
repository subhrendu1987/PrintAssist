import os
import argparse
import sys

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
if __name__ == "__main__":
    # Parse the command-line argument
    parser = argparse.ArgumentParser(description="Prepare Large PDF file for both side printing in a single function printer.")
    parser.add_argument("-f", "--file", help="Path to the PDF file")
    parser.add_argument("-b", "--batch", type=int, default=None, help="Print page size for each batch")
    parser.add_argument("-p", "--print", action="store_true", help="Print the files one after another and wait till it completes")

    args = parser.parse_args()
    args.file="Input/Wrox.Professional.Linux.Kernel.Architecture.Oct.2008.pdf"
    # Call the function to create the folder
    create_folder_for_pdf(args.file)
