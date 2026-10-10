# Four-type proximity workflow

Use this workflow for `ASMC`, `VSMC`, `AF2_A`, and `AF2_V` annotation in cell-segmented lung spatial data with matched cell2location-like abundance factors and registered histology.

## Definitions

- `ASMC`: expression-qualified smooth muscle associated with airway epithelium, supported by proximity to Ciliated and/or Secretory cells.
- `VSMC`: expression-qualified smooth muscle associated with a vessel, supported by proximity to annotated arterial endothelial and venous endothelial cells.
- `AF2_A`: AF2-enriched, fibroblast-qualified cell associated with the airway adventitial compartment; it should be close to both the Ciliated/Secretory epithelial landmark and the ASMC layer.
- `AF2_V`: AF2-enriched, fibroblast-qualified cell associated with vascular adventitia; it should be close to both the combined arterial/venous endothelial landmark and the VSMC layer.

These are inferred spatial identities. Do not imply lineage tracing or direct causal evidence.

## Inputs and audit

Require:

- per-cell or per-bin spatial coordinates;
- expression or inferred abundance factors for ASMC, VSMC, AF2, Ciliated, Secretory, arterial endothelial cells, and venous endothelial cells;
- registered H&E when available, with the coordinate scale or transformation;
- an expression-qualified base SMC pool and fibroblast pool produced using the marker and exclusion framework.

Audit factor names, coordinate units, sample labels, target reference counts, image dimensions, and registration before classifying. Compute anchors and abundance thresholds separately within each sample so condition-wide abundance shifts do not define the labels.

## Landmark anchors

Build two independent anatomical landmark sets:

- airway epithelial anchor score: `Ciliated + Secretory`;
- vascular endothelial anchor score: sum all annotated arterial endothelial and venous endothelial factors. For the current reference use `AEC_1 + AEC_2 + VEC`. Do not include CAP1/CAP2 or other capillary endothelial factors in this anchor.

Select high-specificity anchors within each sample. The VisiumHD implementation used the sample-wise 98th percentile, but this is a tunable starting value, not a universal biological threshold. Confirm that airway anchors trace epithelial-lined airways and vascular anchors trace endothelial vessel structures on H&E.

Calculate physical distances in micrometres when the image metadata permits. Preserve raw distances to both landmark types for every observation.

## SMC classification

First establish a fixed expression-qualified SMC pool using coherent contractile markers and exclusions for pericytes, fibroblasts, and endothelium. Do not use proximity to create new SMCs outside this pool.

For conservative annotation:

- call `ASMC` when airway proximity is sufficiently strong;
- call `VSMC` when vascular proximity is sufficiently strong;
- retain `SMC_unresolved` when neither or both contexts are convincing.

For user-requested complete redistribution:

1. Preserve existing high-confidence ASMC and VSMC calls.
2. For each `SMC_unresolved`, compare distance to the Ciliated/Secretory anchors with distance to the combined arterial/venous endothelial anchors.
3. Assign it to ASMC when the airway distance is smaller or equal; otherwise assign it to VSMC.
4. Verify the invariant:

   `SMC_before = ASMC_before + VSMC_before + SMC_unresolved_before`

   `SMC_after = ASMC_after + VSMC_after`

   `SMC_before == SMC_after`

Report how many unresolved SMCs moved to each subtype. Keep the two landmark distances so borderline assignments remain auditable.

## AF2 classification

Lock an AF2 pool before anatomical subdivision. Require both fibroblast-lineage qualification and AF2 enrichment. The VisiumHD implementation used the top 10% AF2 abundance within each sample as an exploratory threshold.

After the SMC layers are finalized, calculate:

- airway composite distance from each AF2 candidate to airway epithelium and ASMC;
- vascular composite distance from each AF2 candidate to vascular endothelium and VSMC.

A Euclidean composite such as `sqrt(d_landmark^2 + d_SMC^2)` is acceptable when both distances use the same physical unit.

For conservative annotation, require maximum distances to both components and retain `AF2_unresolved` when neither topology is convincing. For user-requested complete redistribution, assign every locked AF2 candidate to the smaller composite distance:

- airway composite smaller or equal -> `AF2_A`;
- vascular composite smaller -> `AF2_V`.

Verify and report:

`AF2_before == AF2_A_after + AF2_V_after`

Do not add AF1 or SCMF to the AF2 pool. Analyze AF1 and SCMF separately; SCMF may represent a contractile/remodeling state and can be unreliable when its reference population is small.

## Validation and outputs

Generate both an H&E overlay and a clean spatial plot with non-target cells in light grey. Visually check:

- ASMC forms bands outside epithelial-lined airway lumens;
- VSMC follows vessel walls and not capillary pericytes or dense inflammatory regions;
- AF2_A lies external to the ASMC layer;
- AF2_V lies external to the VSMC layer.

Return:

- final per-cell label;
- original label and whether redistribution occurred;
- abundance values and thresholds;
- airway, vascular, ASMC, and VSMC distances;
- sample-wise counts before and after redistribution;
- H&E and grey-background spatial plots;
- an explicit limitations statement for mixed segmentation, weak reference classes, remodeling, and broad endothelial signals.

Proximity is an anatomical constraint, not proof of cell identity. When expression and H&E topology disagree, lower confidence and preserve the evidence rather than hiding the discrepancy.
