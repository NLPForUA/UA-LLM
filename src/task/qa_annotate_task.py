import json
from typing import Optional, Tuple

from llm.chatgpt import PromptStrategy
from task.predict_task import PredictTask


class QAAnnotateTask(PredictTask):
    def __init__(self, question_col: str, prompt: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompt = prompt
        self.question_col = question_col

    def run(self, return_predictions=False, print_usage=False) -> Optional[list]:
        predictions = []
        processed = 0

        self.writer.stream(["prediction", "input"])

        for row in self.reader.stream():
            prompt = self.prompt.format(context=row[self.input_col])
            input_data = {"context": row[self.input_col], "prompt": prompt}
            prediction = self.model.predict(prompt, "", PromptStrategy.NONE)
            prediction = prediction.strip()
            prediction = {"text": prediction}

            if return_predictions:
                predictions.append(prediction)
            self.writer.stream([json.dumps(prediction), json.dumps(input_data)])

            processed += 1

            if processed % 100 == 0:
                print(f"Processed {processed} examples")

        if print_usage:
            print(self.model.provider.get_session_usage())

        if return_predictions:
            return predictions

    @staticmethod
    def remove_prefix(text: str, prefix: str) -> str:
        return text[text.startswith(prefix) and len(prefix) :]

    @staticmethod
    def find_start_end(text: str, substr: str) -> Tuple[int, int]:
        start = text.find(substr)
        if start == -1:
            return -1, -1
        end = start + len(substr)
        return start, end
