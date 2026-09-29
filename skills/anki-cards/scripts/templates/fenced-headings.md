---
tags: [example::fenced-headings]
---

# Card 1 — comment lines inside a fence
## 正面
Which file does DVC read the pipeline from?
```yaml
# dvc.yaml
## not a field either
stages:
  train:
    cmd: python train.py
```
## 背面
<code>dvc.yaml</code> at the repo root.
```bash
# ...fix train.py, then rerun only what changed
dvc repro
```

# Card 2 — after the fences, headings work again
## 正面
What does this Python snippet print?
## 背面
```python
# prints True
## still code
print(1 < 2)
```
