# Perception for Visual Computing Contrast Experiments

## RQ
*Does the luminance contrast of a coding editor theme affect code comprehension?*

## Dependencies

[VS Code](https://github.com/microsoft/vscode/releases/tag/1.83.0) version 1.83.0 was used for all experiments.

Install requirements as follows (tested on Python 3.11.6):
```
pip3 install -r requirements.txt
```

Experiments were carried out on Fedora 38

## File Structure

### Experiment Files 

- [`background_script.py`](background_script.py): main background script switching themes and timing participants

- [`contrast.py`](contrast.py): determine gray-scale values given Michelson contrast

- [`trial_1_func.py`](trial_1_func.py): comprehension questions for first coding task

- [`trial_2_func.py`](trial_2_func.py): comprehension questions for second coding task

- [`trial_3_func.py`](trial_3_func.py): comprehension questions for third coding task

### Data

[`data`](data/): participant results

### Analysis

[`results.py`](results.py): main experimental results (response times and response correctness)

[`first_question_plot.py`](first_question_plot.py): visually highlights method error of not showing example question beforehand