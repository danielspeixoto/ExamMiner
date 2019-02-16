from data.MetaQuestions import MetaQuestionsRepository
from data.PreProcessor import PreProcessor
from data.QuestionSplitter import QuestionSplitter
from data.TestValidator import TestValidator


class Miner:

    def __init__(self,
                 preprocessor: PreProcessor,
                 splitter: QuestionSplitter,
                 validator: TestValidator,
                 storage: MetaQuestionsRepository
                 ):
        self.pre_processor = preprocessor
        self.splitter = splitter
        self.validator = validator
        self.storage = storage


    def run(self, input_path: str, output_path: str):
        print("Mining started")
        print("File pre processing")
        self.pre_processor.pre_process(input_path, output_path)
        print("Splitting in questions")
        meta_questions = self.splitter.split(output_path)
        print("Validating Results")
        self.validator.validate(meta_questions)
        print("Saving to storage")
        self.storage.save(meta_questions)