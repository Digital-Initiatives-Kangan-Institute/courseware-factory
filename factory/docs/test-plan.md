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
| HIR | `common/helpers/item_reference.py` — the canonical `[UNIT SECTION numbering]` reference: reading, writing, recognising, resolving |
| HUS | `common/helpers/uoc_sections.py` — which UoC sections a Topic teaches, in institutional vocabulary |
| HDT | `common/helpers/docx_template.py` — filling an institutional .docx template without disturbing its formatting |
| HDX | `common/helpers/docx_text.py` — reading text and block structure out of a .docx body |
| HCOS | `common/helpers/cosmetic.py` — folding the character substitutions Word makes, so a diff can tell them from real edits |
| HMS | `common/helpers/md_section.py` — the lines of one section of a markdown document |
| HSR | `common/helpers/scenario_requirement.py` — the `SR-<CLUSTER>-NN` reference: what the scenario must supply |
| HLLN | `common/helpers/lln_requirements.py` — deriving a cluster's LLN requirements from its units' Foundation Skills |
| HDCD | `common/helpers/docx_code.py` — monospaced code blocks in a .docx body |
| HDBT | `common/helpers/docx_body_text.py` — body paragraphs, bullet lists, guidance and response placeholders |
| HDST | `common/helpers/docx_styling.py` — cell and paragraph shading, borders, rules and field codes |
| HUT | `common/helpers/uoc_tags.py` — the small visual UoC evidence tag stamped into a document |
| HDEV | `common/helpers/docx_evidence.py` — evidence lines: not-applicable markers and described evidence |
| HDCO | `common/helpers/docx_callouts.py` — callout boxes: applicability notes and convention boxes |
| HDTB | `common/helpers/docx_tables.py` — building and filling tables: template, data, instruction and criterion rows |
| HSD | `common/helpers/scenario_document.py` — the in-world scenario document letterhead: styles, wordmark, header and footer |
| HPB | `common/helpers/pptx_brand.py` — the 16:9 branded slide deck for in-world scenario presentations |
| IKD | `institutions/kangan/kangan_deck.py` — the Kangan teaching-deck layouts (an institution pack, outside `factory/`) |
| HDI | `common/helpers/deck_images.py` — resolving a slide plan's `image:` directive into a placement |
| HIL | `common/helpers/instrument_layout.py` — turning an instrument's flat content into navigable .docx layout |
| HRS | `common/helpers/run_sheet.py` — the workbook engine: one content definition rendered as student, assessor and practice sheets |
| HWI | `common/helpers/workbook_instrument.py` — deriving the marking guide, reverse map and coverage gaps from a workbook's own tags |
| IKT | `institutions/kangan/instrument_template.py` — filling the Kangan instrument templates with a workbook instrument |
| TU | `process_01_extraction/step_101_transcribe_uoc/` — `transcribe_uoc.py` |
| VU | `process_01_extraction/step_101_transcribe_uoc/` — `validate_uoc.py`, the step's gate |
| IU | `process_01_extraction/step_102_consolidate_uoc/` — `inventory_uoc.py` |
| VCI | `process_01_extraction/step_102_consolidate_uoc/` — `validate_consolidated_items.py`, one of the step's two gate scripts |

A prefix names the **surface** — a module or an artefact — not its position in the factory. Step numbers
are deliberately absent: steps are retired rather than renumbered, so a positional prefix would go stale
the moment a step moved, and the linter's ID grammar (`[A-Z]{1,5}-\d{1,3}`) admits letters only. Add a
row here when a new surface gains its first case.

## Fixtures

The fake objects the suite needs, named and purposed.

| Fixture | Purpose |
|---|---|
| `_fixtures/brand.py` | a neutral brand pack (palette, font, org identity) standing in for a course's `brand.py`, so the document-styling helpers are tested without any real course |
| `format_doc` | writes a minimal format document containing a `## Skeleton` fenced block, so contract parsing is tested against a real file rather than an inline string |
| `doc_tree` | builds a temporary directory tree (a step folder, a nested `scripts/` dir, an umbrella-style `docs/` dir) so document lookup can be tested from several starting points |
| `docx_fixtures` | Word-XML builders (`p`, `raw_p`, `tbl`, `sdt`, `wrap`, `make_docx`) that assemble a `.docx` from literal strings. Independent ground truth: never the transcriber's own output, because a reader tested against its own consumer only proves the two agree with each other. Writes only the zip parts under test — enough for a zip-reading extractor, not a Word-openable file. |
| `_fixtures/institution.py` | a neutral institution pack (`BODY_STYLE = "Body Text"`, a style a blank python-docx document carries) standing in for an institution's `institution.py`, so layout helpers are tested without any real institution's template |

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

### HIR — `item_reference.py`

The canonical reference every artefact downstream of extraction trades in: `[ICTCLD501 PC 1.2]`. Four
scripts had grown their own copy of the pattern; this is the one definition, and it holds the **writer
and the reader together** so the two cannot drift.

**Any correctly-formed unit code, not an allow-list.** The legacy copies matched `ICT`, `BSB` or `VU`
only, so a cluster of units from any other training package crashed the gate with an `AttributeError`
on an unmatched search. The factory is meant to serve any qualification, so the pattern describes the
*shape* of a unit code — two or more leading capitals, then alphanumerics, ending in at least three
digits. Proven equivalent on the corpus before adoption: 373 references across all three consolidated
documents, identical sets under both patterns.

`format(unit, section, numbering)`

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HIR-01 | a reference renders as `[UNIT SEC numbering]` | `test_reference_renders_in_canonical_form` |
| HIR-02 | an FS numbering is a skill name and keeps its spaces | `test_foundation_skill_numbering_keeps_its_spaces` |

`first(text)` — the first reference in a body of text, or None.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HIR-03 | a well-formed reference yields unit, section and numbering | `test_well_formed_reference_is_parsed` |
| HIR-04 | surrounding whitespace is stripped from the numbering | `test_numbering_whitespace_is_stripped` |
| HIR-05 | any training package is accepted, not an allow-list | `test_any_training_package_is_accepted` |
| HIR-06 | a Victorian accredited code is accepted | `test_accredited_course_unit_code_is_accepted` |
| HIR-07 | a code with no trailing digits is not a reference | `test_code_without_trailing_digits_is_not_a_reference` |
| HIR-08 | a code that starts with digits is a course, not a unit | `test_course_code_is_not_a_unit_reference` |
| HIR-09 | an unrecognised section is not a reference | `test_unrecognised_section_is_not_a_reference` |
| HIR-10 | text containing no reference yields None rather than raising | `test_text_without_a_reference_yields_none` |

HIR-10 is the crash the legacy copies carried: an unmatched search went straight to `.group(1)`, so a
unit outside the allow-list produced a stack trace rather than a message naming the reference.

`find_all(text)`

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HIR-11 | every reference is returned, in document order | `test_every_reference_in_document_order` |
| HIR-12 | a line carrying no reference contributes nothing | `test_line_without_a_reference_contributes_nothing` |
| HIR-13 | a repeated reference is returned once per occurrence, **not de-duplicated** | `test_repeated_reference_is_not_deduplicated` |

HIR-13 is load-bearing: the consolidation gate counts occurrences to catch an item placed in two groups,
so de-duplicating here would silently disable that check.

`strip_code_spans(text)` — a backtick-wrapped reference is a prose citation, not an item.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HIR-14 | a backtick-wrapped reference is removed | `test_wrapped_reference_is_removed` |
| HIR-15 | an unwrapped reference survives | `test_unwrapped_reference_survives` |
| HIR-16 | the prose around a removed span survives | `test_prose_around_a_removed_span_survives` |
| HIR-17 | a reference built by `format` parses back to what it was built from | `test_format_and_first_round_trip` |

`expand(numbering)` — a compressed numbering into its members.

A reference may name several items at once. Downstream every coverage check counts *items*, so a
compressed reference that is not expanded reads as one item and the register silently shrinks.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HIR-18 | a plain number passes through unchanged | `test_plain_number_passes_through` |
| HIR-19 | an integer range expands to every member | `test_integer_range_expands` |
| HIR-20 | a dotted range expands within its major | `test_dotted_range_expands_within_its_major` |
| HIR-21 | a comma list expands to each member | `test_comma_list_expands` |
| HIR-22 | a comma list containing a range expands fully | `test_comma_list_containing_a_range_expands` |
| HIR-23 | a dotted range spanning two majors yields only its endpoints | `test_range_across_majors_yields_endpoints` |
| HIR-24 | a Foundation Skill name passes through unchanged | `test_skill_name_passes_through` |
| HIR-25 | a trailing qualifier is dropped | `test_trailing_qualifier_is_dropped` |

`resolve(line)` — every reference a line makes, expanded and attributed.

Yields `((unit, section, numbering), form)` where form is `full`, `abbrev`, `compressed` or
`unresolved`. The form matters to callers: a compressed reference covers its members but was not
written item by item, which some checks report differently.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HIR-26 | a full reference resolves, form `full` | `test_full_reference_resolves` |
| HIR-27 | an abbreviated reference inherits the unit from the nearest preceding full one, form `abbrev` | `test_abbreviated_reference_inherits_the_unit` |
| HIR-28 | an abbreviated reference with no preceding unit is `unresolved`, and carries no unit | `test_abbreviated_without_a_unit_is_unresolved` |
| HIR-29 | a compressed reference yields one entry per member, form `compressed` | `test_compressed_reference_yields_each_member` |
| HIR-30 | a compound reference splits on the middle dot, each part resolved independently | `test_compound_reference_splits_on_the_middle_dot` |
| HIR-31 | every part of a compound is classified `compressed`, even a single-item part | `test_compound_parts_are_classified_compressed` |
| HIR-32 | unit inheritance carries across brackets on the same line | `test_unit_inheritance_carries_across_brackets` |
| HIR-33 | bracketed text that is not a reference is ignored rather than unresolved | `test_bracketed_prose_is_ignored` |
| HIR-34 | references are yielded in line order | `test_references_are_yielded_in_line_order` |

HIR-31 is not pedantry: a compound like `[ICTCLD401 KE 1 · ICTCLD502 KE 1]` has two single-item parts,
and both are `compressed` — the *reference* was compressed even though each member is singular.

HIR-28 is a **deliberate deviation from the legacy behaviour**, which yielded the sentinel string
`"?? PC 2.1"` for callers to detect with `startswith("?? ")`. This module speaks tuples and the `form`
field already says `unresolved`, so the unit is simply `None` and there is no sentinel to parse.

`valid_set(text)` — the set of references a document actually defines.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HIR-35 | every reference in the text is returned, de-duplicated | `test_valid_set_is_deduplicated` |
| HIR-36 | a backtick-wrapped reference is excluded — a prose citation is not a definition | `test_valid_set_excludes_wrapped_references` |

### HUS — `uoc_sections.py`

Which UoC **sections** a Topic teaches (not which items), mapped to the institutional Delivery Mapping
vocabulary. Deliberately narrow: the docx column is a five-value dropdown, so no range expansion or
unit inheritance is needed — that machinery already exists in `validate_at_traceability.resolve_tags`
and is not duplicated here.

`taught_block(text)` — the taught/developed portion of a `coverage.md`.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HUS-01 | the block runs from the UoC-mapping heading to the next `##` heading | `test_block_runs_from_mapping_heading_to_next_h2` |
| HUS-02 | an "applied earlier / elsewhere" marker truncates the block | `test_applied_earlier_marker_truncates_the_block` |
| HUS-03 | content before the mapping heading is excluded | `test_content_before_the_mapping_heading_is_excluded` |
| HUS-04 | an absent mapping heading yields an empty block | `test_absent_mapping_heading_yields_an_empty_block` |

`sections_taught(text)` — the section codes tagged within that block.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HUS-05 | a section code is collected from a canonical unwrapped tag | `test_section_is_collected_from_a_canonical_tag` |
| HUS-06 | a backtick-wrapped tag is not counted — the canonical form is unwrapped | `test_wrapped_tag_is_not_counted` |
| HUS-07 | a section appearing many times is reported once | `test_repeated_section_is_reported_once` |
| HUS-08 | tags outside the taught block are not counted | `test_tags_outside_the_taught_block_are_not_counted` |
| HUS-09 | a line carrying no tag contributes nothing | `test_line_without_a_tag_contributes_nothing` |
| HUS-10 | a malformed bracket is ignored rather than raising | `test_malformed_bracket_is_ignored` |
| HUS-17 | a section is collected from a unit of any training package, not only ICT/BSB/VU | `test_section_is_collected_from_any_training_package` |

HUS-17 was added when the helper ported to the courseware-factory: the tag pattern carried an allow-list
of the pilot's unit prefixes, so a Topic tagged with a unit from another training package (`HLTINF006`)
reported teaching nothing. The unit code now comes from `item_reference.UNIT_CODE`, the one definition.

`to_delivery_mapping(sections)` — our section codes as the template's dropdown values.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HUS-11 | `PC` maps to `PC` | `test_pc_maps_to_pc` |
| HUS-12 | `KE` maps to `Know` | `test_ke_maps_to_know` |
| HUS-13 | `PE` and `FS` both map to `Skill` | `test_pe_and_fs_both_map_to_skill` |
| HUS-14 | `AC` maps to `Cond` | `test_ac_maps_to_cond` |
| HUS-15 | the result is de-duplicated and in a stable order | `test_result_is_deduplicated_and_stably_ordered` |
| HUS-16 | a section with no institutional equivalent is dropped | `test_section_with_no_institutional_equivalent_is_dropped` |

### HDT — `docx_template.py`

Filling an **institutional** template — a document someone else designed, whose formatting must
survive. Distinct from `scripts/helpers/docx_tables.py`, which *builds* branded tables from nothing:
there the styling is ours to set, here it is theirs to preserve.

`clone_block_after(paragraph, table)` — repeat a heading-plus-table unit.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HDT-01 | the document gains one paragraph and one table | `test_document_gains_one_paragraph_and_one_table` |
| HDT-02 | the clone sits immediately after the source table in document order | `test_clone_sits_immediately_after_the_source_table` |
| HDT-03 | the clone's paragraph carries the same text as the source | `test_clone_paragraph_carries_the_same_text` |
| HDT-04 | the clone's table has the same row and column count as the source | `test_clone_table_has_the_same_shape` |
| HDT-05 | editing the clone leaves the source untouched | `test_editing_the_clone_leaves_the_source_untouched` |

`set_cell_text(cell, text)` — write a value into a template cell, keeping the template's formatting.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HDT-06 | the cell reads back the value written | `test_cell_reads_back_the_value_written` |
| HDT-07 | the existing run's formatting survives the write | `test_existing_run_formatting_survives_the_write` |
| HDT-08 | a cell with no runs yet can still be written to | `test_cell_with_no_runs_can_still_be_written` |
| HDT-09 | a multi-line value becomes one paragraph per line | `test_multiline_value_becomes_one_paragraph_per_line` |
| HDT-10 | writing replaces the previous content rather than appending to it | `test_writing_replaces_rather_than_appends` |

`ensure_row_cells(row, n)` — a supplied template may ship rows narrower than its own header.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HDT-11 | a row shorter than the header gains cells until it matches | `test_narrow_row_gains_cells_until_it_matches` |
| HDT-12 | a row already wide enough is left untouched | `test_wide_enough_row_is_untouched` |
| HDT-13 | added cells copy the formatting of the row's last cell | `test_added_cells_copy_the_last_cells_formatting` |

`set_cell_block(cell, blocks)` — write real content where the template held a styled placeholder.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HDT-14 | each block becomes its own paragraph, in order | `test_each_block_becomes_its_own_paragraph` |
| HDT-15 | a block marked as a heading is bold | `test_heading_block_is_bold` |
| HDT-16 | a block not marked as a heading is not bold | `test_non_heading_block_is_not_bold` |
| HDT-17 | filled content is explicitly black, overriding any colour the placeholder's **style** carries | `test_placeholder_colour_is_cleared` |
| HDT-18 | `set_cell_text` removes any content control the cell held — a filled cell must not still offer its dropdown | `test_writing_removes_a_content_control` |
| HDT-22 | `set_cell_block` removes it too | `test_writing_a_block_removes_a_content_control` |
| HDT-19 | a cell wrapped in a content control is promoted to a real cell on its row | `test_wrapped_cell_is_promoted_to_a_real_cell` |
| HDT-20 | promoting leaves the row's cells in their original left-to-right order | `test_promoting_preserves_left_to_right_order` |
| HDT-21 | a row whose cells are all wrapped ends up with every cell writable | `test_every_cell_is_writable_after_promoting` |

### HDX — `docx_text.py`

The **one** reader both step-101 scripts go through: the transcriber to build the markdown, the validator
to say independently what the source contains. Six other validators and two agents currently import
`docx_to_text` out of `validate_uoc.py` and point here as they port.

Element coverage carries most of the cases, because this is the module whose blindness nothing else can
see. If the reader silently ignores an element type, the character is missing from the transcription
*and* from the text it is compared against, the two agree, and the gate reports a verbatim match over
content that was dropped. The list-shape check in the validator is the one part deliberately kept
independent of this module.

`body(path)` — open the zip and reach the document body.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HDX-01 | the body element is returned from a `.docx` | `test_body_is_returned_from_a_docx` |
| HDX-02 | a document with no `w:body` returns None rather than raising | `test_document_without_a_body_returns_none` |
| HDX-03 | only `word/document.xml` is read — content in a header or footer part cannot reach the output | `test_header_and_footer_parts_are_not_read` |

`para_text(p)` — one paragraph's text, across every element that carries any.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HDX-04 | `w:t` runs concatenate in source order | `test_text_runs_concatenate_in_source_order` |
| HDX-05 | `w:tab` becomes a tab character | `test_tab_becomes_a_tab_character` |
| HDX-06 | `w:br` becomes a newline | `test_break_becomes_a_newline` |
| HDX-07 | `w:cr` becomes a newline | `test_carriage_return_becomes_a_newline` |
| HDX-08 | `w:sym` renders the character named in its `w:char` attribute — content held in an attribute is not lost | `test_symbol_renders_its_char_attribute` |
| HDX-09 | `w:noBreakHyphen` renders as a hyphen character rather than vanishing | `test_non_breaking_hyphen_renders_as_a_hyphen` |
| HDX-10 | an empty `w:t` contributes an empty string rather than raising | `test_empty_text_element_contributes_an_empty_string` |
| HDX-11 | text nested inside a wrapper element (a hyperlink) is still found | `test_text_inside_a_wrapper_element_is_found` |

`para_style(p)` — the style name the transcriber classifies structure from.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HDX-12 | the `w:pStyle` value is returned | `test_paragraph_style_value_is_returned` |
| HDX-13 | a paragraph with no `w:pPr` has no style | `test_paragraph_without_properties_has_no_style` |
| HDX-14 | a `w:pPr` carrying no `w:pStyle` has no style | `test_properties_without_a_style_has_no_style` |

`iter_blocks(parent)` — paragraphs and tables in document order, descending through containers.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HDX-15 | paragraphs and tables are yielded, tagged, in document order | `test_blocks_are_tagged_and_in_document_order` |
| HDX-16 | content inside a `w:sdt` is yielded in place | `test_content_inside_an_sdt_is_yielded_in_place` |
| HDX-17 | blocks inside an unrecognised container are still yielded — a wrapper element cannot hide content | `test_blocks_inside_an_unrecognised_container_are_yielded` |
| HDX-18 | an element that is neither a block nor a container (`w:sectPr`) contributes nothing | `test_a_non_block_element_contributes_nothing` |

`cell_paras(tc)` and `docx_to_text(path)` — table cells, and the flat extraction the validator compares against.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HDX-19 | a cell's paragraphs are returned in order | `test_cell_paragraphs_are_returned_in_order` |
| HDX-20 | paragraphs are joined by newline in document order | `test_paragraphs_are_joined_by_newline_in_document_order` |
| HDX-21 | each table cell contributes its own entry, row by row, cell by cell | `test_each_table_cell_contributes_its_own_entry` |
| HDX-22 | a multi-paragraph cell joins its paragraphs with a newline, lining up with `<br>` in the markdown | `test_multi_paragraph_cell_joins_with_a_newline` |
| HDX-23 | a document with no body yields an empty string | `test_document_without_a_body_yields_empty_text` |

### HCOS — `cosmetic.py`

`normalise(text)` — fold the character substitutions Word makes on the author's behalf, so a comparison
can separate *"the author wrote something different"* from *"Word curled a quote"*.

Used by the transcription gate to grade a difference as cosmetic rather than substantive, and by the
consolidation validator when matching item text. Deliberately narrow: it folds typography, never
whitespace and never a word — collapsing whitespace here would hide a respaced compound
(`IaaS/PaaS/SaaS` retyped as `IaaS / PaaS / SaaS`), which is a real edit.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HCOS-01 | curly single quotes become a straight apostrophe | `test_curly_single_quotes_become_straight` |
| HCOS-02 | curly double quotes become straight double quotes | `test_curly_double_quotes_become_straight` |
| HCOS-03 | en dash, em dash, minus sign and non-breaking hyphen all become a plain hyphen | `test_every_dash_becomes_a_plain_hyphen` |
| HCOS-04 | a non-breaking space becomes an ordinary space | `test_non_breaking_space_becomes_a_space` |
| HCOS-05 | an ellipsis character becomes three dots | `test_ellipsis_becomes_three_dots` |
| HCOS-06 | a soft hyphen is removed — invisible in Word, so it must not survive as a character | `test_soft_hyphen_is_removed` |
| HCOS-07 | a byte-order mark is removed | `test_byte_order_mark_is_removed` |
| HCOS-08 | decomposed characters are composed, so `é` written two ways compares equal | `test_decomposed_characters_are_composed` |
| HCOS-09 | ordinary text passes through unchanged | `test_ordinary_text_is_unchanged` |
| HCOS-10 | normalising twice gives the same result as once — no substitution feeds another | `test_normalising_is_idempotent` |

### HMS — `md_section.py`

`span(text, start, until)` — the lines from a heading matching `start` up to the first line matching any
pattern in `until`.

Validators that check a document section by section need to isolate one section before looking inside
it: "does §3 carry an AT table", "does §6 define any SR rows". Two scripts carried a byte-identical
`section_span`; this is the one implementation.

Distinct from `md_table.rows_under_heading`, which returns *table rows* under a heading and ends at the
next heading of any level. This returns *raw lines* and takes explicit end patterns, because a numbered
section ends at the next numbered section — not at a `###` subheading inside it.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HMS-01 | the section runs from the start line to the first end match | `test_section_runs_to_the_first_end_match` |
| HMS-02 | the start line is included — callers check the heading itself | `test_start_line_is_included` |
| HMS-03 | the end line is excluded | `test_end_line_is_excluded` |
| HMS-04 | an absent start yields None, distinct from an empty section | `test_absent_start_yields_none` |
| HMS-05 | with no end match, the section runs to the end of the document | `test_no_end_match_runs_to_the_end` |
| HMS-06 | whichever end pattern matches first wins, not the first pattern listed | `test_earliest_end_pattern_wins` |
| HMS-07 | an end pattern matching before the start is ignored | `test_end_pattern_before_the_start_is_ignored` |
| HMS-08 | a subheading inside the section does not end it — only an `until` pattern does | `test_subheading_does_not_end_the_section` |

HMS-04 is load-bearing: both callers write `span(...) or ""`, so None means *the document has no §3 at
all* — a format failure worth reporting — while an empty string means *§3 exists and is empty*.
Collapsing them would lose the distinction the caller is making.

### HSR — `scenario_requirement.py`

The system's **second** reference type, and deliberately shaped like the first: `SR-CL2-01` names
something the scenario must supply, the way `[ICTCLD501 PC 1.2]` names something a unit requires. An
assessment plan's §6 defines them; its §3 references them; the scenario plan's build checklist claims
to satisfy them; the consolidated plan unions them.

Four scripts carried five regexes between them, in three different capture shapes. This is the one
definition.

`find_all(text)` — every SR reference, in order.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HSR-01 | every reference in the text is returned, in document order | `test_every_reference_in_document_order` |
| HSR-02 | a reference is returned as written, padding included | `test_reference_is_returned_as_written` |
| HSR-03 | a repeated reference is returned once per occurrence | `test_repeated_reference_is_not_deduplicated` |
| HSR-04 | text carrying no reference yields nothing | `test_text_without_a_reference_yields_nothing` |
| HSR-05 | a reference inside a bold table cell is found | `test_reference_in_a_bold_table_cell_is_found` |
| HSR-06 | a malformed id is not a reference | `test_malformed_id_is_not_a_reference` |
| HSR-07 | the cluster token is any letters-then-digits | `test_cluster_token_is_any_letters_then_digits` |

`parse(sr_id)` — the components, and the canonical ordering.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HSR-08 | an id parses into its cluster prefix, cluster number and sequence | `test_id_parses_into_its_components` |
| HSR-09 | the parse sorts numerically, not lexically | `test_parse_sorts_numerically` |
| HSR-10 | a malformed id yields None rather than raising | `test_malformed_id_parses_to_none` |

**HSR-09 earns the helper.** Sorted as strings, `SR-CL10-01` lands before `SR-CL2-01`, so a consolidated
register spanning ten clusters would be silently mis-ordered. `generate_consolidated_plan._sr_key`
already parses numerically; the other three scripts do not sort at all, so the correct behaviour exists
in exactly one place and would be re-derived wrong by whoever needed it next. `parse` returning
`("CL", 2, 1)` is both the accessor and the sort key — `sorted(refs, key=parse)` is the whole story.

### HLLN — `lln_requirements.py`

The institutional LLN section, derived from the units' own Foundation Skills rather than written by
hand. Only the **LLN-relevant** skills count: a unit's Foundation Skills also cover planning, problem
solving and self-management, which are not language, literacy or numeracy demands.

Cross-process by nature: the source is extraction's `consolidated_uoc.md`; the consumer is a delivery
document. Lives in `common/` for that reason.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HLLN-01 | a Reading skill is collected under the reading heading | `test_reading_is_collected` |
| HLLN-02 | an Oral communication skill is collected under the language heading | `test_oral_communication_is_collected` |
| HLLN-03 | a Writing skill is collected under the writing heading | `test_writing_is_collected` |
| HLLN-04 | a Numeracy skill is collected under the numeracy heading | `test_numeracy_is_collected` |
| HLLN-05 | Planning and organising is excluded — not an LLN demand | `test_planning_and_organising_is_excluded` |
| HLLN-06 | Problem solving and Self-management are excluded | `test_problem_solving_and_self_management_are_excluded` |
| HLLN-07 | skills from every unit in the cluster are amalgamated under one heading | `test_skills_from_every_unit_are_amalgamated` |
| HLLN-08 | an item repeated verbatim across units is listed once | `test_item_repeated_across_units_is_listed_once` |
| HLLN-09 | the trailing source-unit tag is stripped from the item text | `test_source_unit_tag_is_stripped` |
| HLLN-10 | headings are emitted in the institution's order, and an empty heading is omitted | `test_headings_are_ordered_and_empty_ones_omitted` |
| HLLN-11 | rendering produces one bullet per item beneath each heading | `test_rendering_produces_one_bullet_per_item` |
| HLLN-12 | a bullet joining two demands with `<br>` becomes two separate items | `test_br_joined_demands_become_separate_items` |
| HLLN-13 | no markup survives into a demand — the guard against the next tag the source uses | `test_no_markup_survives_into_a_demand` |

### HDCD — `docx_code.py`

Ported from the pilot's legacy `scripts/helpers/`, whose suite had no plan; each case records the
behaviour its existing test already defended.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HDCD-01 | one paragraph per line monospaced | `test_one_paragraph_per_line_monospaced` |
| HDCD-02 | blank line renders as space | `test_blank_line_renders_as_space` |

### HDBT — `docx_body_text.py`

Ported from the pilot's legacy `scripts/helpers/`, whose suite had no plan; each case records the
behaviour its existing test already defended.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HDBT-01 | guidance text is italic grey at guidance size | `test_guidance_text_is_italic_grey_at_guidance_size` |
| HDBT-02 | response placeholder default label italic | `test_response_placeholder_default_label_italic` |
| HDBT-03 | body paragraph text and size | `test_body_paragraph_text_and_size` |
| HDBT-04 | body paragraph returns one paragraph | `test_body_paragraph_returns_one_paragraph` |
| HDBT-05 | one paragraph per item | `test_one_paragraph_per_item` |
| HDBT-06 | text and bullet style | `test_text_and_bullet_style` |
| HDBT-07 | body font size | `test_body_font_size` |
| HDBT-08 | empty is noop | `test_empty_is_noop` |

### HDST — `docx_styling.py`

Ported from the pilot's legacy `scripts/helpers/`, whose suite had no plan; each case records the
behaviour its existing test already defended.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HDST-01 | shade cell sets fill | `test_shade_cell_sets_fill` |
| HDST-02 | shade paragraph sets fill | `test_shade_paragraph_sets_fill` |
| HDST-03 | set cell borders draws all four edges | `test_set_cell_borders_draws_all_four_edges` |
| HDST-04 | paragraph bottom rule adds bottom border | `test_paragraph_bottom_rule_adds_bottom_border` |
| HDST-05 | add field inserts field code | `test_add_field_inserts_field_code` |

### HUT — `uoc_tags.py`

Ported from the pilot's legacy `scripts/helpers/`, whose suite had no plan; each case records the
behaviour its existing test already defended.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HUT-01 | evidence tag prefixes text | `test_evidence_tag_prefixes_text` |
| HUT-02 | evidence tag is small italic teal | `test_evidence_tag_is_small_italic_teal` |

### HDEV — `docx_evidence.py`

Ported from the pilot's legacy `scripts/helpers/`, whose suite had no plan; each case records the
behaviour its existing test already defended.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HDEV-01 | not applicable text bold terracotta | `test_not_applicable_text_bold_terracotta` |
| HDEV-02 | described evidence tag and desc | `test_described_evidence_tag_and_desc` |

### HDCO — `docx_callouts.py`

Ported from the pilot's legacy `scripts/helpers/`, whose suite had no plan; each case records the
behaviour its existing test already defended.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HDCO-01 | applicability note text and colour | `test_applicability_note_text_and_colour` |
| HDCO-02 | convention box shaded cell and bold head | `test_convention_box_shaded_cell_and_bold_head` |

### HDTB — `docx_tables.py`

Ported from the pilot's legacy `scripts/helpers/`, whose suite had no plan; each case records the
behaviour its existing test already defended.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HDTB-01 | add section row bolds label and blanks col1 | `test_add_section_row_bolds_label_and_blanks_col1` |
| HDTB-02 | add criterion row sets yes no | `test_add_criterion_row_sets_yes_no` |
| HDTB-03 | template table shape and placeholder styling | `test_template_table_shape_and_placeholder_styling` |
| HDTB-04 | data table first col bold and money right aligned | `test_data_table_first_col_bold_and_money_right_aligned` |
| HDTB-05 | set cell content multiline replaces | `test_set_cell_content_multiline_replaces` |
| HDTB-06 | find instruction row matches and raises | `test_find_instruction_row_matches_and_raises` |
| HDTB-07 | clear table rows keeps n | `test_clear_table_rows_keeps_n` |

### HSD — `scenario_document.py`

Ported from the pilot's legacy `scripts/helpers/`, whose suite had no plan; each case records the
behaviour its existing test already defended.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HSD-01 | configure styles sets normal and title | `test_configure_styles_sets_normal_and_title` |
| HSD-02 | wordmark two runs branded | `test_wordmark_two_runs_branded` |
| HSD-03 | header footer disclosure and page field | `test_header_footer_disclosure_and_page_field` |

### HPB — `pptx_brand.py`

Ported from the pilot's legacy `scripts/helpers/`, whose suite had no plan; each case records the
behaviour its existing test already defended.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HPB-01 | new deck starts empty | `test_new_deck_starts_empty` |
| HPB-02 | build a small branded deck | `test_build_a_small_branded_deck` |
| HPB-03 | the palette, font and disclosure come from the course's `brand` module, not a copy held here | `test_palette_comes_from_the_course_brand` |

HPB-03 was added when the helper ported to the courseware-factory: it carried its own copy of the pilot
scenario's palette, so any other course's decks came out in the pilot's colours. It now reads `brand`
like every other styling helper.

### IKD — `institutions/kangan/kangan_deck.py`

Ported from the pilot's legacy `scripts/helpers/`, whose suite had no plan; each case records the
behaviour its existing test already defended.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| IKD-01 | new deck starts empty | `test_new_deck_starts_empty` |
| IKD-02 | build a small teaching deck | `test_build_a_small_teaching_deck` |

### HDI — `deck_images.py`

`resolve_image(directive, topic_dir, allow_gen=False)` — one slide's `image:` value as None, a placeholder
(`{"label"}`) or a real picture (`{"path", "label"}`).

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HDI-01 | an empty directive, or `none`, means no image | `test_empty_or_none_means_no_image` |
| HDI-02 | `placeholder <text>` is a labelled placeholder | `test_placeholder_is_labelled` |
| HDI-03 | a bare `placeholder` is labelled with the keyword | `test_bare_placeholder_is_labelled_with_the_keyword` |
| HDI-04 | `reuse <file>` places a committed file from the topic's `images/` | `test_reuse_places_a_committed_file` |
| HDI-05 | `reuse <stem>` with no extension matches the committed file of any extension | `test_reuse_stem_matches_any_extension` |
| HDI-06 | `reuse <file>` not yet committed falls back to a labelled placeholder | `test_reuse_missing_file_is_a_placeholder` |
| HDI-07 | `gen <prompt>` with a committed `gen-<hash>` cache is placed without `allow_gen` | `test_gen_cache_hit_is_placed_without_allow_gen` |
| HDI-08 | `gen <prompt>` with no cache and no `allow_gen` is a placeholder and calls nothing — the cost guard | `test_gen_miss_without_allow_gen_calls_nothing` |
| HDI-09 | an unknown keyword is a placeholder naming the raw directive, so nothing is silently dropped | `test_unknown_keyword_is_a_placeholder` |
| HDI-10 | `diagram <ref>` with no spec raises, naming the missing spec path | `test_diagram_without_spec_raises_naming_the_path` |
| HDI-11 | the directive keyword is case-insensitive | `test_keyword_is_case_insensitive` |

Written when the helper ported to the courseware-factory: the pilot had no tests for it. The two routes
that shell out to a skill — rendering a diagram, and generating a missing image — are not unit cases;
they depend on the draw-diagram and image-gen skills, and are covered when those port.

### HIL — `instrument_layout.py`

Written when the helper ported to the courseware-factory: the pilot had no tests for it.

`add_hyperlink(paragraph, text, url, colour, size_pt)` — python-docx has no native hyperlink.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HIL-01 | a hyperlink is appended whose external relationship targets the URL | `test_hyperlink_targets_the_url_externally` |
| HIL-02 | the link run is underlined and link-blue by default, and takes a size when given | `test_hyperlink_is_underlined_link_blue_and_sized` |

`render_prose(doc, prose)` — Instructions-to-Student prose from `(text, style)` pairs.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HIL-03 | an `item` entry is bulleted with its lead-in, up to ` — `, in bold | `test_item_entry_bolds_its_lead_in` |
| HIL-04 | a `bullet` entry is a plain bulleted line | `test_bullet_entry_is_a_plain_bulleted_line` |
| HIL-05 | a link entry (style `link` + URL) is a bulleted clickable link | `test_link_entry_is_a_bulleted_clickable_link` |
| HIL-06 | any other style is a paragraph in that Word style, with heading spacing for a heading | `test_other_style_is_a_paragraph_in_that_style` |

`set_cell_rich(cell, blocks)` — an instruction-table cell from `(text, kind)` blocks.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HIL-07 | the cell's previous content is replaced, keeping its first paragraph's style | `test_cell_content_is_replaced_keeping_its_style` |
| HIL-08 | `h` is a bold sub-heading, `b` a bulleted entry, and a link kind (`link` + URL) a bulleted link | `test_cell_blocks_render_by_kind` |

`render_benchmark(doc, blocks, render_table, styles)` — the assessor-only benchmark body, shape inferred from the text.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HIL-09 | `N. …` becomes Heading 2 and `N.N …` Heading 3 | `test_numbered_lines_become_headings` |
| HIL-10 | a `UoC evidenced:` line is muted, italic, 9 pt | `test_uoc_evidenced_line_is_muted_italic_small` |
| HIL-11 | `NYS: …` has a bold lead-in and a plain remainder | `test_nys_line_has_a_bold_lead_in` |
| HIL-12 | a line ending in `:` is a bold label, and the lines after it are bulleted | `test_label_line_bullets_what_follows` |
| HIL-13 | a `tbl` block is handed to `render_table`, and ends any bulleting | `test_table_block_is_handed_over_and_ends_bulleting` |

`render_flat_prose(doc, lines, headings)` — instruction prose held as flat strings.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HIL-14 | a heading line becomes Heading 2, and its flag decides whether the block under it is bulleted | `test_heading_flag_decides_bulleting` |
| HIL-15 | a `§…` or `Appendix …` line is a bulleted entry with a bold lead | `test_section_and_appendix_lines_have_a_bold_lead` |
| HIL-16 | a `(text, link + URL)` tuple is a bulleted clickable link | `test_link_tuple_is_a_bulleted_clickable_link` |

The institution seam.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HIL-17 | body text uses the institution pack's body style, not a style name held in the engine | `test_body_text_uses_the_institution_body_style` |

HIL-17 is the port's one behaviour change: the pilot hard-coded the Kangan template's `Assessor text`
style, so any other institution's template failed on a missing style. The name now comes from the
institution pack's `institution.py` — the same seam shape as a course's `brand.py`.

### HRS — `run_sheet.py`

Ported from the pilot's legacy `scripts/helpers/`, whose suite had no plan; each case records the
behaviour its existing test already defended.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HRS-01 | uoc line assessor only | `test_uoc_line_assessor_only` |
| HRS-02 | standard line assessor only | `test_standard_line_assessor_only` |
| HRS-03 | element student copy carries no marking apparatus | `test_element_student_copy_carries_no_marking_apparatus` |
| HRS-04 | element assessor copy carries the model answer | `test_element_assessor_copy_carries_the_model_answer` |
| HRS-05 | response slot blank for student modelled for assessor | `test_response_slot_blank_for_student_modelled_for_assessor` |
| HRS-06 | screenshot slot describes for assessor prompts for student | `test_screenshot_slot_describes_for_assessor_prompts_for_student` |
| HRS-07 | element renders practice scaffolding after the task | `test_element_renders_practice_scaffolding_after_the_task` |
| HRS-08 | given prefills leading columns only | `test_given_prefills_leading_columns_only` |
| HRS-09 | blank rows sets the room offered not the answer count | `test_blank_rows_sets_the_room_offered_not_the_answer_count` |
| HRS-10 | exemplar row renders worked and is announced | `test_exemplar_row_renders_worked_and_is_announced` |
| HRS-11 | exemplar is not announced in the assessor copy | `test_exemplar_is_not_announced_in_the_assessor_copy` |
| HRS-12 | assessor table shows every model row in model colour | `test_assessor_table_shows_every_model_row_in_model_colour` |

### HWI — `workbook_instrument.py`

Written when the helper ported to the courseware-factory: the pilot had no tests for it. Only the
derivation ported; filling the institution's template (`assemble`) belongs to the institution pack.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| HWI-01 | tasks are keyed by number and questions by `Q<n>`, so a criterion can group either | `test_tasks_and_questions_are_keyed_separately` |
| HWI-02 | a criterion's tasks may be numbers, `Q` keys, or `lo-hi` ranges | `test_criterion_tasks_accept_numbers_q_keys_and_ranges` |
| HWI-03 | a criterion's UoC line is the union of its tasks' tags, de-duplicated, in the order the workbook introduces them | `test_uoc_line_is_the_ordered_union_of_task_tags` |
| HWI-04 | a criterion naming a task that does not exist raises, naming the task | `test_unknown_task_raises_naming_it` |
| HWI-05 | a criterion whose tasks carry no tags raises — it would be a free-floating criterion | `test_untagged_criterion_raises` |
| HWI-06 | the mapping engine's `BENCHMARK` comes from the same derivation as the marking guide | `test_benchmark_comes_from_the_marking_derivation` |
| HWI-07 | item text is read verbatim from `consolidated_uoc.md` bullets, FS bold names and `<br>` normalised | `test_item_text_is_read_verbatim_and_normalised` |
| HWI-08 | a unit's reverse map holds only that unit's tags, ordered PC, PE, KE, FS, AC and numerically, each with its criteria | `test_reverse_map_is_per_unit_and_ordered` |
| HWI-09 | a tag absent from `consolidated_uoc.md` raises as a phantom rather than printing a plausible row | `test_phantom_tag_raises` |
| HWI-10 | assessment conditions appear as pre-condition rows | `test_conditions_are_pre_condition_rows` |
| HWI-11 | expected items no criterion covers are reported, in order | `test_unevidenced_items_are_reported_in_order` |
| HWI-12 | the benchmark body is a heading, the intro, and one reverse-map table per unit | `test_benchmark_body_has_one_table_per_unit` |
| HWI-13 | a unit from any training package is recognised in `consolidated_uoc.md` | `test_any_training_package_unit_is_recognised` |

### IKT — `institutions/kangan/instrument_template.py`

`assemble(template_path, spec, mode, render_body, benchmark=None)` — moved from the pilot's
`workbook_instrument.py`, which had no tests for it: it is shaped entirely by the Kangan templates'
tables, so it belongs to the Kangan pack. Tested against the pack's real templates.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| IKT-01 | the assessor copy's Details rows take the qualification, units, task title and task number | `test_assessor_details_are_filled` |
| IKT-02 | the student copy's Details are filled one row lower — the student template's extra leading row | `test_student_details_sit_one_row_lower` |
| IKT-03 | instruction rows are filled by their label; the assessor copy gets the assessor overview and resources, the student copy the student ones | `test_instruction_rows_follow_the_copy` |
| IKT-04 | the assessor copy clears Location and gains an Assessment Conditions & Setup Requirements row; the student copy has neither | `test_conditions_row_is_assessor_only` |
| IKT-05 | the marking table shows the student only criterion statements, and the assessor the statements with their UoC lines | `test_marking_table_follows_the_copy` |
| IKT-06 | the template's guidance boilerplate is removed | `test_template_boilerplate_is_removed` |
| IKT-07 | the workbook body is rendered by the caller's `render_body`, told which copy it is | `test_body_is_rendered_by_the_caller` |
| IKT-08 | a benchmark is rendered into the assessor copy only | `test_benchmark_is_assessor_only` |

### TU — extraction step 101, `transcribe_uoc.py`

Lifts a unit-of-competency `.docx` into verbatim Markdown. The content guarantee comes from **not
retyping**: text is taken from the Word runs through `docx_text`, so the only thing this script reasons
about is structure — which style is a heading, which is a bullet, where a table starts. Its failure mode
is a mis-shaped heading or bullet, never a changed word, and the step's gate catches that.

Reading the document is `docx_text`'s job and is covered by `HDX-*`. The cases here are the structure
rules and the markdown assembly, which are this script's alone.

`inline(text)` — extracted text as a single markdown line.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| TU-01 | runs of spaces and tabs collapse to a single space | `test_runs_of_whitespace_collapse_to_one_space` |
| TU-02 | an internal line break becomes `<br>` | `test_internal_line_break_becomes_br` |
| TU-03 | leading and trailing whitespace is stripped | `test_surrounding_whitespace_is_stripped` |

`heading_level(style)` — which styles are headings, and at what depth.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| TU-04 | `Title` is level 1 | `test_title_is_level_one` |
| TU-05 | `Heading3` is level 3 | `test_heading3_is_level_three` |
| TU-06 | a style that is not a heading yields no level | `test_non_heading_style_yields_no_level` |
| TU-07 | a paragraph with no style yields no level | `test_absent_style_yields_no_level` |

`list_level(para, style)` — bullet nesting depth. The style suffix is 1-based and the depth is 0-based,
because the consolidation step counts top-level bullets and treats sub-bullets as part of their parent.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| TU-08 | `ListBullet` is depth 0 | `test_list_bullet_is_depth_zero` |
| TU-09 | `ListBullet3` is depth 2 | `test_list_bullet3_is_depth_two` |
| TU-10 | `ListNumber` and `ListParagraph` are list styles too | `test_number_and_paragraph_are_list_styles` |
| TU-11 | a paragraph with no list style takes its depth from `w:numPr`/`w:ilvl` | `test_depth_falls_back_to_the_numbering_level` |
| TU-12 | a `w:numPr` carrying no `w:ilvl` is depth 0 | `test_numbering_without_a_level_is_depth_zero` |
| TU-13 | a plain paragraph is not a list item | `test_plain_paragraph_is_not_a_list_item` |

`cell_md(cell)` and `render_table(tbl)` — a Word table as markdown.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| TU-14 | a cell's paragraphs join with `<br>` | `test_cell_paragraphs_join_with_br` |
| TU-15 | an empty paragraph inside a cell is dropped rather than leaving an empty segment | `test_empty_paragraph_in_a_cell_is_dropped` |
| TU-16 | each row renders as a pipe-delimited line | `test_each_row_renders_pipe_delimited` |
| TU-17 | a separator row follows the header row, and only it | `test_separator_follows_the_header_row_only` |

`transcribe(path)` — the assembly.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| TU-18 | a heading paragraph renders as `#`s at its level | `test_heading_renders_at_its_level` |
| TU-19 | consecutive bullets stay one tight list block | `test_consecutive_bullets_stay_one_block` |
| TU-20 | nesting depth renders as two-space indentation | `test_nesting_renders_as_two_space_indent` |
| TU-21 | an empty paragraph ends an open list | `test_empty_paragraph_ends_an_open_list` |
| TU-22 | an empty paragraph contributes no output of its own | `test_empty_paragraph_contributes_nothing` |
| TU-23 | a table ends an open list and renders as its own block | `test_table_ends_a_list_and_is_its_own_block` |
| TU-24 | blocks are separated by a blank line | `test_blocks_are_separated_by_a_blank_line` |
| TU-25 | the output ends with a single trailing newline | `test_output_ends_with_one_newline` |
| TU-26 | a document with no body yields empty output | `test_document_without_a_body_yields_nothing` |
| TU-27 | header and footer content never reaches the transcription | `test_page_furniture_never_reaches_the_output` |

`main()` — the CLI.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| TU-28 | given an output path, the file is written and its parent directories created | `test_output_path_is_written_creating_parents` |
| TU-29 | given no output path, the markdown goes to stdout | `test_markdown_goes_to_stdout_without_a_path` |
| TU-30 | a wrong argument count exits 2 | `test_wrong_argument_count_exits_two` |

### VU — extraction step 101, `validate_uoc.py`

The Gate 101→102 oracle: proves a `.md` transcription is verbatim against its source `.docx`. Three failure
modes must be caught — content MISSING from the transcription, content NOT IN the source, and content
MISTRANSCRIBED (changed, renumbered, re-cased, re-ordered, duplicated). It must equally not cry wolf on
what is legitimately different: markdown syntax, page furniture, whitespace, and Word's own typography.

**Where its independence now lives.** Both scripts read words through `docx_text`, so the word diff no
longer double-checks extraction — what it checks is that every extracted word survived into the right
structural place. The `docx_list_shape` check is the genuinely independent opinion: it reads bullet
nesting from the source paragraph styles, so a flattened bullet fails even when every word matches.
That matters because step 102 itemises PE/KE/AC by counting top-level bullets — a flattened bullet is a
lost assessable item, not a cosmetic difference.

Fixtures are hand-written Word XML and hand-written markdown, never the transcriber's output: a gate fed
its own subject's work would only prove the two agree with each other.

`md_to_text(path)` — strip markdown syntax, leaving the words.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| VU-01 | a heading loses its `#` markers and keeps its text | `test_heading_markers_are_stripped` |
| VU-02 | a bullet loses its `-` marker and keeps its text | `test_bullet_marker_is_stripped` |
| VU-03 | a numbered item loses its `1.` marker | `test_numbered_marker_is_stripped` |
| VU-04 | a table row becomes one line per cell | `test_table_row_becomes_one_line_per_cell` |
| VU-05 | the dashes-only separator row under a table header contributes nothing | `test_separator_row_contributes_nothing` |
| VU-06 | `<br>` inside a cell becomes a line break, matching how the source cell reads | `test_br_inside_a_cell_becomes_a_line_break` |
| VU-07 | `<br>` in ordinary prose becomes a line break | `test_br_in_prose_becomes_a_line_break` |

`docx_list_shape(path)` / `md_list_shape(path)` — bullet identity, which a word diff cannot see.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| VU-08 | each `List*`-styled body paragraph contributes its nesting depth, in document order | `test_list_paragraphs_contribute_their_depth` |
| VU-09 | any style starting `List` counts — wider than the transcriber's rule, so an unhandled style surfaces rather than flattening silently | `test_any_list_prefixed_style_counts` |
| VU-10 | a `List`-styled paragraph inside a table is not a bullet | `test_list_styled_table_cell_is_not_a_bullet` |
| VU-11 | an empty list paragraph contributes no depth | `test_empty_list_paragraph_contributes_no_depth` |
| VU-12 | markdown bullet depth comes from indentation, two spaces per level | `test_markdown_depth_comes_from_indentation` |

`compare(docx, md)` — the verdict. Not crying wolf.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| VU-13 | a faithful transcription is EXACT | `test_faithful_transcription_is_exact` |
| VU-14 | page furniture in the source does not read as missing content | `test_page_furniture_is_not_missing_content` |
| VU-15 | tabs and line breaks are structure, not content | `test_tabs_and_line_breaks_are_structure` |
| VU-16 | a multi-paragraph cell transcribed with `<br>` is exact, not an insertion | `test_multi_paragraph_cell_is_exact` |
| VU-17 | Word's typography alone grades COSMETIC, not substantive | `test_word_typography_grades_cosmetic` |

Failure mode 1 — content in the source MISSING from the transcription.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| VU-18 | a dropped word fails | `test_dropped_word_fails` |
| VU-19 | a dropped negation fails — the smallest omission that inverts a requirement | `test_dropped_negation_fails` |
| VU-20 | a dropped bullet fails | `test_dropped_bullet_fails` |
| VU-21 | a dropped table cell fails | `test_dropped_table_cell_fails` |
| VU-22 | a truncated trailing section fails | `test_truncated_trailing_section_fails` |

Failure mode 2 — content in the transcription NOT IN the source.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| VU-23 | an added sentence fails | `test_added_sentence_fails` |
| VU-24 | an added bullet fails | `test_added_bullet_fails` |
| VU-25 | an added table row fails | `test_added_table_row_fails` |
| VU-26 | a duplicated item fails | `test_duplicated_item_fails` |

Failure mode 3 — content MISTRANSCRIBED.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| VU-27 | a changed word fails | `test_changed_word_fails` |
| VU-28 | a changed item number fails — numbering is the identity every UoC tag is built from | `test_changed_item_number_fails` |
| VU-29 | a changed quantity fails | `test_changed_quantity_fails` |
| VU-30 | a changed letter case fails | `test_changed_case_fails` |
| VU-31 | reordered items fail — PE bullets are numbered in source order downstream | `test_reordered_items_fail` |
| VU-32 | a respaced compound fails — `IaaS/PaaS/SaaS` respaced is a changed token, not whitespace | `test_respaced_compound_fails` |

Blind spots — a green gate over genuinely missing content is the worst outcome available.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| VU-33 | a source with no extractable words is never a pass | `test_empty_source_is_never_a_pass` |
| VU-34 | a flattened bullet is detected | `test_flattened_bullet_is_detected` |
| VU-35 | an invented bullet is detected | `test_invented_bullet_is_detected` |
| VU-36 | lost nesting depth is detected | `test_lost_nesting_depth_is_detected` |
| VU-37 | a lost symbol character fails | `test_lost_symbol_character_fails` |
| VU-38 | a lost non-breaking hyphen fails | `test_lost_non_breaking_hyphen_fails` |
| VU-39 | a non-breaking hyphen transcribed as a plain hyphen is cosmetic — the right answer must pass | `test_non_breaking_hyphen_as_hyphen_is_cosmetic` |
| VU-40 | a lost carriage return fails | `test_lost_carriage_return_fails` |

`main()` — the CLI, which is what the gate actually runs.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| VU-41 | a faithful pair exits 0 | `test_cli_exits_zero_on_a_faithful_pair` |
| VU-42 | a substantive difference exits 1 — *green on the red run (a raising stub also exits 1); **proven non-vacuous by mutation**: forcing `main` to return 0 turns it red* | `test_cli_exits_one_on_a_substantive_diff` |
| VU-43 | a structure-only difference exits 1 and says LIST STRUCTURE DIFFERS | `test_cli_exits_one_on_a_structure_only_diff` |
| VU-44 | a cosmetic-only difference exits 0 | `test_cli_exits_zero_on_cosmetic_only` |
| VU-45 | an unpaired argument exits 2 — a forgotten `.md` must never be a silent skip | `test_cli_rejects_an_unpaired_argument` |
| VU-46 | every pair is reported before failing, so one bad unit does not mask the ones after it | `test_cli_reports_every_pair_before_failing` |

### IU — extraction step 102, `inventory_uoc.py`

Extracts every PC / FS / PE / KE / AC from a cluster's validated transcriptions as pre-tagged, verbatim
item lines — the raw material the grouping step arranges.

The point matches the transcriber's: consolidation should **arrange** items, never **retype** them. Each
line's text is lifted from the transcription and stamped with its source reference, so the editorial
step only moves tagged lines around and cannot drop, alter or mis-tag an item.

The itemisation rules here are the same ones the step's gate builds its expected set from — the gate
calls this module rather than carrying a second copy, because two mirrored parsers that must agree are
a maintenance hazard, not independent evidence. The independent check lives upstream at Gate 101, where
the `.docx` is the oracle.

`section_body(md, heading)` — the text of one section.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| IU-01 | the text between a heading and the next heading is returned | `test_text_between_headings_is_returned` |
| IU-02 | an absent heading yields nothing | `test_absent_heading_yields_nothing` |
| IU-03 | the last section runs to the end of the document | `test_last_section_runs_to_the_end` |

`parse_pcs(md)` — the performance-criteria column of the Elements table.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| IU-04 | each `N.N …` entry in the criteria column becomes an item carrying its number | `test_each_criterion_becomes_an_item` |
| IU-05 | several criteria in one cell, separated by `<br>`, become separate items | `test_criteria_split_on_br` |
| IU-06 | the element column is not read as criteria | `test_element_column_is_not_criteria` |
| IU-07 | a cell with no `N.N` prefix contributes nothing | `test_cell_without_a_number_contributes_nothing` |

`parse_fs(md)` — the Foundation Skills table.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| IU-08 | each row becomes a skill name and its description | `test_each_row_becomes_skill_and_description` |
| IU-09 | the header row is skipped | `test_header_row_is_skipped` |
| IU-10 | a row with an empty skill name is skipped | `test_row_without_a_skill_name_is_skipped` |

`parse_bullets(md, heading)` — PE / KE / AC itemisation.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| IU-11 | each top-level bullet is one item | `test_each_top_level_bullet_is_an_item` |
| IU-12 | nested sub-bullets stay with their parent, as part of that one item | `test_sub_bullets_stay_with_their_parent` |
| IU-13 | intro prose between the heading and the bullets is ignored | `test_intro_prose_is_ignored` |
| IU-14 | a section whose only top-level bullet ends in `:` promotes its children to items | `test_single_parent_ending_in_colon_promotes_children` |
| IU-15 | that promotion applies only when there is exactly one top-level bullet | `test_promotion_needs_exactly_one_parent` |

`trailing_assessor_ac(md)` and `emit_item(tag, line, children)`

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| IU-16 | the "Assessors of this unit must…" paragraph is found | `test_assessor_paragraph_is_found` |
| IU-17 | a section without one yields nothing | `test_section_without_an_assessor_paragraph_yields_nothing` |
| IU-18 | the reference is appended to the end of the parent line, in house style | `test_reference_is_appended_to_the_line` |
| IU-19 | child lines follow it, keeping their source indentation | `test_child_lines_keep_their_indentation` |
| IU-20 | the source bullet marker is not duplicated | `test_bullet_marker_is_not_duplicated` |

`inventory(code, md, assessor_ac)` — the whole unit.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| IU-21 | all five sections are emitted, in order, each under its own heading | `test_five_sections_in_order` |
| IU-22 | PC items are tagged `[CODE PC N.N]` | `test_pc_items_carry_their_number` |
| IU-23 | FS items are tagged by skill name, with the name rendered bold | `test_fs_items_are_tagged_by_skill_name` |
| IU-24 | PE / KE / AC items are numbered 1..N in source order | `test_bullet_sections_are_numbered_in_source_order` |
| IU-25 | `--assessor-ac` adds the trailing paragraph as one extra AC item, numbered after the last | `test_assessor_ac_adds_one_numbered_item` |
| IU-26 | without it, the trailing paragraph is not emitted | `test_without_assessor_ac_the_paragraph_is_absent` |
| IU-27 | a section yielding no items raises rather than returning quietly | `test_empty_section_raises` |

IU-27 is the one that protects the gate: the validator builds its expected set by these same rules, so a
silently empty section would shorten the yardstick and let an incomplete consolidation pass.

`main()` — the CLI.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| IU-28 | several units are emitted in order, each under its own `# CODE` heading | `test_units_are_emitted_in_order` |
| IU-29 | a `--unit` that is not `CODE=PATH` is an error — *green on the red run (a raising stub also exits non-zero); **proven non-vacuous by mutation**: removing the argument check turns it red* | `test_malformed_unit_argument_is_an_error` |
| IU-30 | an extraction failure exits 2 | `test_extraction_failure_exits_two` |

### VCI — extraction step 102, `validate_consolidated_items.py`

The Gate 102 → 103 oracle. `consolidated_uoc.md` is the **last point in the run-sheet where the source of
truth is still checkable**: nothing downstream reads the units again. The assessment plan's coverage
rollup, every AT's traceability, the mapping documents and the cluster-coverage capstone all build their
expected item set from this one document. An item lost here does not surface later as a gap — it
surfaces as 100% coverage of a set that is quietly short.

So four things must hold about the item layer, while the gate stays indifferent to the editorial layer
around it (group headings, rationale, assessment ideas — legitimately in no unit):

| | |
|---|---|
| MISSING | every assessable item from every unit is present |
| UNEXPECTED | nothing is present that no unit contains |
| DUPLICATED | each item appears exactly once |
| MISTRANSCRIBED | each item's text is the source's text, under the reference that identifies it |

Cases are behavioural, run through the CLI: that is the shape the gate is actually used in, and it
leaves the internals free to change. Fixtures are unit `.md` and consolidated `.md` written by hand, so
the expectations are independent of the parsers under test.

**Baseline** — the gate must not cry wolf on the editorial layer.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| VCI-01 | a faithful consolidation passes | `test_a_faithful_consolidation_passes` |
| VCI-02 | editorial prose is not treated as items | `test_editorial_prose_is_not_treated_as_items` |
| VCI-03 | backticked example references in the preamble are not occurrences | `test_backticked_example_references_are_not_occurrences` |
| VCI-04 | an editorial bullet citing references is not an item line, even placed before the real items | `test_an_editorial_bullet_citing_references_is_not_an_item` |

**MISSING** — nothing lost.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| VCI-05 | a dropped item is MISSING — parametrised across all five sections, each a different parse path | `test_a_dropped_item_is_missing` |
| VCI-06 | a whole unit left out is MISSING throughout | `test_a_dropped_unit_is_missing_throughout` |
| VCI-07 | the assessor paragraph is required when the flag is set | `test_assessor_paragraph_required_when_the_flag_is_set` |
| VCI-08 | a backticked item reference does not count as present | `test_a_backticked_item_reference_does_not_count_as_present` |
| VCI-09 | an empty consolidation is not a pass | `test_an_empty_consolidation_is_not_a_pass` |

**UNEXPECTED and DUPLICATED** — nothing invented, nothing doubled.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| VCI-10 | a phantom item number is UNEXPECTED | `test_a_phantom_item_number_is_unexpected` |
| VCI-11 | an item from a unit outside the cluster is UNEXPECTED | `test_an_item_from_outside_the_cluster_is_unexpected` |
| VCI-12 | the same item in two groups is DUPLICATED | `test_the_same_item_in_two_groups_is_duplicated` |

**MISTRANSCRIBED** — the item's text is the source's text. Reference presence alone would report a clean
sweep over a document whose items had been rewritten.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| VCI-13 | a reworded item fails | `test_a_reworded_item_fails` |
| VCI-14 | a truncated item fails | `test_a_truncated_item_fails` |
| VCI-15 | dropped sub-bullets fail — the parent kept, its children gone, the item left on a colon | `test_dropped_sub_bullets_fail` |
| VCI-16 | swapped references fail — nothing missing, extra or doubled, only the pairing wrong | `test_swapped_references_fail` |
| VCI-17 | a cosmetic difference in item text passes | `test_a_cosmetic_difference_passes` |

**Grouping invariance** — the judgement layer must not move the verdict.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| VCI-18 | regrouping and reordering the items does not change the verdict | `test_regrouping_does_not_change_the_verdict` |
| VCI-19 | renaming group headings does not change the verdict | `test_renaming_group_headings_does_not_change_the_verdict` |

**Harness.**

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| VCI-20 | every defect class is reported in one run — a human fixes the whole document at once | `test_every_defect_class_is_reported_in_one_run` |
| VCI-21 | a missing consolidated file is an error, not a pass | `test_a_missing_consolidated_file_is_an_error` |
| VCI-22 | a unit with an absent or renamed section is an error naming the section | `test_an_absent_section_is_an_error_naming_it` |
| VCI-23 | assessor-AC off does not expect the trailing paragraph | `test_assessor_ac_off_does_not_expect_the_trailing_paragraph` |
| VCI-24 | a cluster from **any** training package validates, not only ICT / BSB / VU | `test_any_training_package_validates` |
| VCI-25 | a unit path resolves relative to the cluster directory; an absolute path is used as given | `test_unit_paths_resolve_relative_or_absolute` |
| VCI-26 | a malformed `--unit` is an error | `test_a_malformed_unit_argument_is_an_error` |

VCI-22 was **reworded during the port**. The legacy case asserted that changing a heading's *case*
(`# Knowledge Evidence` → `# Knowledge evidence`) was an error, which held because the legacy extractor
matched headings case-sensitively. The ported extractor matches case-insensitively — the convention
`md_table` already used, and what will let an accredited course's ALL-CAPS headings work at all. The
guard's real intent is that **the expected set must never shrink silently**, and a genuinely absent or
renamed section still errors, so the case was widened rather than retired.
