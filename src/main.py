import os
from pathlib import Path
from docx import Document

from create_stamps import create_pdf

def prompt_source_file() -> Path:
    """ Show in the console a list with all files in the lists-of-products folder and prompt
    the user to select one of these files to take the names of the products from it.

    Returns:
        Path: Path and name of the file with the names of the products
    """

    # Instructions for the user
    print('''
    Be sure to save a .docx or .txt file in the folder named lists-of-products 
    with the list of products which you want to create stamps for.
    ''')

    print('Select the file which contains the names of the products\n')
    
    # Show all files in the lists-of-products folder
    prod_lists_folder_path = Path('../lists-of-products')
    files = [f for f in prod_lists_folder_path.iterdir() if f.is_file()]

    for i, f in enumerate(files):
        print(f'{i}. {f.name}')
    
    print('')

    # Prompt index of source file from the user
    file_index = ''
    while file_index not in list(range(0,i+1)):
        file_index = int(input(f'Select a number from 0 to {i}: '))

    # Return the path and name of the source file
    source_file = files[file_index]
    
    return source_file



def get_product_list_from_docx(source_file: Path) -> list[str]:
    """ Read a docx file and return a list of the texts in each line of the document """
    
    doc = Document(source_file) 
    product_list = [line.text.strip() for line in doc.paragraphs]
    
    return product_list



def get_product_list_from_txt(source_file: Path) -> list[str]:
    """ Read a txt file and return a list of the texts in each line of the file """
    
    product_list = list()
    with open(source_file, 'r') as file:
        for line in file:
            product_list.append(line.strip())
    
    return product_list



def create_stamps_folder(name:str) -> Path:
    """ Create a subfolder of results which name has the form 'stamps_from_{source_file}'. For example 'stamps_from_list123'.
    If the subfolder already exists in results folder, then a term '(new)' is added at the end. For example 'stamps_from_list123(new)'

    Args:
        name (str): Name of the source file 

    Returns:
        Path: Path of the new subfolder as a Path class of pathlib package 
    """
    
    new_dir = f'stamps_from_{name}'
    results_path = Path('../results')

    # If the new folder already exists in the results folder, then add "(new)" at the end of the subfolder name
    results_folders = [folder.name for folder in results_path.iterdir() if not folder.is_file()]
    while new_dir in results_folders:
        new_dir = f'{new_dir}(new)'
    
    # Create the new subfolder in the results folder
    stamps_folder = f'../results/{new_dir}'
    os.mkdir(stamps_folder)
    
    return Path(stamps_folder)
        
    
    
def main():
    source_file = prompt_source_file()
    
    if source_file.suffix == '.txt':
        product_list = get_product_list_from_txt(source_file)
    
    elif source_file.suffix == '.docx':
        product_list = get_product_list_from_docx(source_file)
    
    else:
        print('Format of source file is incompatible, use a .txt file or a .docx file.')
        return

    if len(product_list) == 0:
        print('File is empty')
    
    # The PDF files which contains the stamps for each product are stored in a subfolder of results folder called stamps_from_source_file_name_
    name_stamps_sub_folder = source_file.name.split('.')[0]
    stamps_folder = create_stamps_folder(name_stamps_sub_folder)
    
    for prod in product_list:
        create_pdf(prod, prod, stamps_folder)
    


if __name__ == "__main__":
   main()