# Northplan #100 — isolated numeric-input candidate

**Review option, not an upstream change or ready-to-merge PR.** Based on [schema.py at f3b55a5e72a30080ef28cd3066371017ecae1b97](https://github.com/janowoc/northplan/blob/f3b55a5e72a30080ef28cd3066371017ecae1b97/engine/scenario/schema.py). Original source © 2026 Jan Owoc, AGPL-3.0-or-later; this derived patch retains that license. [Upstream license](https://github.com/janowoc/northplan/blob/f3b55a5e72a30080ef28cd3066371017ecae1b97/LICENSE).

The narrow decision explored here is to refuse bool at numeric leaves without changing other coercions. In particular, integral-float seeds and integer flags retain the project's existing expectation. The owner has not accepted this policy; broader strict typing is a separate option. No tax parameters or financial calculations are changed.

A scratch harness changed 29 scalar annotation occurrences in the four aliases and model fields. Only annotations change; runtime int/float calls, helper signatures and validators remain intact. Both grid union branches use guarded scalar types. [16 isolated groups passed](TESTS.md). No upstream suite, editor/API integration, minimum-supported Pydantic matrix or pinned formatter run. No test expectations or snapshots were edited. Empty package initializers are disclosed in TESTS.md.

The following diff is the exact candidate tested, including its preliminary formatting; it must be adapted to repository style and owner policy before any authorized upstream proposal.

```diff
--- a/engine/scenario/schema.py
+++ b/engine/scenario/schema.py
@@ -55,7 +55,7 @@
 from typing import Annotated, Any, Final, Literal, Self, TypeVar
 
 import numpy as np
-from pydantic import AfterValidator, BaseModel, ConfigDict, Field, model_validator
+from pydantic import AfterValidator, BeforeValidator, BaseModel, ConfigDict, Field, model_validator
 
 from engine.mc.moments import covariance_from_correlation, monthly_log_moments
 
@@ -148,21 +148,32 @@
 #: ``FrozenMapping[Finite]``; nests as ``FrozenMapping[FrozenMapping[Finite]]``.
 FrozenMapping = Annotated[Mapping[str, _V], AfterValidator(_freeze)]
 
+def _reject_bool_number(value: Any) -> Any:
+    """Refuse booleans before numeric conversion; preserve other input coercions."""
+    if isinstance(value, bool):
+        raise ValueError("boolean is not a numeric scenario value")
+    return value
+
+
+InputInt = Annotated[int, BeforeValidator(_reject_bool_number)]
+InputFloat = Annotated[float, BeforeValidator(_reject_bool_number)]
+
+
 #: A float that is neither infinite nor nan. Every float in this schema is
 #: finite, either through this alias or through ``allow_inf_nan=False``
 #: alongside its own bounds.
-Finite = Annotated[float, Field(allow_inf_nan=False)]
+Finite = Annotated[InputFloat, Field(allow_inf_nan=False)]
 
 #: A finite dollar amount that cannot be negative. Real dollars of January of
 #: the scenario's start year, like every amount below except
 #: ``Person.prior_year_net_income`` and ``Person.net_income_two_years_prior``.
-Money = Annotated[float, Field(ge=0.0, allow_inf_nan=False)]
+Money = Annotated[InputFloat, Field(ge=0.0, allow_inf_nan=False)]
 
 #: A calendar month, January is 1.
-Month = Annotated[int, Field(ge=1, le=12)]
+Month = Annotated[InputInt, Field(ge=1, le=12)]
 
 #: A bare fraction in ``[0, 1]``, never a percentage.
-Fraction = Annotated[float, Field(ge=0.0, le=1.0, allow_inf_nan=False)]
+Fraction = Annotated[InputFloat, Field(ge=0.0, le=1.0, allow_inf_nan=False)]
 
 #: A two-letter jurisdiction code, e.g. ``"ab"``. Lower case, so that the
 #: string can be handed to ``ParamYear.province`` and reach a file name
@@ -191,10 +202,10 @@
         annual: Real dollars per year, before tax.
     """
 
-    from_year: int = Field(
+    from_year: InputInt = Field(
         description="First calendar year this income is earned.",
     )
-    to_year: int = Field(
+    to_year: InputInt = Field(
         description="Last calendar year this income is earned, inclusive.",
     )
     annual: Money = Field(
@@ -291,7 +302,7 @@
         description="A label for this pension, unique for this person, used to tell pensions "
         "apart in results.",
     )
-    start_year: int = Field(
+    start_year: InputInt = Field(
         description="Calendar year the pension begins.",
     )
     start_month: Month = Field(
@@ -310,7 +321,7 @@
         description="Real dollars a year of a bridge benefit paid on top of the pension until "
         "the bridge age. Zero if there is none.",
     )
-    bridge_to_age_years: int | None = Field(
+    bridge_to_age_years: InputInt | None = Field(
         default=None,
         description="Age the bridge benefit stops, usually the age the public pension it "
         "bridges to begins.",
@@ -632,7 +643,7 @@
         description="A short name for this person, unique among every person and beneficiary. "
         "Elections, RESP subscribers and grid paths refer to it.",
     )
-    birth_year: int = Field(
+    birth_year: InputInt = Field(
         description="Calendar year of birth.",
     )
     birth_month: Month = Field(
@@ -826,13 +837,13 @@
             the RESP covers it; a shortfall comes from the household.
     """
 
-    start_year: int = Field(
+    start_year: InputInt = Field(
         description="Calendar year schooling begins.",
     )
     start_month: Month = Field(
         description="Month schooling begins, 1 to 12; usually 9 for September.",
     )
-    months: Annotated[int, Field(ge=1)] = Field(
+    months: Annotated[InputInt, Field(ge=1)] = Field(
         description="Length of the programme in months, at least one.",
     )
     annual_cost: Money = Field(
@@ -859,7 +870,7 @@
     id: str = Field(
         description="A short name for this beneficiary, unique among every person and beneficiary.",
     )
-    birth_year: int = Field(
+    birth_year: InputInt = Field(
         description="Calendar year of birth; it decides grant eligibility.",
     )
     birth_month: Month = Field(
@@ -963,7 +974,7 @@
         annual: Real dollars a year for the household.
     """
 
-    from_year: int = Field(
+    from_year: InputInt = Field(
         description="First calendar year this spending level applies.",
     )
     annual: Money = Field(
@@ -988,7 +999,7 @@
         description="Spending levels by year. Each level lasts until the next one begins; the "
         "first must begin at or before the start year, and the last runs to the second death.",
     )
-    survivor_share: Annotated[float, Field(gt=0.0, le=1.0, allow_inf_nan=False)] = Field(
+    survivor_share: Annotated[InputFloat, Field(gt=0.0, le=1.0, allow_inf_nan=False)] = Field(
         description="Fraction of household spending the survivor keeps from the month after the "
         "first death. Above 0 and at most 1.",
     )
@@ -1042,18 +1053,18 @@
         description="Expected real annual total return, a fraction (0.05), not a percentage. It "
         "may be negative, but must be above -1.",
     )
-    vol: Annotated[float, Field(ge=0.0, allow_inf_nan=False)] = Field(
+    vol: Annotated[InputFloat, Field(ge=0.0, allow_inf_nan=False)] = Field(
         description="Annual standard deviation of the real return. Zero means a riskless class.",
     )
-    interest_yield: Annotated[float, Field(ge=0.0, allow_inf_nan=False)] = Field(
+    interest_yield: Annotated[InputFloat, Field(ge=0.0, allow_inf_nan=False)] = Field(
         description="Fraction of the balance paid out each year as interest. This is the tax "
         "character of the return, not an addition to it.",
     )
-    dividend_yield: Annotated[float, Field(ge=0.0, allow_inf_nan=False)] = Field(
+    dividend_yield: Annotated[InputFloat, Field(ge=0.0, allow_inf_nan=False)] = Field(
         description="Fraction of the balance paid out each year as eligible dividends. Part of "
         "the return, not an addition to it.",
     )
-    distributed_gains_yield: Annotated[float, Field(ge=0.0, allow_inf_nan=False)] = Field(
+    distributed_gains_yield: Annotated[InputFloat, Field(ge=0.0, allow_inf_nan=False)] = Field(
         description="Fraction of the balance paid out each year as realized capital gains. Part "
         "of the return, not an addition to it; price change is the real mean less the three "
         "yields.",
@@ -1088,7 +1099,7 @@
             allocation names known classes, is finite, and sums to one.
     """
 
-    inflation: Annotated[float, Field(gt=-1.0, allow_inf_nan=False)] = Field(
+    inflation: Annotated[InputFloat, Field(gt=-1.0, allow_inf_nan=False)] = Field(
         description="Annual inflation, a fraction (0.02), not a percentage. Constant for the "
         "run. Returns below are real, so inflation erodes amounts fixed in dollars.",
     )
@@ -1304,7 +1315,7 @@
         description="Account kinds to draw from, in order, each at most once. Mandatory minimum "
         "withdrawals happen regardless of this order.",
     )
-    taxable_ceiling_bracket: Annotated[int, Field(ge=0)] | None = Field(
+    taxable_ceiling_bracket: Annotated[InputInt, Field(ge=0)] | None = Field(
         description="Turn on to draw from the RRIF, then the RRSP, every month until this "
         "year's net income, projected from the year to date, reaches the top of this federal "
         "tax bracket, counted from 0, whether or not cash is needed. Suits a household that "
@@ -1334,7 +1345,7 @@
             the whole balance to a minimum.
     """
 
-    age_years: int = Field(
+    age_years: InputInt = Field(
         description="Age the conversion happens. The legal deadline is checked against the "
         "start year's parameters.",
     )
@@ -1364,10 +1375,10 @@
         rrif_conversion: The RRSP-to-RRIF conversion, household-wide.
     """
 
-    cpp_start_age_years: FrozenMapping[int] = Field(
+    cpp_start_age_years: FrozenMapping[InputInt] = Field(
         description="The age each person starts CPP, by person id.",
     )
-    oas_start_age_years: FrozenMapping[int] = Field(
+    oas_start_age_years: FrozenMapping[InputInt] = Field(
         description="The age each person starts OAS, by person id.",
     )
     rrif_conversion: RrifConversion = Field(
@@ -1444,26 +1455,26 @@
     name: str = Field(
         description="A label for this scenario, used in export file names.",
     )
-    start_year: int = Field(
+    start_year: InputInt = Field(
         description="The year the simulation starts, on 1 January. Every dollar amount in the "
         "scenario is in that January's dollars, except the two prior-year net incomes, and "
         "that year's tax parameters serve the whole run.",
     )
-    n_paths: Annotated[int, Field(ge=1)] = Field(
+    n_paths: Annotated[InputInt, Field(ge=1)] = Field(
         description="How many Monte Carlo paths to simulate.",
     )
-    seed: int = Field(
+    seed: InputInt = Field(
         description="Seed for the random draws. The same seed reproduces the same results, and "
         "every policy sees the same draws, so policies are compared rather than luck.",
     )
-    risk_aversion: Annotated[float, Field(ge=0.0, allow_inf_nan=False)] | None = Field(
+    risk_aversion: Annotated[InputFloat, Field(ge=0.0, allow_inf_nan=False)] | None = Field(
         default=None,
         description="Your household's risk preference: a coefficient of relative risk aversion, "
         "a bare number and not a percentage. Zero means risk neutral. It scores the finished "
         "results and changes no simulated number. Leave it out and the objectives that need "
         "it refuse to run instead of choosing a preference for you.",
     )
-    estate_utility_shift: Annotated[float, Field(gt=0.0, allow_inf_nan=False)] | None = Field(
+    estate_utility_shift: Annotated[InputFloat, Field(gt=0.0, allow_inf_nan=False)] | None = Field(
         default=None,
         description="Real dollars added to every path's after-tax estate before the "
         "certainty-equivalent objective scores it, and subtracted again afterwards. Without "
@@ -1484,7 +1495,7 @@
     policies: tuple[PolicySpec, ...] = Field(
         description="One or more policies to simulate and compare.",
     )
-    grid: FrozenMapping[tuple[int | Finite, ...]] = Field(
+    grid: FrozenMapping[tuple[InputInt | Finite, ...]] = Field(
         default_factory=lambda: MappingProxyType({}),
         description="Optional. Each key is a dotted path to one number in a policy, and each "
         "value is the list of numbers to try there. Every key must exist on every policy.",
```
