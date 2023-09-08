import pyautogui
import time
import pyperclip
import os
import argparse
import re
import glob
import img2pdf
from multiprocessing.pool import ThreadPool

def download_pages(pageNums=1801):
    ######## Also change this to the image src of the page
    url_template = "https://plus.pearson.com/eplayer/pdfassets/prod1/173621/ad9687cf-6a97-437d-8e18-be730bb1a994/pages/page{i}?password=&amp;accessToken=null&amp;formMode=true"
    urls = (url_template.format(i=i) for i in range(48, pageNums + 1))
    time.sleep(5)
    for url in urls:
        ######################### change this to the x,y of your url input --- so fukin gank ik 
        pyautogui.click(653, 98)
        pyperclip.copy(url)
        pyautogui.hotkey('command', 'v')
        pyautogui.press('enter')
        time.sleep(0.5)

def find_missing_pages(directory):
    os.chdir(directory)
    files = os.listdir()
    page_files = [f for f in files if f.startswith('page') and f.endswith('.png')]
    page_numbers = [int(f[4:-4]) for f in page_files]
    page_numbers.sort()
    missing_pages = [i for i in range(page_numbers[-1] + 1) if i not in page_numbers]
    return missing_pages


def convert_to_pdf(directory):
    os.chdir(directory)
    # for filename in os.listdir():
    #     name, ext = os.path.splitext(filename)
    #     os.rename(filename, f"{name}.png")
    file_name = os.path.basename(directory)
    pdf_path = f"{directory}/{file_name}.pdf"
    png_files = sorted(glob.glob(f"{directory}/*.png"))
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert([str(png_file) for png_file in png_files]))
    print("Saved pdf successfully")


def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]


def convert_to_pdf(download_dir):
    os.chdir(download_dir)
    for filename in os.listdir():
        name, ext = os.path.splitext(filename)
        os.rename(filename, f"{name}.png")
    
    file_name = os.path.basename(download_dir)
    pdf_path = f"{download_dir}/{file_name}.pdf"
    
    png_files = glob.glob(f"{download_dir}/*.png")
    png_files.sort(key=natural_sort_key)  # Sort using the natural_sort_key function
    
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert([str(png_file) for png_file in png_files]))

if __name__ == "__main__":
    # You can add argparse here to get pageNums, directory, and directory from the command line
    pageNums = 1801
    directory = '/Users/felix/Projects/Pearson-PDF-Downloader/book'
    
    # Download pages
    download_pages(pageNums)
    
    # Find missing pages
    missing_pages = find_missing_pages(directory)
    if missing_pages:
        print(f"Missing pages: {missing_pages}")
    else:
        print("No pages are missing.")
        
    # Convert to PDF
    convert_to_pdf(directory)
