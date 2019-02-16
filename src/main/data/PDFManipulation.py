from typing import Tuple

import pyPdf
from pdf2image import convert_from_path


def crop_page(page,
              lower: Tuple[int, int] = None,
              upper: Tuple[int, int] = None):
    if lower is None:
        lower = page.mediaBox.lowerLeft
    if upper is None:
        upper = page.mediaBox.upperRight
    new_page = page
    new_page.mediaBox.upperRight = upper
    new_page.mediaBox.lowerLeft = lower
    new_page.cropBox.upperRight = upper
    new_page.cropBox.lowerLeft = lower
    new_page.trimBox.upperRight = upper
    new_page.trimBox.lowerLeft = lower
    return new_page


def crop_all(pages: [int],
             lower: Tuple[int, int] = None,
             upper: Tuple[int, int] = None):
    new_pages = []
    for page in pages:
        new_pages.append(crop_page(page, lower, upper))
    return new_pages


def select_pages(input_path: str, page_numbers: [int]):
    pages = []
    with open(input_path, "rb") as pdf:
        pdf_reader = pyPdf.PdfFileReader(pdf)
        for i in page_numbers:
            page = pdf_reader.getPage(i)
            pages.append(page)
    return pages


def output_pages(pages: [int], output_path: str):
    with open(output_path, "wb") as page_file:
        output = pyPdf.PdfFileWriter()
        for page in pages:
            output.addPage(page)
        output.write(page_file)


def output_page_number(pdf_input_path: str, pdf_output: str, page_number: int):
    page = select_pages(pdf_input_path, [page_number])
    output_pages([page], pdf_output)


def crop_and_output_pages(input_path: str, output_path: str, page_numbers: [int],
                          lower: Tuple[int, int] = None,
                          upper: Tuple[int, int] = None):
    pages = select_pages(input_path, page_numbers)
    pages = crop_all(pages, lower, upper)
    output_pages(pages, output_path)


def pdf2img(input_path, output_path):
    pages = convert_from_path(input_path, 500)

    for page in pages:
        page.save(output_path, 'JPEG')
        break
