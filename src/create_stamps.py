from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from itertools import product



def create_pdf(product_stamp:str, file_name:str, folder:str):
    """ Generate a PDF file with the stamps organized in a grid. The PDF is saved in given folder 

    Args:
        product_stamp (str): Text of the stamp
        file_name (str): Name of the pdf file generated
        folder (str): Folder path where the pdf file will be stored
    """
    # File main settings
    file_path = f'{folder}/{file_name}.pdf'
    pdf = canvas.Canvas(file_path, pagesize=letter)
    pdf.setTitle(file_name)

    #------------------------------------------------------------
    # Line grid
    #------------------------------------------------------------

    # Line Color
    pdf.setStrokeColor('#f3f3f3') 

    # Boundaries of the grid

    ## Width dimensions
    stamps_width = 21/8
    num_stamps_w = 3
    blank_space = 1/8
    num_spaces = 2

    grid_width = stamps_width*num_stamps_w + blank_space*num_spaces
    x_inf = (17/2 - grid_width ) / 2
    x_sup = x_inf + grid_width

    ## Height dimensions
    stamps_height = 1
    num_stamps_h = 10
    grid_height = stamps_height*num_stamps_h
    y_inf = (11 - grid_height)/2
    y_sup = y_inf + grid_height


    # Horizontal lines
    for i in range(num_stamps_h+1):
        pdf.line(
            x_inf*inch,
            (y_inf + i*stamps_height)*inch,
            x_sup*inch,
            (y_inf + i*stamps_height)*inch
        )

    # Vertical lines
    for i in range(num_stamps_w):
        # Left vertical line of each stamp
        pdf.line(
            (x_inf + i*(stamps_width+blank_space))*inch,
            y_inf*inch,
            (x_inf + i*(stamps_width+blank_space))*inch,
            y_sup*inch
        )
        # Right vertical line of each stamp
        pdf.line(
            (x_inf + (i+1)*stamps_width + i*blank_space)*inch,
            y_inf*inch,
            (x_inf + (i+1)*stamps_width + i*blank_space)*inch,
            y_sup*inch
        )


    #------------------------------------------------------------
    # Texts
    #------------------------------------------------------------

    

    heights = [ y_inf + stamps_height/2 + stamps_height * i for i in range(num_stamps_h)]

    x_positions = [ x_inf + stamps_width/2 + 
                i*(stamps_width+blank_space) for i in range(num_stamps_w) ]

    # Loop to decrease Font size until textwidth is smaller than stamp width
    font_size = 28
    pdf.setFont('Helvetica-Bold', font_size)
    text_width = pdf.stringWidth(product_stamp)
    
    while text_width > stamps_width*inch:
        font_size = font_size - 1
        pdf.setFont('Helvetica-Bold', font_size)
        text_width = pdf.stringWidth(product_stamp)
        

    for x,y in product(x_positions, heights):
        pdf.drawString(
            x*inch - text_width/2, 
            y*inch - 1/8*inch, 
            product_stamp
        )

    # Save pdf
    pdf.save()
    



