# Release notes


For full details, view the [commit logs](https://github.com/rstudio/vetiver-python/commits/).

## v0.2.3
## What's Changed

[**Full Changelog**](https://github.com/rstudio/vetiver-python/compare/v0.2.2...v0.2.3)

* ENH: add `root_path` if user in Posit Workbench in {{< pr 191 >}}

## v0.2.2
### What's Changed

[**Full Changelog**](https://github.com/rstudio/vetiver-python/compare/v0.2.1...v0.2.2)

* DOCS: add square logo in {{< pr 173 >}}
* DOCS: add API structure documentation in {{< pr 176 >}}
* DOCS: update docs to look less like vetiver.rstudio.com in {{< pr 178 >}}
* BUG: remove __all__ in init in {{< pr 182 >}}
* MAINT: require no less than pins 0.7.1 in {{< pr 183 >}}
* ENH: endpoint_fx docstring as FastAPI description in {{< pr 179 >}}
* MAINT: Update Pydantic usage for v2 compatibility in {{< pr 185 >}}
* MAINT: Update model_card.qmd by in {{< pr 186 >}}
* ENH: add `/GET` prototype endpoint in {{< pr 174 >}}
* BUG: use max instead of first in {{< pr 189 >}}

## v0.2.1
### What's Changed

[**Full Changelog**](https://github.com/rstudio/vetiver-python/compare/v0.2.0...v0.2.1)

* DOC: add changelog in {{< pr 151 >}}
* FIX: None type handling for `python_version` in metadata {{< pr 149 >}}
* Match GHA Python versions to Connect {{< pr 157 >}}
* DOCS: move from sphinx to quartodoc {{< pr 153 >}}
* BUG,CI: /latest not rendering correctly {{< pr 158 >}}
* MAINT: spring cleaning {{< pr 160 >}}
* DOCS: Add netlify docs preview {{< pr 163 >}}
* MAINT: spring cleaning {{< pr 164 >}}
* ENH: Refactor server handling {{< pr 155 >}}
* FEAT: add required packages to authorize pins boards {{< pr 166 >}}
* MAINT: start typing vetiver {{< pr 168 >}}
* FEAT: add new `/metadata` GET endpoint {{< pr 170 >}}
* FEAT: implement spacy models {{< pr 143 >}}

## v0.2.0
### What's Changed

[**Full Changelog**](https://github.com/rstudio/vetiver-python/compare/v0.1.8...v0.2.0)

* DOC: Added missing `model_name` to `VetiverModel` in {{< pr 128 >}}
* BUG, MAINT: Catch non 200 codes in {{< pr 129 >}}
* DOC: fix `deploy_rsconnect` example in {{< pr 1234 >}}
* ENH: Make `vetiver_post` extensible for all endpoints in {{< pr 130 >}}
* TEST: ci testing to run generated dockerfile in {{< pr 136 >}}
* MAINT: rsconnect-python>=1.8.0 in {{< pr 132 >}}
* ENH: New `prepare_docker` function in {{< pr 137 >}}
* DOC: refresh README and add to docs in {{< pr 141 >}}
* TEST: Update weekly tests: only run necessary tests in {{< pr 142 >}}
* MAINT: update `ptype_data` to `prototype_data` in {{< pr 138 >}}
* ENH: Refactor metadata in {{< pr 126 >}}
* MAINT: remove stars for explicit imports in {{< pr 145 >}}
* DOC: Changing language from "Example" to "Examples" for docstrings in {{< pr 146 >}}
* ENH: Added Python version to `vetiver_pin_write` in {{< pr 127 >}}


## v0.1.8
### What's Changed

[**Full Changelog**](https://github.com/rstudio/vetiver-python/compare/v0.1.7...v0.1.8)

* TEST: pins<>vetiver compatibility test in {{< pr 113 >}}
* TEST: Update weekly tests to include `rsconnect-python` in {{< pr 117 >}}
* DOC: Missing whitespace in InvalidModelError in {{< pr 120 >}}
* MAINT: Remove xfail from `test_rsconnect` in {{< pr 119 >}}
* MAINT: Add httpx in {{< pr 125 >}}
* ENH: Add pin URL to REST API and metadata in {{< pr 123 >}}


## v0.1.7
### What's Changed

[**Full Changelog**](https://github.com/rstudio/vetiver-python/compare/v0.1.6...v0.1.7)

* ENH, DOC: have stable and latest docs in {{< pr 93 >}}
* BUG: bug fix for load_pkgs function on Windows OS in {{< pr 98 >}}
* MAINT: Update attach_pkgs.py in {{< pr 99 >}}
* ENH: implement statsmodels handler in {{< pr 100 >}}
* FEAT: xgboost handler in {{< pr 101 >}}
* ENH: adding model card template in {{< pr 106 >}}
* BUG: refactor pseudo version to pin_url in model card in {{< pr 107 >}}
* DOC: adding docs, small refactoring in {{< pr 108 >}}
* ENH, DOC: add examples to docstrings in {{< pr 109 >}}


## v0.1.6
### What's Changed

[**Full Changelog**](https://github.com/rstudio/vetiver-python/compare/v0.1.5...v0.1.6)

* ENH: add `rsconnect_deploy` support for `board_folder` in {{< pr 77 >}}
* ENH: model monitoring in {{< pr 76 >}}
* DOC: add mini chicago dataset in {{< pr 81 >}}
* MAINT: remove trailing slashes in API paths {{< pr 83 >}}
* ENH: explicitly add `n` to hover data in `plot_metrics` in {{< pr 84 >}}
* ENH: initial vetiver_pin_metrics implementation in {{< pr 82 >}}
* MAINT, ENH: Use setuptools_scm for tagged versioning in {{< pr 86 >}}
* ENH: handlers to register themselves in {{< pr 87 >}}
* BUG: coerce date var to datetime in {{< pr 89 >}}
