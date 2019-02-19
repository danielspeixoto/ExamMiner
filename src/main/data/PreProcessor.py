import os

from PyPDF2 import PdfFileReader, PdfFileWriter

from data import PDFManipulation


class PreProcessor:

    def __init__(self, working_dir: str,
                 one_column_pages: [int],
                 excluded_pages: [int]):

        os.makedirs(working_dir, exist_ok=True)
        self.working_dir = working_dir
        self.left_column_pdf = working_dir + "left.pdf"
        self.right_column_pdf = working_dir + "right.pdf"
        self.one_column_pdf = working_dir + "one.pdf"
        self.one_column_pages = one_column_pages
        self.excluded_pages = excluded_pages

    @staticmethod
    def _remove_pages(all_pages, excluded) -> [int]:
        pages = []
        for page in all_pages:
            if page not in excluded:
                pages.append(page)
        return pages

    def pre_process(self, input_path: str, working_pdf: str):
        with open(input_path, 'rb') as input_pdf:
            pdf_file = PdfFileReader(input_pdf)
            all_pages = range(pdf_file.numPages)

            # Two-column page, gets left side
            PDFManipulation.crop_and_output_pages(
                input_path,
                self.left_column_pdf,
                self._remove_pages(all_pages,
                                   self.excluded_pages + self.one_column_pages),
                (55, 60), (310, 750)
            )

            # Two-column page, gets right side
            PDFManipulation.crop_and_output_pages(
                input_path,
                self.right_column_pdf,
                self._remove_pages(all_pages, self.excluded_pages + self.one_column_pages),
                (315, 60), (570, 750)
            )

            # One-column page, grabs entire page
            PDFManipulation.crop_and_output_pages(
                input_path,
                self.one_column_pdf,
                self.one_column_pages,
                (55, 60), (570, 750))


        one_column_pages = 0
        two_column_pages = 0

        left_column_pdf = PdfFileReader(open(self.left_column_pdf, "rb"))
        right_column_pdf = PdfFileReader(open(self.right_column_pdf, "rb"))
        one_column_pdf = PdfFileReader(open(self.one_column_pdf, "rb"))
        output = PdfFileWriter()
        for page_index in all_pages:
            if page_index in self.excluded_pages:
                continue
            if page_index in self.one_column_pages:
                output.addPage(one_column_pdf.getPage(one_column_pages))
                one_column_pages += 1
            else:
                output.addPage(left_column_pdf.getPage(two_column_pages))
                output.addPage(right_column_pdf.getPage(two_column_pages))
                two_column_pages += 1

        with open(working_pdf, "wb") as working_file:
            output.write(working_file)
        os.remove(self.left_column_pdf)
        os.remove(self.right_column_pdf)
        os.remove(self.one_column_pdf)
