from collections import defaultdict
from typing import Any, Dict, List, Optional

import nltk
from evaluate import load

from eval.base_eval import BaseEval

INDEX_BASED_STRING_MATCHING = ["exact", "partial", "any", "control"]
TEXT_BASED_STRING_MATCHING = ["bleu", "rouge", "squad_v2"]


class StringsEval(BaseEval):
    def __init__(self, methods: list, bleu_max_order: Optional[List[int]] = None):
        super().__init__(methods)
        self.bleu_max_order = bleu_max_order or [1]
        self.external_metrics = {}
        for method in methods:
            if method in TEXT_BASED_STRING_MATCHING:
                self.external_metrics[method] = load(method)
            elif method not in INDEX_BASED_STRING_MATCHING:
                raise ValueError(f"Method {method} not supported")

    def run(self, predictions: List[Dict], targets: List[Dict]) -> Dict[str, List]:
        results = defaultdict(list)
        tokenizer = lambda x: nltk.word_tokenize(x)  # noqa: E731
        for idx, (prediction, target) in enumerate(zip(predictions, targets)):
            for method in self.methods:
                if method in TEXT_BASED_STRING_MATCHING:
                    if method == "squad_v2":
                        no_answer_probability = 0.0 if prediction["text"] else 1.0
                        tgt_text = [target["text"]] if target["text"] else []
                        pred = [
                            {
                                "prediction_text": prediction["text"],
                                "no_answer_probability": no_answer_probability,
                                "id": str(idx),
                            }
                        ]
                        tgt = [
                            {
                                "answers": {
                                    "text": tgt_text,
                                    "answer_start": [target["start"]],
                                },
                                "id": str(idx),
                            }
                        ]
                        results[method].append(
                            self.external_metrics[method].compute(
                                predictions=pred, references=tgt
                            )
                        )
                        continue

                    if not target["text"] or not prediction["text"]:
                        results[method].append(None)
                        continue
                    pred = [prediction["text"]]
                    tgt = [target["text"]]
                    if method == "bleu":
                        for order in self.bleu_max_order:
                            results[method].append(
                                self.external_metrics[method].compute(
                                    predictions=pred,
                                    references=tgt,
                                    tokenizer=tokenizer,
                                    max_order=order,
                                )
                            )
                    else:
                        results[method].append(
                            self.external_metrics[method].compute(
                                predictions=pred, references=tgt, tokenizer=tokenizer
                            )
                        )
                else:
                    results[method].append(self.match(prediction, target, method))
        return self.aggregate_metrics(results)

    def match(self, prediction: dict, target: dict, method: str = "exact") -> str:
        if not prediction["text"] and not target["text"]:
            return "true_negative"
        if not prediction["text"]:
            return "false_negative"
        if method == "control" and prediction["start"] != -1:
            return "true_positive"
        if not target["text"]:
            return "false_positive"
        if method == "exact":
            if (
                prediction["start"] == target["start"]
                and prediction["end"] == target["end"]
            ):
                return "true_positive"
        if method == "partial":
            if (
                target["start"] <= prediction["start"] <= target["end"]
                or target["start"] <= prediction["end"] <= target["end"]
                or prediction["start"] <= target["start"] <= prediction["end"]
                or prediction["start"] <= target["end"] <= prediction["end"]
            ):
                return "true_positive"
        if method == "any":
            if prediction["start"] >= 0 and bool(target["text"]):
                return "true_positive"
        return "false_positive"

    def aggregate_metrics(self, results: Dict[str, List]) -> Dict[str, Dict[str, Any]]:
        metrics = {}
        for method, values in results.items():
            if method in TEXT_BASED_STRING_MATCHING:
                metrics[method] = self.average_metrics(values)
            else:
                metrics[method] = self.calculate_precision_recall_f1(values)
        return metrics

    def average_metrics(self, metric_results: List[Dict[str, Any]]) -> Dict[str, float]:
        averages = {}
        occ_per_key = defaultdict(int)
        for result in metric_results:
            if result is None:
                continue
            for key in result.keys():
                if not isinstance(result[key], int) and not isinstance(
                    result[key], float
                ):
                    continue
                if key not in averages:
                    averages[key] = 0
                averages[key] += result[key]
                occ_per_key[key] += 1
        for key in averages.keys():
            averages[key] = (
                averages[key] / occ_per_key[key]
                if "total" not in key
                else averages[key]
            )
        return averages

    def calculate_precision_recall_f1(self, results: list) -> Dict[str, float]:
        tp = results.count("true_positive")
        fp = results.count("false_positive")
        fn = results.count("false_negative")
        pr_div = tp + fp
        rc_div = tp + fn
        precision = tp / pr_div if pr_div else 0
        recall = tp / rc_div if rc_div else 0
        f1_div = precision + recall
        f1 = 2 * precision * recall / f1_div if f1_div else 0
        return {"precision": precision, "recall": recall, "f1": f1}
