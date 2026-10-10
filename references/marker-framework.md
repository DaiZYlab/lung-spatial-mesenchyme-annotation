# Marker and anatomy framework

Markers are candidate modules, not single-gene definitions. Re-estimate specificity in the matched reference and spatial assay.

## Contractile smooth muscle lineage

Positive core: `ACTA2/Acta2`, `TAGLN/Tagln`, `MYH11/Myh11`, `CNN1/Cnn1`, `ACTG2/Actg2`, `MYLK/Mylk`, `LMOD1/Lmod1`, `DES/Des`, `TPM2/Tpm2`, `MYL9/Myl9`.

Exclude or penalize:

- pericyte-like: `RGS5`, `CSPG4`, `MCAM`, `KCNJ8`, `ABCC9`, `PDGFRB`, `COX4I2`, `NDUFA4L2`, `HIGD1B`;
- fibroblast/ECM-dominant without mature contractile coherence: `DCN`, `LUM`, `COL1A1`, `COL1A2`, `COL3A1`, `PDGFRA`;
- endothelial: `PECAM1`, `VWF`, `EMCN`, `KDR`, `CLDN5`.

Candidate airway-enriched evidence includes `HHIP/Hhip`, `MYLK/Mylk`, `IGF1/Igf1`, and coherent proximity around a bronchial epithelial boundary. Candidate vascular-enriched evidence includes `NTRK3/Ntrk3`, `MEF2C/Mef2c` and a circumferential mural relationship to a vascular endothelial structure. These subtype genes are context-, species-, age-, and disease-dependent; anatomy carries substantial weight.

## Adventitial fibroblast lineage

Positive core: `COL1A1/Col1a1`, `COL1A2/Col1a2`, `COL3A1/Col3a1`, `DCN/Dcn`, `LUM/Lum`, `PDGFRA/Pdgfra`, with an adventitial module such as `PI16/Pi16`, `SERPINF1/Serpinf1`, `SFRP2/Sfrp2`, `MFAP5/Mfap5`, `FBLN1/Fbln1`, `CD34/Cd34`, `IGFBP4/Igfbp4`, or `PDGFRL/Pdgfrl` when detected.

Exclude or penalize mature contractile SMC, pericyte, endothelial, epithelial, immune, and mesothelial programs. Treat `POSTN`, `CTHRC1`, strong `ACTA2`, or other injury-associated myofibroblast signals as state annotations unless lineage and anatomy resolve them.

Airway-AdvF and Vascular-AdvF often do not have universally separable expression programs. Require topology:

- Airway-AdvF: fibroblast/adventitial identity in the outer connective-tissue layer of a bronchial structure, outside epithelium and smooth muscle.
- Vascular-AdvF: fibroblast/adventitial identity external to the vascular smooth-muscle layer surrounding an endothelial vessel.

Do not call any generic `PI16+` or `SERPINF1+` fibroblast vascular solely because those genes are established adventitial markers; lung adventitial fibroblasts can occur near both vessels and airways.

## Landmark modules

Airway epithelium can be supported by combinations of basal (`KRT5`, `KRT14`, `KRT17`, `TP63`), ciliated (`FOXJ1`, `PIFO`, `TPPP3`), and secretory (`SCGB1A1`, `SCGB3A1`, `MUC5B`) programs. Use morphology and species-appropriate markers.

Use annotated arterial endothelial cells and venous endothelial cells as the vascular anchors for VSMC and vascular adventitia. In the current reference, combine all available arterial endothelial sublabels (`AEC_1` and `AEC_2`) with `VEC`; if another dataset uses different names, map them explicitly rather than assuming the same labels. Generic endothelial genes such as `PECAM1`, `VWF`, `KDR`, and `CLDN5` can support the landmark, but capillary endothelium is not the default anchor. Capillary endothelium plus `RGS5+` mural cells should raise a pericyte alternative rather than automatically imply VSMC.

## Current VisiumHD project caveats

The inspected mouse reference uses `ASMC`, `VSMC`, `AF1`, `AF2`, and `SCMF`. It contains only 14 ASMC and 77 VSMC reference cells, versus 777 AF1 and 134 AF2 cells. Therefore:

- treat the present ASMC model signature as exploratory until expanded or externally validated;
- do not rename AF1/AF2 as airway or vascular adventitial fibroblasts without anatomical validation;
- use the existing cell2location abundances as lineage evidence, not as proof of the four requested anatomical identities;
- validate condition robustness separately in WT and CKO because remodeling may alter marker expression and geometry.

## Evidence basis

- Travaglini et al., *Nature* (2020), human lung atlas: adventitial fibroblasts marked by SFRP2, PI16, and SERPINF1 localized near vascular adventitia and airways; contractile stromal populations overlap transcriptionally.
- Danopoulos et al., *European Respiratory Journal* (2020), developing human lung: airway-enriched HHIP/MYLK/IGF1 and vascular-enriched NTRK3/MEF2C smooth-muscle programs with spatial validation.
- Madissoon et al., *Nature Genetics* (2023), spatially resolved human lung atlas: regional anatomy is integral to resolving lung cell identities.
