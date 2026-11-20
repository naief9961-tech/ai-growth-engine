# R35 targeted follow-up — chart665

> Publication update2026-11-20: [comment7000865667](https://github.com/aws-samples/sample-spec-driven-presentation-maker/issues/665#issuecomment-7000865667) by naief9961-tech was manually posted2026-11-19T05:42:24Z and verified. Do not repost. Earlier investigation/403 notes below are historical; no later developer reply observed.

Checked 2026-11-19T05:35:10.661Z. User explicitly requested solving one candidate after screening. This is a material new local investigation, not another generic comment. Upstream issue remains open with0 comments; latest30 PR summaries and full issue timeline read. Related open PR649 diff reviewed; it adds a reusable order helper for different elements and does not repair this bar block. No third-party publication.

Issue: https://github.com/aws-samples/sample-spec-driven-presentation-maker/issues/665
Reporter: ShotaroKataoka. Source commit: 955b743a51dc9cf31782e4c6c39291a12d3accdb. File: sdpm/sdpm/engine/builder/elements/chart.py; Git blob797347f70755416c9e75d82412b2bf5a636681af verified locally. Initial file materialization added a newline; removed it and verified the exact Git blob before testing.

## Evidence and result

The reporter already identified append order. New contribution: 16 paired cases execute the pinned bar block and candidate on real python-pptx1.0.2 charts, serialize to PPTX and reopen. Original order fails in16/16; candidate passes16/16; values match in each pair. Additional3 optional-child/idempotency cases pass. Source-extracted bounded test, not whole SDPM. No packages installed, network calls, secrets or payment operations in the test.

Preserve stacked overlap100 and insert gapWidth before it. Preserve existing gapWidth zero-fallback semantics; changing it is separate scope. Existing malformed element locations are not normalized by this candidate. Full SDPM generate(), repository suite, ruff, full XSD validation and native PowerPoint were NOT RUN. Confidence high in bounded ordering behavior, integration acceptance pending.

## Candidate patch

If PR649 lands first, reuse its helper and omit the duplicate helper addition below. Standalone candidate at the pinned main SHA:

```diff
--- a/sdpm/sdpm/engine/builder/elements/chart.py
+++ b/sdpm/sdpm/engine/builder/elements/chart.py
@@ -7,6 +7,21 @@
 from sdpm.engine.schema.chart import restores_chart_xml
 from sdpm.utils import xml_safe
 
+
+def _insert_in_order(parent, tag_name, before_tags):
+    from lxml import etree
+    from pptx.oxml.ns import qn
+    existing = parent.find(qn(tag_name))
+    if existing is not None:
+        return existing
+    element = etree.Element(qn(tag_name))
+    before = {qn(tag) for tag in before_tags}
+    for index, child in enumerate(parent):
+        if child.tag in before:
+            parent.insert(index, element)
+            return element
+    parent.append(element)
+    return element
 
 class ChartMixin:
     """Mixin providing chart element methods."""
@@ -280,13 +295,13 @@
                 # Gap width: tighter grouping
                 gap_w = x_chart.find(qn('c:gapWidth'))
                 if gap_w is None:
-                    gap_w = etree.SubElement(x_chart, qn('c:gapWidth'))
+                    gap_w = _insert_in_order(x_chart, 'c:gapWidth', ('c:overlap', 'c:serLines', 'c:axId', 'c:extLst'))
                 gap_w.set('val', str(elem.get("gapWidth") or style_gap_width or ('80' if not stacked else '60')))
                 # Overlap for clustered
                 if not stacked:
                     overlap = x_chart.find(qn('c:overlap'))
                     if overlap is None:
-                        overlap = etree.SubElement(x_chart, qn('c:overlap'))
+                        overlap = _insert_in_order(x_chart, 'c:overlap', ('c:serLines', 'c:axId', 'c:extLst'))
                     overlap.set('val', str(elem.get("overlap", -10)))
     
         # --- Line-specific: smooth curves ---

```

## Reproduction

Save the pinned chart.py as source.py beside check.py, verify its Git blob, then run python check.py in an environment with python-pptx1.0.2 and lxml. Harness executes only the extracted bar block; it does not import upstream entrypoints.

```python
import ast
import copy
import io
import json
from pathlib import Path
from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.oxml.ns import qn
from pptx.util import Inches

source = Path(__file__).with_name('source.py').read_text()
start = source.index('        # --- Bar-specific:')
end = source.index('        # --- Line-specific:', start)
import textwrap
baseline = textwrap.dedent(source[start:end])
helper = '''def _insert_in_order(parent, tag_name, before_tags):
    existing = parent.find(qn(tag_name))
    if existing is not None:
        return existing
    element = etree.Element(qn(tag_name))
    before = {qn(tag) for tag in before_tags}
    for index, child in enumerate(parent):
        if child.tag in before:
            parent.insert(index, element)
            return element
    parent.append(element)
    return element
'''
candidate = baseline.replace("etree.SubElement(x_chart, qn('c:gapWidth'))", "_insert_in_order(x_chart, 'c:gapWidth', ('c:overlap', 'c:serLines', 'c:axId', 'c:extLst'))").replace("etree.SubElement(x_chart, qn('c:overlap'))", "_insert_in_order(x_chart, 'c:overlap', ('c:serLines', 'c:axId', 'c:extLst'))")
assert candidate != baseline
rows=[]
for stacked in (False, True):
 for horizontal in (False, True):
  for name, elem, style_gap in [('default', {}, None), ('style', {}, 95), ('explicit', {'gapWidth': 120, 'overlap': 15}, 95), ('zero-compat', {'gapWidth': 0, 'overlap': 0}, 95)]:
   originals=[]
   for fixed in (False, True):
    prs=Presentation(); slide=prs.slides.add_slide(prs.slide_layouts[6])
    data=CategoryChartData(); data.categories=['A','B']; data.add_series('one',[1,2]); data.add_series('two',[3,4])
    kind={(False,False):XL_CHART_TYPE.COLUMN_CLUSTERED,(True,False):XL_CHART_TYPE.COLUMN_STACKED,(False,True):XL_CHART_TYPE.BAR_CLUSTERED,(True,True):XL_CHART_TYPE.BAR_STACKED}[stacked,horizontal]
    chart=slide.shapes.add_chart(kind, Inches(1), Inches(1), Inches(5), Inches(3),data).chart
    pa=chart._chartSpace.find('.//'+qn('c:plotArea'))
    ns=dict(etree=etree,qn=qn,plot_area=pa,chart_type='bar',stacked=stacked,elem=elem,style_gap_width=style_gap)
    exec(compile(helper+(candidate if fixed else baseline),'source-extract','exec'),ns)
    buffer=io.BytesIO(); prs.save(buffer); buffer.seek(0)
    reopened=Presentation(buffer); ch=reopened.slides[0].shapes[0].chart
    bar=ch._chartSpace.find('.//'+qn('c:barChart'))
    tags=[etree.QName(x).localname for x in bar]
    ordered=tags.index('gapWidth')<tags.index('overlap')<tags.index('axId')
    assert ordered is fixed, (fixed,tags)
    values=[bar.find(qn('c:'+k)).get('val') for k in ('gapWidth','overlap')]
    originals.append(values)
   assert originals[0]==originals[1]
   rows.append(dict(stacked=stacked,horizontal=horizontal,input=name,baseline_order_failed=True,candidate_order_passed=True,values_unchanged=originals[1]))
# Optional later children: must not insert after serLines/extLst, even without axes.
ns={'etree':etree,'qn':qn};exec(helper,ns)
for later in ('c:serLines','c:extLst','c:axId'):
 p=etree.Element(qn('c:barChart')); etree.SubElement(p,qn('c:ser')); etree.SubElement(p,qn(later))
 ns['_insert_in_order'](p,'c:overlap',('c:serLines','c:axId','c:extLst'))
 gap=ns['_insert_in_order'](p,'c:gapWidth',('c:overlap','c:serLines','c:axId','c:extLst'))
 assert [etree.QName(x).localname for x in p]==['ser','gapWidth','overlap',later.split(':')[1]]
 assert ns['_insert_in_order'](p,'c:gapWidth',('c:axId',)) is gap
result={'paired_pptx_cases':len(rows),'optional_child_cases':3,'cases':rows,'limits':'Source-extracted bar block using real python-pptx 1.0.2 charts and save/reopen; not full SDPM generate(), full XSD validation, ruff or native PowerPoint.'}
Path(__file__).with_name('results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

```

## Actual result

```json
{
  "paired_pptx_cases": 16,
  "optional_child_cases": 3,
  "cases": [
    {
      "stacked": false,
      "horizontal": false,
      "input": "default",
      "baseline_order_failed": true,
      "candidate_order_passed": true,
      "values_unchanged": [
        "80",
        "-10"
      ]
    },
    {
      "stacked": false,
      "horizontal": false,
      "input": "style",
      "baseline_order_failed": true,
      "candidate_order_passed": true,
      "values_unchanged": [
        "95",
        "-10"
      ]
    },
    {
      "stacked": false,
      "horizontal": false,
      "input": "explicit",
      "baseline_order_failed": true,
      "candidate_order_passed": true,
      "values_unchanged": [
        "120",
        "15"
      ]
    },
    {
      "stacked": false,
      "horizontal": false,
      "input": "zero-compat",
      "baseline_order_failed": true,
      "candidate_order_passed": true,
      "values_unchanged": [
        "95",
        "0"
      ]
    },
    {
      "stacked": false,
      "horizontal": true,
      "input": "default",
      "baseline_order_failed": true,
      "candidate_order_passed": true,
      "values_unchanged": [
        "80",
        "-10"
      ]
    },
    {
      "stacked": false,
      "horizontal": true,
      "input": "style",
      "baseline_order_failed": true,
      "candidate_order_passed": true,
      "values_unchanged": [
        "95",
        "-10"
      ]
    },
    {
      "stacked": false,
      "horizontal": true,
      "input": "explicit",
      "baseline_order_failed": true,
      "candidate_order_passed": true,
      "values_unchanged": [
        "120",
        "15"
      ]
    },
    {
      "stacked": false,
      "horizontal": true,
      "input": "zero-compat",
      "baseline_order_failed": true,
      "candidate_order_passed": true,
      "values_unchanged": [
        "95",
        "0"
      ]
    },
    {
      "stacked": true,
      "horizontal": false,
      "input": "default",
      "baseline_order_failed": true,
      "candidate_order_passed": true,
      "values_unchanged": [
        "60",
        "100"
      ]
    },
    {
      "stacked": true,
      "horizontal": false,
      "input": "style",
      "baseline_order_failed": true,
      "candidate_order_passed": true,
      "values_unchanged": [
        "95",
        "100"
      ]
    },
    {
      "stacked": true,
      "horizontal": false,
      "input": "explicit",
      "baseline_order_failed": true,
      "candidate_order_passed": true,
      "values_unchanged": [
        "120",
        "100"
      ]
    },
    {
      "stacked": true,
      "horizontal": false,
      "input": "zero-compat",
      "baseline_order_failed": true,
      "candidate_order_passed": true,
      "values_unchanged": [
        "95",
        "100"
      ]
    },
    {
      "stacked": true,
      "horizontal": true,
      "input": "default",
      "baseline_order_failed": true,
      "candidate_order_passed": true,
      "values_unchanged": [
        "60",
        "100"
      ]
    },
    {
      "stacked": true,
      "horizontal": true,
      "input": "style",
      "baseline_order_failed": true,
      "candidate_order_passed": true,
      "values_unchanged": [
        "95",
        "100"
      ]
    },
    {
      "stacked": true,
      "horizontal": true,
      "input": "explicit",
      "baseline_order_failed": true,
      "candidate_order_passed": true,
      "values_unchanged": [
        "120",
        "100"
      ]
    },
    {
      "stacked": true,
      "horizontal": true,
      "input": "zero-compat",
      "baseline_order_failed": true,
      "candidate_order_passed": true,
      "values_unchanged": [
        "95",
        "100"
      ]
    }
  ],
  "limits": "Source-extracted bar block using real python-pptx 1.0.2 charts and save/reopen; not full SDPM generate(), full XSD validation, ruff or native PowerPoint."
}

```

## English reply — POSTED MANUALLY — VERIFIED; DO NOT REPOST

I checked the bar-specific block at 955b743a51dc and reproduced the ordering issue using its extracted source with python-pptx 1.0.2.

Across 16 paired cases (clustered/stacked × vertical/horizontal × default/style/explicit/zero inputs), the original block produced the wrong order. Inserting the missing elements at their schema positions fixed the order after PPTX save/reopen in all 16 cases, with gapWidth/overlap values unchanged. Three additional checks covered serLines/extLst/axId insertion boundaries.

The stacked case matters: python-pptx already supplies overlap=100, so gapWidth must be inserted before that existing overlap, not merely before axId.

I would reuse the _insert_in_order helper from #649:
- gapWidth before overlap, serLines, axId or extLst;
- overlap before serLines, axId or extLst.

One compatibility detail: the current `elem.get("gapWidth") or style_gap_width ...` treats an explicit zero as a fallback. I preserved that behavior in this ordering-only candidate rather than mixing in a value-semantics change.

These are isolated source-block tests with real PPTX serialization, not the full SDPM generate()/roundtrip suite, full OOXML schema validation or a PowerPoint application test. Before merging, the same matrix should run through tests/test_chart_roundtrip.py.


## Publication attempt

User explicitly approved this exact reply. GitHub rejected comment creation with403 Resource not accessible by integration. Re-read issue comments after the attempt: empty. No comment created, no permission workaround attempted. Original destination: https://github.com/aws-samples/sample-spec-driven-presentation-maker/issues/665. Manual publication remains possible by the owner; verify comments before posting.
