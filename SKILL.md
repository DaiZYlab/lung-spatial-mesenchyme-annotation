---
name: lung-spatial-mesenchyme-annotation
description: Annotate airway versus vascular smooth muscle cells and airway versus vascular adventitial fibroblasts in lung spatial transcriptomics. Use for Visium HD, cell-segmented spatial data, cell2location outputs, or matched lung scRNA-seq references; not for generic lung cell typing without an airway-versus-vessel question.
---

# Lung Spatial Mesenchyme Annotation

Produce four target annotations with an explicit confidence score:

- airway smooth muscle cell (ASMC)
- vascular smooth muscle cell (VSMC)
- airway-associated AF2/adventitial fibroblast (AF2_A)
- vascular-associated AF2/adventitial fibroblast (AF2_V)

Do not infer anatomical identity from one marker. Airway and vascular mesenchymal cells share strong contractile or ECM programs, and disease can blur them.

## Required evidence model

Use two independent axes:

1. **Lineage/state evidence** from expression: contractile SMC versus fibroblast, excluding pericyte, endothelial, epithelial, immune, mesothelial, and activated myofibroblast alternatives.
2. **Anatomical evidence** from spatial context: proximity and topology relative to a confidently identified bronchial epithelium or vascular endothelial lumen.

Assign a four-way label only when both axes agree. If spatial anatomy is unavailable, report `SMC_unresolved` or `AdvF_unresolved`; expression alone is insufficient for airway-versus-vascular naming.

Read [references/marker-framework.md](references/marker-framework.md) before selecting markers or interpreting scores. Adapt gene symbols to species and verify that positive and exclusion genes are detected in the assay.

For the finalized four-type proximity workflow, including fixed-pool invariants and redistribution rules, read [references/four-type-proximity-workflow.md](references/four-type-proximity-workflow.md).

## Workflow

1. Audit the reference and spatial object before modeling. Record species, platform, segmentation unit, sample/condition, gene count, target-label counts, available images, spatial coordinates, and existing abundance scores. `scripts/audit_h5ad.py` provides a lightweight H5AD audit without loading the full matrix.
2. Establish structural landmarks independently of the four target labels:
   - airway: continuous epithelial structure supported by basal/ciliated/secretory markers and visible lumen or histology;
   - vessel: endothelial ring/track supported by arterial and/or venous endothelial annotations and visible lumen or histology. Do not use capillary endothelium as the default VSMC or vascular-adventitial anchor.
3. Establish lineage scores using multi-gene positive modules plus exclusion modules. Avoid using ACTA2 alone for SMC or COL1A1 alone for fibroblast.
4. Learn expression signatures only from adequately represented, biologically verified reference cells. Use donor/sample-aware validation. Do not treat labels with very small reference counts as validated training classes.
5. Combine expression and anatomy. Prefer continuous distance-to-landmark and neighborhood composition over nearest-cell identity alone. For vessels, distinguish mural layers from capillary pericytes; for airways, distinguish smooth muscle from myofibroblast/fibromyocyte programs.
6. Report per-cell or per-bin fields for lineage score, airway-context score, vascular-context score, exclusion score, final label, confidence tier, and reason. Preserve raw scores.
7. Validate against held-out samples and selected histological regions. Include confusion between ASMC/VSMC, Airway-AdvF/Vascular-AdvF, SMC/pericyte, and fibroblast/myofibroblast. Use spatial overlays and marker plots, not only UMAP separation.

## Confidence tiers

- `high`: coherent lineage module, clear anatomical topology, exclusion tests passed, and agreement across methods or replicates.
- `moderate`: coherent lineage plus plausible spatial context, but incomplete landmark or weak subtype signature.
- `low/unresolved`: conflicting expression and anatomy, mixed spot/cell, low counts, injury-state ambiguity, or absent landmark.

Default to unresolved labels when anatomy is inadequate. If the user explicitly requests complete redistribution, first lock the expression-qualified lineage pool, assign unresolved members by relative proximity, and prove that the before/after lineage totals are identical.

## Deliverables

Return an annotated object plus:

- a table defining every score and threshold;
- target/reference cell counts by sample and condition;
- spatial maps with airway and vascular landmarks overlaid;
- marker and exclusion-gene plots;
- validation metrics and an error/ambiguity table;
- a concise statement separating expression-based inference from anatomically validated identity.
