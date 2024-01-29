from ast import literal_eval
from typing import Optional

from data.reader.base_reader import BaseReader
from eval.base_eval import BaseEval
from task.base_task import BaseTask


class EvalTask(BaseTask):
    def __init__(
        self,
        evaluator: BaseEval,
        input_col: str,
        output_col: str,
        predictions_reader: Optional[BaseReader] = None,
        pred_col: Optional[str] = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.evaluator = evaluator
        self.input_col = input_col
        self.output_col = output_col
        self.predictions_reader = predictions_reader
        self.pred_col = pred_col

    def run(self):
        if not self.predictions_reader:
            predictions = self.model.run(return_predictions=True, print_usage=True)
        else:
            predictions = self.predictions_reader.run(
                apply_fn={self.pred_col: literal_eval}
            )[self.pred_col]
        eval_data = self.reader.run(apply_fn={self.input_col: literal_eval})

        results = self.evaluator.run(predictions, eval_data[self.input_col])
        print("\n", results)
        self.writer.run(results)
