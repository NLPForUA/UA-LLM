import json
from typing import Optional, Tuple

from llm.chatgpt import PromptStrategy
from task.predict_task import PredictTask


class QAPredictTask(PredictTask):
    def __init__(self, question_col: str, prompt: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.question_col = question_col
        self.prompt = prompt

    def run(self, return_predictions=False, print_usage=False) -> Optional[list]:
        predictions = []
        processed = 0

        self.writer.stream(["prediction", "input"])

        for row in self.reader.stream():
            prompt = self.prompt.format(
                context=row[self.input_col], question=row[self.question_col]
            )
            input_data = {
                "context": row[self.input_col],
                "question": row[self.question_col],
                "prompt": prompt,
            }
            prediction = self.model.predict(prompt, "", PromptStrategy.NONE)
            prediction = self.remove_prefix(prediction, "answer:").strip()

            if len(prediction) and prediction[-1] in [".", ",", "!", "?", ";", ":"]:
                prediction = prediction[:-1].strip()

            if prediction == "<no-answer>":
                prediction = ""

            if prediction:
                start, end = self.find_start_end(row[self.input_col], prediction)
                prediction = {"text": prediction, "start": start, "end": end}
            else:
                prediction = {"text": "", "start": -1, "end": -1}

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
