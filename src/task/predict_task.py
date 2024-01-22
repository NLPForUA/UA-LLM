from typing import Optional

from data.reader.base_reader import BaseReader
from data.writer.base_writer import BaseWriter
from llm.base_llm import BaseLLM
from llm.chatgpt import PromptStrategy
from task.base_task import BaseTask


class PredictTask(BaseTask):
    def __init__(
        self,
        model: BaseLLM,
        reader: BaseReader,
        writer: BaseWriter,
        input_col: str,
        output_col: str,
    ):
        super().__init__(model, reader, writer)
        self.input_col = input_col
        self.output_col = output_col

    def run(self, return_predictions=False) -> Optional[list]:
        predictions = []

        for row in self.reader.stream():
            prediction = self.model.predict(
                row[self.input_col], "", PromptStrategy.NONE
            )
            if return_predictions:
                predictions.append(prediction)
            self.writer.stream([prediction])

        if return_predictions:
            return predictions
