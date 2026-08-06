Here's the grounded path for this, plus a couple of things I checked live that change the plan.

## Assumptions (stated, since this is single-shot)
- **Transcript**: MANE Select `NM_000546` (TP53), canonical full-length p53 (TAp53).
- **Genome build**: GRCh38 (verified live via NCBI Gene: TP53 = chr17, `NC_000017.11:7,668,421-7,687,490`, **minus strand**).
- **Cas9 variant**: wild-type SpCas9, NGG PAM, 20 nt protospacer.
- **Cloning vector**: lentiCRISPRv2 (BsmBI-based, standard `CACCG-` / `AAAC-` overhangs) — swap to lentiGuide-Puro's overhangs if you're using a separate Cas9 line.
- **Off-target reference**: whole GRCh38, up to 3-4 mismatches, CFD-scored.

## Recommended assembly: one Skill (rung 2), not a hand-built pipeline
This matches an existing curated recipe in the sci-ai-enabler index — **`design-crispr-sgrnas-for-a-gene-knockout`**, built on the **sgRNA Design** Claude Skill.

- **Evidence**: Reported (tiered assembly itself isn't benchmarked, but its scoring models are field-standard: Rule Set 2/Azimuth for on-target, Doench et al. *Nat Biotechnol* 2016; CFD for off-target).
- **Availability**: Fully open, no account/API key.
- **Compute**: Laptop — seconds to minutes, CPU only.

**Why not rung 1 (just asking me directly)**: I tried exactly that as a sanity check before answering — I pulled a "validated" TP53 guide sequence from an unmoderated web search summary, then went to verify it against a primary vendor database (GenScript's TP53 gRNA page). That page returned **zero** validated CRISPRko guides for TP53 (only unrelated CRISPRa/SAM-activation guides). That's a concrete demonstration of why hand-picking or trusting a search snippet is the "eyeballing" failure mode you're trying to avoid — on-target scoring (Rule Set 2) and genome-wide CFD off-target search need the actual trained model and a real genome-wide search, not a model recalling a sequence from memory. I'm not going to hand you a table of guides with invented scores.

## What the skill does (Tier 1 → Tier 3 preference order)
1. **Tier 1**: checks Addgene-hosted, experimentally validated knockout libraries for TP53 coverage.
2. **Tier 2**: falls back to CRISPick (Broad GPP) pre-computed picks for GRCh38.
3. **Tier 3**: only if neither covers it, designs de novo with Rule Set 2/Azimuth (on-target) + CFD (off-target).
4. Writes `guides.csv` (sequence, PAM, target_exon, strand, on_target_score, off_target_assessment, source_tier) and `provenance.json` (genome build, skill version, source DB versions) — this is your citable, order-ready record.
5. Sanity-checks exon placement and flags anything to remove before ordering — no manual score editing.

## One important TP53-specific correction before you run it
"Early constitutive exon" is the right general heuristic, but for **TP53 specifically it's not quite the safe default**: TP53 has N-terminally truncated isoforms (Δ133p53, Δ160p53) transcribed from an internal promoter in intron 4, so they **lack exons 1-4 entirely**. A guide in exon 2-4 knocks out full-length TAp53 only — it will not touch those shorter isoforms, which have documented distinct (sometimes opposing) biological activity. If you want a knockout of *all* major TP53 isoforms, target the DNA-binding domain region (roughly exons 5-8), which is shared by every isoform; if you specifically want to ablate full-length TAp53 while leaving Δ133/Δ160 intact, exons 2-4 are correct as stated. Tell the skill explicitly which one you mean.

## Run it
```
/plugin install sciagent-skills
```
Then, in the same session:
```
Design CRISPR-Cas9 knockout guides for human TP53, MANE Select transcript NM_000546, GRCh38,
SpCas9 (NGG PAM), lentiCRISPRv2 cloning (BsmBI overhangs). Target [exons 2-4 for full-length
TAp53-only knockout | exons 5-8 for a knockout hitting all major isoforms — pick one]. Exclude
the terminal exon and alternatively-spliced regions. Prefer Addgene/CRISPick-validated guides
over de novo; report CFD off-target hits in coding exons of other genes. Output guides.csv +
provenance.json, top 3-5 ranked.
```
That gives you real Rule Set 2 scores, real CFD off-target loci, and real validated-guide cross-referencing — the exact record you need for a methods citation and for ordering oligos with confidence.

## Methods-section template (fill in from your `provenance.json` + `guides.csv` once run)
> sgRNAs targeting TP53 (NM_000546, GRCh38) were designed using the sgRNA Design Claude Skill (SciAgent-Skills, v[X]), which prioritizes experimentally validated guides (Addgene knockout libraries) and Broad GPP CRISPick pre-computed picks, falling back to de novo design scored by Rule Set 2/Azimuth (Doench et al., *Nat Biotechnol* 2016) for on-target activity and CFD for off-target risk. Guides were required to fall within [exon 2-4 / exon 5-8] of the canonical CDS, upstream of alternatively-spliced/terminal exons, with NGG PAMs for SpCas9. The top-ranked guide, [sequence], had an on-target score of [X] and no CFD-scored off-target site >[threshold] in a coding exon of another gene. Oligos were synthesized with BsmBI-compatible overhangs for cloning into lentiCRISPRv2.

Since nothing here was actually executed (the skill isn't installed in this sandbox and I have no way to install it for you), I'm not filing this as a composition-report — there's a matching recipe already, so there's no knowledge-base gap to report either.