# R28 isolated evidence

Python 3.12.14. Five groups passed: three baseline AttributeErrors (integer, None, tuple labels) and guarded correct-order checks, plus string-only and no-score controls. The extracted comprehension comes from Phoenix commit 464a60fd3c24aaed780cea3f2e0e437d3c8ba037, utils.py blob 9dd797daf113206c1f73837ee55aa57c9920c868.

This substitutes a SimpleNamespace.columns list for a DataFrame. It does not execute pandas, evaluate_dataframe, to_annotation_dataframe, transport, persistence or the full package. The candidate guard is already the reporter's proposal, not an original repair.

```python
from types import SimpleNamespace
original = "[col[:-6] for col in working_df.columns if col.endswith(\"_score\")]"
fixed = original.replace('if col.endswith', 'if isinstance(col, str) and col.endswith')
for bad in (0, None, ('tuple',)):
    working_df=SimpleNamespace(columns=['span_id','first_score',bad,'second_score'])
    try: eval(original)
    except AttributeError: pass
    else: raise AssertionError('baseline should fail')
    assert eval(fixed)==['first','second']
for cols, expected in [(['span_id','first_score','second_score'],['first','second']),(['span_id',0],[])]:
    working_df=SimpleNamespace(columns=cols)
    assert eval(fixed)==expected
print('5 isolated comprehension groups passed; 3 reproduce baseline AttributeError. No pandas/public API/full suite.')
```

Observed output:
```text
5 isolated comprehension groups passed; 3 reproduce baseline AttributeError. No pandas/public API/full suite.
```
