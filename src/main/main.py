from data.ConfigProvider import YAMLConfigProvider
from data.ENEM import ENEMMetadataFormatter
from data.ExamValidator import ExamValidator
from data.MetaQuestions import MetaQuestionsRepository
from data.PreProcessor import PreProcessor
from data.QuestionSplitter import QuestionSplitter
from domain.Miner import Miner

prov = YAMLConfigProvider("/home/daniel/work/enem-parser (copy 1)/src/test/res/config.yaml")
config = prov.get_config()

preprocessor = PreProcessor(
    config["work_dir"],
    config["one_column_pages"],
    config["excluded_pages"]
)

splitter = QuestionSplitter(
    config["work_dir"],
    "/home/daniel/work/enem-parser/res/question_pattern.png"
)

validator = ExamValidator()

formatter = ENEMMetadataFormatter(
    config["microdata"],
    config["edition"],
    config["variant"],
    config["part"],
    []
)

storage = MetaQuestionsRepository(
    config["output_dir"]
)

miner = Miner(
    preprocessor,
    splitter,
    validator,
    formatter,
    storage
)

miner.run(config["file"], config["work_dir"] + "/working_pdf")
