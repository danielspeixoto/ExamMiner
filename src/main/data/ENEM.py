from typing import Tuple

import pandas as pd

from data.MetaQuestions import QuestionPortions, MetaQuestion, MetadataFormatter


class ENEMMetadataFormatter(MetadataFormatter):

    def __init__(self,
                 micro_data_path: str,
                 edition: int,
                 variant: str,
                 part: int,
                 tags: [str]
                 ):
        self.micro_data = pd.read_csv(micro_data_path, sep=";")
        self.micro_data = self.micro_data.loc[self.micro_data['TX_COR'] == variant]
        self.exam = "ENEM"
        self.edition = edition
        self.variant = variant
        self.part = part
        self.tags = tags

    def format(self, questions: [QuestionPortions])-> [MetaQuestion]:
        metas = []
        i = 0
        for question in questions:
            i += 1
            domain, number = self._get_domain__and_number(i)
            meta = MetaQuestion(
                question,
                self.exam,
                self.edition,
                domain,
                self.variant,
                self.part,
                number,
                self._answer(i),
                self.tags
            )
            metas.append(meta)
        return metas

    def _get_domain__and_number(self, question_idx)-> Tuple[str, int]:
        if self.edition >= 2017:
            if self.part == 2:
                if question_idx < 45:
                    return "Naturais", question_idx
                else:
                    return "Matemática", question_idx
            else:
                if question_idx < 5:
                    return "Inglês", question_idx
                elif question_idx < 10:
                    return "Espanhol", question_idx - 5
                elif question_idx < 50:
                    return "Linguagens", question_idx - 5
                else:
                    return "Humanas", question_idx - 5
        else:
            if self.part == 2:
                if question_idx < 45:
                    return "Humanas", question_idx
                else:
                    return "Naturais", question_idx
            else:
                if question_idx <= 5:
                    return "Inglês", question_idx
                elif question_idx <= 10:
                    return "Espanhol", question_idx - 5
                elif question_idx < 50:
                    return "Linguagens", question_idx - 5
                else:
                    return "Matemática", question_idx - 5

    def _answer(self, question_idx):
        if self.part == 2:
            question_idx += 90
            if self.edition >= 2017:
                # First self.part had 95 questions instead of only 90
                question_idx += 5

        ans = self.micro_data.iloc[question_idx, 3]
        return ord(ans[0]) - ord('A')