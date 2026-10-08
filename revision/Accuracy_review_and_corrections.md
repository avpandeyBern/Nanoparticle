# Accuracy review and suggested corrections

Manuscript: *Critical review of direct comparisons, exposure, tumor control and reporting bias*

---

## 1. Arithmetic audit

Every derived ratio and percentage in the manuscript was recomputed from the group means the text itself reports. **All of them check out.**

| Statement in text | Recomputed | Verdict |
|---|---|---|
| nano-EGCG / free EGCG = 0.828; 17.2% lower | 707 / 854 = 0.8279 | correct |
| chitosan-EGCG ratios 0.603 and 0.420 | 310 / 514; 216 / 514 | correct |
| untargeted and targeted EGCG 0.649 and 0.566 | 1230 / 1895; 1073 / 1895 | correct |
| targeted / untargeted 0.872 | 1073 / 1230 | correct |
| catechin nanoemulsion 0.717 and 0.475 | (100−48.3)/(100−27.9); (100−77.5)/(100−52.6) | correct |
| A15 liposome ratios 0.753 and 0.332 | 275 / 365; 121 / 365 | correct |
| lipid carrier ratio 0.674 | 778.4 / 1155.1 | correct |
| tumor AUC ratio 4.22 | 4356.3 / 1032.3 | correct |
| lnRR sampling variance formula | standard delta-method form | correct |

No numerical errors were found. The quantitative section is sound.

---

## 2. Corrections applied in the revised file

These are small and unambiguous, so they are already in `Nanoparticle_review_revised.docx`.

1. **Logical inversion in the pharmacokinetics section.** "For oral products, absolute bioavailability requires a suitable intravenous reference; a higher oral AUC alone establishes relative exposure" read as an endorsement of the inference the sentence is warning against. Changed to "**establishes only relative exposure**."
2. **Compound-adjective hyphenation in three headings.** "dose sparing evidence" → "dose-sparing evidence"; "formulation dependent gains" → "formulation-dependent gains".
3. **Missing commas in one heading.** "Quercetin resveratrol and other natural products broaden the evidence but not uniformly" → "Quercetin, resveratrol and other natural products broaden the evidence, but not uniformly".

---

## 3. Corrections recommended, not applied

These need an author decision, so the revised file leaves them alone.

1. **The manuscript has no main title.** The file opens directly with what reads as a subtitle. Add a title above it, for example: *Nanoparticle delivery of natural products in prostate cancer*.
2. **No included-study count is given.** The methods state that 314 records were retrieved and that "the search count is not an included-study count", but never report how many studies entered each evidence category. Add one sentence giving the number of matched single-compound experiments, unequal-dose studies, combination studies, pharmacokinetic studies and cell-only studies. Reviewers will ask for this.
3. **No declarations.** The manuscript carries no funding statement, competing-interests statement, author contributions, or data-availability statement. The methods refer to "the accompanying evidence package", which should be named and deposited with a persistent identifier in a data-availability statement.
4. **An unsupported group size appeared in the old Figure 2C legend.** It stated n = 12 per group for the targeted-EGCG study, a number that appears nowhere in the text and is not among the values the text says were recovered. It has been removed from the new legend. If the source does report it, add it to the body text as well.
5. **The blank-liposome arm was missing from the old Figure 3A.** The text reports 659 ± 136 mm³ for blank liposomes, but the figure omitted it. The new Figure 3A includes it, which also makes the carrier-only control visible, a point the manuscript argues for elsewhere.
6. **Catechin ratios are tumor-weight ratios.** The ratios 0.717 and 0.475 derive from tumor weight, while every other ratio in the manuscript derives from tumor volume. The new Figure 5C legend says so. Consider adding the same clarifier where these values first appear in the text.
7. **Gene nomenclature.** *Pten* should be italicised throughout when it denotes the mouse gene, and the distinction from human *PTEN* kept consistent.
8. **Reference 35.** The isotope in the title is set as "198gold"; it should be "¹⁹⁸Au" or "198Au" with the mass number superscripted, if the journal permits editing a quoted title.

---

## 4. Items to verify against the primary sources

These could not be checked from this environment, and none is asserted to be wrong. They are the statements most exposed if a reviewer checks them.

- The 2009 EGCG doses of 100 µg and 1 mg per mouse, and the day-45 means of 1,242, 854 and 707 mm³.
- Whether the error bars in that source are s.e.m. or s.d., since the manuscript elsewhere makes the s.d./s.e.m. distinction a central reporting point.
- The 2026 references 20 and 21: volume, article number, DOI and PMID. Recently indexed records change, and both are cited for specific numerical values.
- The De Velasco dietary doses of 76 and 380 mg/kg/day.
- Reference 18, described in the text as "the 2015 polycaprolactone study". The formulation in that report is a polymer blend, so "polycaprolactone-based" may be the safer description.

---

## 5. Figure changes

All six figures were redrawn. Panel order, panel lettering and the scientific content of each panel are unchanged, so every in-text callout to Figures 1 to 6 still resolves correctly.

- **No titles and no citation numbers appear anywhere inside the artwork.** All provenance, dosing detail and caveats were moved into the legends, which have been rewritten accordingly.
- A six-colour categorical palette was validated for deuteranopia, protanopia and tritanopia separation and for lightness and chroma against a white surface. Every encoding carries a second channel, either a direct label, a glyph or a position, so no distinction rests on colour alone.
- Colour roles are consistent across all six figures: grey for control, orange for free compound, blue for untargeted nanoparticle, violet for targeted nanoparticle, teal for lipid carrier.
- Text in the figures follows the manuscript's US spelling.
- Each figure is supplied as a 7.0-inch-wide PNG at 600 dpi for submission systems and as a vector PDF with embedded Type 42 fonts for production. Editable Python sources are included so panels can be adjusted without redrawing.
