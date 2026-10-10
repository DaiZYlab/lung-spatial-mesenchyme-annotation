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

Before re-annotation, define and lock the candidate universe. Do not silently mix these two modes:

- **Original dominant target pool:** use only observations whose highest cell2location factor across all reference types is ASMC, VSMC, or AF2. Only original ASMC/VSMC may become ASMC/VSMC, and only original AF2 may become AF2_A/AF2_V. This is the default when the user asks to use the original ASMC, VSMC, and AF2 annotations.
- **Expression-qualified pool:** construct broader SMC and fibroblast pools from abundance, expression, and exclusions. This mode may contain unresolved cells and must be named separately.

Never compare counts from one candidate-universe definition with labels from the other without explaining the denominator change. A cell2location factor is continuous; calling its maximum a discrete original annotation is a deliberate rule, not an intrinsic property of the H5AD.

Read [references/marker-framework.md](references/marker-framework.md) before selecting markers or interpreting scores. Adapt gene symbols to species and verify that positive and exclusion genes are detected in the assay.

For the finalized four-type proximity workflow, including fixed-pool invariants and redistribution rules, read [references/four-type-proximity-workflow.md](references/four-type-proximity-workflow.md).

## Workflow

1. Audit the reference and spatial object before modeling. Record species, platform, segmentation unit, sample/condition, gene count, target-label counts, available images, spatial coordinates, and existing abundance scores. `scripts/audit_h5ad.py` provides a lightweight H5AD audit without loading the full matrix.
2. Establish structural landmarks independently of the four target labels:
   - airway: continuous epithelial structure supported by basal/ciliated/secretory markers and visible lumen or histology;
   - vessel: endothelial ring/track supported by arterial and/or venous endothelial annotations and visible lumen or histology. Do not use capillary endothelium as the default VSMC or vascular-adventitial anchor.
3. Lock the requested candidate universe before applying anatomical rules. For original-pool mode, compute the dominant factor across the complete reference panel, not only among ASMC/VSMC/AF2.
4. Establish lineage scores using multi-gene positive modules plus exclusion modules. Avoid using ACTA2 alone for SMC or COL1A1 alone for fibroblast.
5. Learn expression signatures only from adequately represented, biologically verified reference cells. Use donor/sample-aware validation. Do not treat labels with very small reference counts as validated training classes.
6. Combine expression and anatomy. Prefer continuous distance-to-landmark and neighborhood composition over nearest-cell identity alone. For vessels, distinguish mural layers from capillary pericytes; for airways, distinguish smooth muscle from myofibroblast/fibromyocyte programs.
7. Report per-cell or per-bin fields for original dominant label, candidate-pool membership, lineage score, airway-context score, vascular-context score, exclusion score, final label, confidence tier, and reason. Preserve raw scores and distances.
8. Validate against held-out samples and selected histological regions. Include confusion between ASMC/VSMC, Airway-AdvF/Vascular-AdvF, SMC/pericyte, and fibroblast/myofibroblast. Use spatial overlays and marker plots, not only UMAP separation.

## Confidence tiers

- `high`: coherent lineage module, clear anatomical topology, exclusion tests passed, and agreement across methods or replicates.
- `moderate`: coherent lineage plus plausible spatial context, but incomplete landmark or weak subtype signature.
- `low/unresolved`: conflicting expression and anatomy, mixed spot/cell, low counts, injury-state ambiguity, or absent landmark.

Default to unresolved labels when anatomy is inadequate. If the user explicitly requests complete redistribution, first lock the expression-qualified lineage pool, assign unresolved members by relative proximity, and prove that the before/after lineage totals are identical.

In original dominant target-pool mode, every eligible observation must receive a final subtype unless the user requests a conservative unresolved category. Prove both invariants per sample and overall:

- `original_ASMC + original_VSMC == final_ASMC + final_VSMC`
- `original_AF2 == final_AF2_A + final_AF2_V`

## Deliverables

Return an annotated object plus:

- a table defining every score and threshold;
- target/reference cell counts by sample and condition;
- spatial maps with airway and vascular landmarks overlaid;
- marker and exclusion-gene plots;
- validation metrics and an error/ambiguity table;
- a concise statement separating expression-based inference from anatomically validated identity.
