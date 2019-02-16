import json
import os
from typing import Tuple, Dict

import pandas as pd
from pyPdf2 import PdfFileWriter, PdfFileReader, PdfFileMerger

from data import PDFManipulation
from data.PDFManipulation import crop_page


class Portion:

    def __init__(self):
        self.upper = None
        self.lower = None
        self.page = None

    def save_as_pdf(self, pdf_input_path, output_path):
        with open(pdf_input_path, "rb") as pdf_file:
            pdf_input = PdfFileReader(pdf_file)
            output = PdfFileWriter()

            page = pdf_input.getPage(self.page)
            page = crop_page(page, self.upper, self.lower)
            output.addPage(page)

            with open(output_path, "wb") as out_f:
                output.write(out_f)


class QuestionPortions:

    def __init__(self):
        self.parts = []
        self.number = None
        self.pdf_file = None

    def add_part(self, part: Portion):
        self.parts.append(part)

    def save_as_pdf(self, pdf_input_path, output_path):
        i = 0
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        for part in self.parts:
            part.meta2pdf(pdf_input_path,
                          output_path + "/" +
                          str(i) + ".pdf")
            i += 1

        merger = PdfFileMerger()
        for i in range(len(self.parts)):
            merger.append(
                PdfFileReader(
                    open(
                        output_path + "/" + str(i) + ".pdf", 'rb'
                    )
                )
            )
        merger.write(output_path + "/" + "question.pdf")
        for i in range(len(self.parts)):
            os.remove(
                output_path + "/" + str(i) + ".pdf"
            )


class MetaQuestion:

    def __init__(self,
                 portions: QuestionPortions,
                 exam: str,
                 edition: int,
                 variant: str,
                 part: int,
                 number: int,
                 answer: int,
                 tags: [str]
                 ):
        self.portions = portions
        self.exam = exam
        self.edition = edition
        self.variant = variant
        self.part = part
        self.number = number
        self.answer = answer
        self.tags = tags

    def metadata_to_dict(self) -> Dict:
        return {
            "exam": self.exam,
            "edition": self.edition,
            "variant": self.variant,
            "part": self.part,
            "number": self.number,
            "answer": self.answer,
            "tags": self.tags
        }


class MetadataFormatter:
    def format(self, questions: [QuestionPortions]) -> [MetaQuestion]:
        raise NotImplementedError()


class MetaQuestionsRepository:

    def __init__(self, output_dir: str):
        self.dir = output_dir

    def save(self, questions: [MetaQuestion]):
        amount = len(questions)
        for i in range(amount):
            question = questions[i]
            folder = self.dir + "/" + str(i)

            with open(folder + "/meta.json", 'wb') as fp:
                json.dump(question.metadata_to_dict(), fp)

    @staticmethod
    def _meta2pdf(question: MetaQuestion, output_path: str):
        i = 0
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        for part in question.portions.parts:
            MetaQuestionsRepository._portion2pdf(
                part,
                question.portions.pdf_file,
                output_path + "/" +
                str(i) + ".pdf")
            i += 1

        merger = PdfFileMerger()
        for i in range(len(question.portions.parts)):
            merger.append(
                PdfFileReader(
                    open(
                        output_path + "/" + str(i) + ".pdf", 'rb'
                    )
                )
            )
        merger.write(output_path + "/" + "question.pdf")
        for i in range(len(question.portions.parts)):
            os.remove(
                output_path + "/" + str(i) + ".pdf"
            )

    @staticmethod
    def _portion2pdf(pdf_input_path: str, portion: Portion, output_path: str):
        with open(pdf_input_path, "rb") as pdf_file:
            pdf_input = PdfFileReader(pdf_file)
            output = PdfFileWriter()

            page = pdf_input.getPage(portion.page)
            page = PDFManipulation.crop_page(
                page,
                portion.upper,
                portion.lower)
            output.addPage(page)

            with open(output_path, "wb") as out_f:
                output.write(out_f)
