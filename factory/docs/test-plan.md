# Test plan — factory

Every case the factory commits to covering, and the test function that covers it. Built test-first: cases
are agreed here, tests are written against them, then the code is written to pass. The **Test function**
column is the auditable trail — an empty cell means the case is agreed but not yet covered.

`factory/` is one unit of development, so this is its single plan. See
[test-first-process.md](../../docs/test-first-process.md) for the process.

## Prefix legend

Case IDs are prefixed by the surface they cover, and never renumbered (retire an ID rather than reuse
it). Helper prefixes name the module; step prefixes are the process letter plus the step number, so a
case ID says where in the factory the behaviour lives.

| Prefix | Surface it covers |
|---|---|
| HFC | `common/helpers/format_contract.py` — locating a format doc, parsing its `## Skeleton` contract |
| HNUM | `common/helpers/numeric.py` — number coercion and display used in validator reporting |
| HMDT | `common/helpers/md_table.py` — reading markdown tables out of a document |

A prefix names the **surface** — a module or an artefact — not its position in the factory. Step numbers
are deliberately absent: steps are retired rather than renumbered, so a positional prefix would go stale
the moment a step moved, and the linter's ID grammar (`[A-Z]{1,5}-\d{1,3}`) admits letters only. Add a
row here when a new surface gains its first case.

## Fixtures

The fake objects the suite needs, named and purposed.

| Fixture | Purpose |
|---|---|
| `format_doc` | writes a minimal format document containing a `## Skeleton` fenced block, so contract parsing is tested against a real file rather than an inline string |
| `doc_tree` | builds a temporary directory tree (a step folder, a nested `scripts/` dir, an umbrella-style `docs/` dir) so document lookup can be tested from several starting points |

## Cases

### HFC — `format_contract.py`

`find_format_doc(name, explicit=None, start=None)` — locate the format document a validator is driven by.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HFC-01 | an explicit path that exists is returned unchanged | `test_explicit_path_that_exists_is_returned` |
| HFC-02 | an explicit path that does not exist returns None | `test_explicit_path_that_is_missing_returns_none` |
| HFC-03 | the document is found beside the starting directory | `test_found_beside_the_starting_directory` |
| HFC-04 | the document is found in a `docs/` directory while walking up from the start | `test_found_in_a_docs_dir_walking_up` |
| HFC-05 | a number-prefixed variant (`_02_<name>`) is found beside the starting directory — the factory step-folder convention | `test_number_prefixed_variant_is_found` |
| HFC-06 | None is returned when the document is nowhere on the search path | `test_returns_none_when_nowhere_on_the_path` |
| HFC-07 | the nearest match wins when the document exists at more than one level | `test_nearest_match_wins` |

`parse_contract(format_text)` — read the machine-readable contract out of the `## Skeleton` block.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HFC-08 | `##` headings inside the Skeleton block are returned, de-duplicated, in document order | `test_headings_are_returned_in_order_deduplicated` |
| HFC-09 | `- Label:` field names inside the Skeleton block are returned | `test_labelled_field_names_are_returned` |
| HFC-10 | the column names of the first table header row in the block are returned | `test_grid_columns_come_from_the_first_header_row` |
| HFC-11 | the table separator row is not mistaken for a header row | `test_separator_row_is_not_read_as_a_header` |
| HFC-12 | three empty lists are returned when there is no `## Skeleton` block | `test_no_skeleton_block_returns_three_empty_lists` |
| HFC-13 | headings and fields outside the Skeleton block are ignored | `test_content_outside_the_skeleton_is_ignored` |
| HFC-21 | a **bold** field label is returned without its emphasis markers | `test_bold_field_label_is_returned_unwrapped` |

`parse_labelled_fields(text)` — read `- Label: value` lines from a document body.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HFC-14 | `- Label: value` lines are read into a mapping | `test_labelled_lines_are_read_into_a_mapping` |
| HFC-15 | lines that are markdown table rows are ignored | `test_table_rows_are_ignored` |
| HFC-16 | a repeated label keeps the last value | `test_repeated_label_keeps_the_last_value` |
| HFC-17 | a line with no colon is ignored | `test_line_without_a_colon_is_ignored` |
| HFC-18 | an indented line after a labelled field continues that field's value | `test_indented_line_continues_the_field` |
| HFC-19 | continuation ends at the next unindented line | `test_continuation_ends_at_the_next_unindented_line` |
| HFC-20 | a continued value keeps its line breaks, so a document can render it as written | `test_continued_value_keeps_its_line_breaks` |
| HFC-22 | a **bold** label is read without its markers, and its value without the closing ones | `test_bold_label_and_value_are_unwrapped` |
| HFC-23 | a value that is *itself* emphasised keeps its emphasis — only the label's own markers are removed | `test_emphasised_value_keeps_its_emphasis` |

HFC-21 and HFC-22 were added when the assessment-plan standard was ported: it writes
`- **UoC coverage:** …`, with the colon *inside* the emphasis. Unwidened, the label came back as
`**UoC coverage` and the value carried a leading `**`. Bold labels are ordinary in these documents, so
the helper handles them rather than every caller stripping markers itself.

### HNUM — `numeric.py`

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HNUM-01 | an integer is parsed out of a string | `test_integer_is_parsed_from_a_string` |
| HNUM-02 | a decimal is parsed out of a string | `test_decimal_is_parsed_from_a_string` |
| HNUM-03 | a unicode minus (`−`) is read as a negative sign | `test_unicode_minus_is_read_as_negative` |
| HNUM-04 | None is returned when the string contains no number | `test_string_without_a_number_returns_none` |
| HNUM-05 | None is returned for a None input | `test_none_input_returns_none` |
| HNUM-06 | an integral value is displayed without a decimal point | `test_integral_value_displays_without_a_decimal_point` |
| HNUM-07 | a non-integral value is displayed with its decimal part | `test_non_integral_value_keeps_its_decimal_part` |

### HMDT — `md_table.py`

Reading markdown tables. Nine scripts across the repo carry their own copy of this parsing; this is
the one implementation. Rows keep their source line number, so a validator can point a human at the
line that needs fixing.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HMDT-01 | a pipe-delimited row splits into stripped cell values | `test_row_splits_into_stripped_cells` |
| HMDT-02 | the leading and trailing pipes are not returned as cells | `test_outer_pipes_are_not_cells` |
| HMDT-03 | an empty cell is preserved as an empty string, not dropped | `test_empty_cell_is_preserved` |
| HMDT-04 | a dashes-only row is recognised as the separator under a table header | `test_separator_row_is_recognised` |
| HMDT-05 | a row of real content is not mistaken for a separator | `test_content_row_is_not_a_separator` |
| HMDT-06 | the rows under a heading are returned, header row first | `test_rows_are_returned_header_first` |
| HMDT-07 | the separator row is not returned as data | `test_separator_row_is_not_returned` |
| HMDT-08 | each row carries its 1-based source line number | `test_each_row_carries_its_source_line_number` |
| HMDT-09 | reading stops at the next heading | `test_reading_stops_at_the_next_heading` |
| HMDT-10 | an absent heading yields no rows | `test_absent_heading_yields_no_rows` |
| HMDT-11 | the heading is matched case-insensitively, on a substring | `test_heading_matches_case_insensitively_on_a_substring` |
| HMDT-12 | prose between the heading and the table is skipped | `test_prose_between_heading_and_table_is_skipped` |
