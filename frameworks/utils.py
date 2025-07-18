from typing import List, Any


def batch_iterator(items: List[Any], step: int = 1000):
    overall_count = len(items)
    previous_step = 0
    for step in range(step, overall_count, step):
        if previous_step == step:
            step = overall_count
        yield items[previous_step:step]
        if step != overall_count:
            previous_step = step
    else:
        yield items[previous_step:overall_count]
