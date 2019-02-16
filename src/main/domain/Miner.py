from data.MetaQuestions import MetaQuestionsRepository, MetadataFormatter
from data.PreProcessor import PreProcessor
from data.QuestionSplitter import QuestionSplitter
from data.ExamValidator import ExamValidator


class Miner:

    def __init__(self,
                 preprocessor: PreProcessor,
                 splitter: QuestionSplitter,
                 validator: ExamValidator,
                 formatter: MetadataFormatter,
                 storage: MetaQuestionsRepository
                 ):
        self.pre_processor = preprocessor
        self.splitter = splitter
        self.validator = validator
        self.formatter = formatter
        self.storage = storage


    def run(self, input_path: str, output_path: str):
        print("Mining started")
        print("File pre processing")
        self.pre_processor.pre_process(input_path, output_path)
        print("Splitting in questions")
        questions = self.splitter.split(output_path)
        print("Validating Results")
        self.validator.validate(questions)
        print("Adding metadata")
        metas = self.formatter.format(questions)
        print("Saving to storage")
        self.storage.save(metas)