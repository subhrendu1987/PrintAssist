### e.g. python3 PrintPDFFilePrep.py -f Input/abc.pdf -b 500

import os
import argparse
import sys
from PyPDF2 import PdfReader, PdfWriter
import platform
import subprocess
import shutil
########################################################################
def split_into_batches(start,N,batch_size):
    if(batch_size==None):
        return([{'start': start, 'end': N}])
    batchRange=[]
    for i in range(start, N, batch_size):
        st = i
        end = min(i + batch_size - 1, N)
        batchRange.append({'start': st, 'end': end})
    return(batchRange)
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
def split_odd_even_pages(pdf_file, output_file=None,start=0,end=None):
    #print(f"Debug args: {pdf_file} , {output_file}, {start},{end}")
    return_files={}
    try:
        # Open the PDF file
        reader = PdfReader(pdf_file)
        writer = PdfWriter()

        # Get the total number of pages in the PDF
        num_pages = len(reader.pages)
        if(output_file==None):
            return(num_pages)
        # Extraction Range processing
        end = num_pages if end is None else end

        path,op_filename=extract_path_and_filename(output_file)
        # Odd Page processing
        odd_pages= [page for page in range(start,end) if (page) % 2 != 0]
        odd_output_file=modify_filename(output_file,"Odd_","_%d-%d"%(start,end))
        # Add the reversed even pages to the writer
        for page_num in odd_pages:
            writer.add_page(reader.pages[page_num])

        with open(odd_output_file, "wb") as output_pdf:
            writer.write(output_pdf)
        #print(f"Odd pages are saved to '{odd_output_file}'")
        return_files["odd"]=odd_output_file

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
        return_files["even"]=even_output_file

    except Exception as e:
        print(f"Error processing PDF file: {e}")
    return(return_files)
########################################################################
def open_pdf_and_wait(file_path):
    try:
        if platform.system() == 'Windows':
            # On Windows, 'start' opens files with the default application
            subprocess.run(['start', file_path], check=True, shell=True)
        elif platform.system() == 'Darwin':  # macOS
            # On macOS, 'open' opens files with the default application
            subprocess.run(['open', file_path], check=True)
        else:  # Linux and other Unix-like systems
            # On Linux, 'xdg-open' opens files with the default application
            subprocess.run(['xdg-open', file_path], check=True)
    except Exception as e:
        print(f"Failed to open the file: {e}")
########################################################################
if __name__ == "__main__":
    # Parse the command-line argument
    parser = argparse.ArgumentParser(description="Prepare Large PDF file for both side printing in a single function printer.")
    parser.add_argument("-f", "--file", help="Path to the PDF file")
    parser.add_argument("-b", "--batch", type=int, default=None, help="Print page size for each batch")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start from page")
    parser.add_argument("-e", "--end", type=int, default=100000, help="End at page")
    parser.add_argument("-p", "--print", action="store_true", help="Print the files one after another and wait till it completes")
    parser.add_argument("-c", "--clean", action="store_true", help="Cleanup after printing")

    args = parser.parse_args()
    #args.file="Input/Wrox.Professional.Linux.Kernel.Architecture.Oct.2008.pdf"
    TotalPages=min(split_odd_even_pages(args.file),(args.end-1))
    start=max((args.start-1),0)
    print(f"Total pages: {TotalPages}")
    Target_folder=create_folder_for_pdf(args.file)
    batchRange=split_into_batches(start,TotalPages,args.batch)
    ListOfFiles=[]
    for i,entry in enumerate(batchRange):
        print(f"Processing Batch No. : {i} {entry}")
        ListOfFiles.append(split_odd_even_pages(args.file,output_file=Target_folder+"/ALL.pdf",start=entry["start"],end=entry["end"]))
    print(ListOfFiles)
    if(args.print):
        print(f'Print job starting')
        for i,e in enumerate(ListOfFiles):
            print(f"Processing Batch No. : {i} {e}")
            print("Print Even pages first")
            open_pdf_and_wait(e["even"])
            response = input("Re-insert printed pages and press 'y' to continue?: ").strip().lower()
            if response != 'y':
                break
            else:
                print("Print ODD pages")
                open_pdf_and_wait(e["odd"])
            response = input("Press 'y' to continue with next batch?: ").strip().lower()
            if response != 'y':
                break
    if(args.clean):
        try:
            shutil.rmtree(Target_folder)
            print(f"Folder '{Target_folder}' and all its contents have been deleted.")
        except Exception as e:
            print(f"Error deleting folder: {e}")