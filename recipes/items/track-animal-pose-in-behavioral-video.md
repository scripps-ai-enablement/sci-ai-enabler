---
title: Track animal pose in behavioral video
parent: All recipes
grand_parent: Recipes
nav_order: 27
problem_class: Data analysis
subject_areas: [Neuroscience]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Workstation with GPU
last_verified: 2026-08-02
summary: Use the DeepLabCut skill in Claude Code to go from behavioral video to a filtered, quality-controlled keypoint table with kinematics and provenance recorded.
---

# Track animal pose in behavioral video

Hand Claude Code a folder of behavioral videos; get back a committed pose-estimation pipeline that produces per-frame keypoint coordinates, an explicit low-confidence mask, derived kinematics, and a record of which model produced them.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Neuroscience |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Workstation with GPU |

## Problem

Behavioral neuroscience runs on video, and almost every downstream question — reach kinematics, gait, freezing, social approach, aligning neural activity to movement onset — starts by turning pixels into keypoint coordinates. DeepLabCut is the standard way to do that, but the pipeline has nine stages and each one hides a choice that quietly determines whether the output is usable: how many frames you label and how diverse they are, which backbone, when to stop training, what likelihood cutoff separates a real detection from a hallucinated one, and whether the tracked points survive occlusion.

The failure mode is not a crash. It is a `.csv` full of confidently-wrong coordinates that nobody notices until a velocity trace has spikes in it. The training-set-diversity effect is measured: for 2D sagittal gait, models trained on 25% of participants gave good adult joint angles but failed on clinical parameters and on toddlers, while 75%-participant models reached good-to-excellent absolute agreement against a Vicon reference — same algorithm, same landmarks, different training coverage ([Verhoeven et al., *J. Biomech.* 2025](https://doi.org/10.1016/j.jbiomech.2025.112708)). "Solved" means: a versioned script that produces the keypoint table, an explicit record of the model and its test error, and low-confidence frames flagged rather than silently interpolated.

## Recommended approach

1. **Install the [DeepLabCut skill](../../catalog/tools/deeplabcut.html)** in Claude Code, and install DeepLabCut itself into the project environment (the skill drives your Python; it does not vendor the package). PyTorch must be matched to your CUDA version — see the catalog page for both install paths.

2. **Try SuperAnimal zero-shot before you label anything.** For standard mouse/rat top-view or side-view arenas and many other species, the pretrained models often need no labels at all. Ask for a throwaway probe first:

   ```
   Using the deeplabcut skill, run SuperAnimal zero-shot inference on
   data/videos/session01.mp4 (top-view mouse in an open field, 30 fps).
   Use the recommended scale list [200, 300, 400]. Save a labeled preview
   video of 30 s from the middle of the session so I can eyeball it.
   Do not create a training project yet.
   ```

   Watch the preview. If the keypoints track cleanly through the behaviors you care about, skip steps 3–4 entirely — this is the cheap path, and fine-tuning from SuperAnimal is 10–100× more data-efficient than transfer learning from scratch if you do end up needing it.

3. **If zero-shot is not good enough, label for diversity, not for volume.** Have the assistant create the project and extract frames by k-means clustering (the skill's default) so the labeled set spans the behavioral range rather than 200 near-identical frames from one bout. Explicitly cover every animal, every lighting condition, and every camera position you intend to run inference on — that is what the Verhoeven result is about.

4. **Train, then read the test error before you touch the full dataset.** Ask for evaluation on the held-out test set and a per-keypoint error in *pixels and in physical units* (you need a scale factor: a ruler frame or known arena dimension). A test error that is a large fraction of the movement amplitude you plan to measure means the model is not ready, regardless of how the preview video looked.

5. **Have the assistant write a versioned inference-and-QC script, not an interactive session.** A minimal prompt:

   ```
   Using the deeplabcut skill, write me a script run_pose.py that:
   - runs inference over every mp4 in data/videos/ with the model in
     <project>/dlc-models/, writing per-video HDF5 + CSV
   - loads each result into a tidy DataFrame (frame, bodypart, x, y, likelihood)
   - masks coordinates with likelihood below a LIKELIHOOD_CUTOFF constant
     defined at the top of the file (do NOT interpolate over the mask —
     emit NaN and a per-bodypart masked-frame count)
   - converts pixels to mm using a PIXELS_PER_MM constant
   - computes per-bodypart speed with a stated smoothing window, and writes
     out/kinematics.csv plus out/pose_qc.csv (per video, per bodypart:
     median likelihood, % frames masked, longest masked run)
   Surface every threshold as a named constant with a comment. No silent defaults.
   ```

   The `pose_qc.csv` is the part people skip. A bodypart with 30% masked frames or a 400-frame masked run is an occlusion or a camera problem, not data.

6. **Pin the environment and record provenance.** Emit a `requirements.txt` pinning `deeplabcut`, the PyTorch build, `pandas`, `numpy`, `scipy`, and have the script write `out/provenance.json`: DeepLabCut version, torch + CUDA version, backbone and whether SuperAnimal (and which one) or a fine-tuned model was used, the model snapshot/iteration, the training-set fraction, the reported test error, `PIXELS_PER_MM`, `LIKELIHOOD_CUTOFF`, the `sha256` of each input video, run date, and the model/agent identity. Model weights are large — commit the config and the provenance record, and archive the snapshot separately with its hash. See the [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.md) guide.

The durable artifact is `run_pose.py` + the pinned environment + the DeepLabCut project `config.yaml` + `kinematics.csv`, `pose_qc.csv` and `provenance.json`, all under version control.

## Why this assembly

Rung 2. DeepLabCut has a large API surface and a stage ordering that is easy to get wrong; the skill supplies the correct call sequence and the defaults (k-means frame extraction, backbone choices, SuperAnimal scale list, multi-animal detector) so the model does not reinvent them each session. What plain Claude Code tends to miss without it is the zero-shot-first ordering — it will happily start a labeling project when SuperAnimal would have worked.

No escalation is warranted. This is one tool with one input type and a human looking at a preview video in the middle; a multi-tool harness adds nothing, and no autonomous system targets pose estimation.

## Availability

Fully open. The DeepLabCut skill is community OSS (MIT, part of the Awesome Cognitive and Neuroscience Skills collection); DeepLabCut itself is LGPL-3.0 and separately installed. No subscription, no institutional gate, no data leaves the machine — relevant if your videos contain identifiable humans, which is the common case in clinical gait and infant-movement work.

**Verify the skill's numbers before running an experiment.** The collection's skills are AI-generated and not individually expert-reviewed; the catalog page flags this. Treat the stated `maxiters`, batch sizes and scale lists as starting points and check them against the [DeepLabCut documentation](https://deeplabcut.github.io/DeepLabCut/).

## Compute requirements

Workstation with GPU. Training is the binding constraint: the skill's default 100,000 iterations on a ResNet-50 is hours on a modern GPU and impractical on CPU — drop batch size to 4 or 2 when VRAM is tight (8 GB is workable, 16 GB+ comfortable). Inference is far cheaper and roughly real-time-to-several-times-real-time per video on the same GPU, so the per-session cost after training is small.

The SuperAnimal zero-shot path in step 2 skips training entirely, which is most of the reason to try it first — a laptop with a modest GPU can do inference-only work, though CPU-only inference on long sessions is slow. Budget disk for the labeled dataset, the model snapshots, and the labeled preview videos; H.264 `.mp4` or AVI are the recommended input containers.

## Evidence

Proposed. No documented attempt at driving DeepLabCut through the Claude skill on a real behavioral dataset is known — the assembly is `Proposed`, and the skill's own text is AI-generated. The *components* are well validated:

- **SuperAnimal** — unified pretrained models covering over 45 species with no additional manual labels, "excellent performance across six pose estimation benchmarks", and 10–100× better data efficiency than prior transfer-learning approaches when fine-tuned ([Ye et al., *Nat. Commun.* 2024](https://doi.org/10.1038/s41467-024-48792-2)). This is the basis for the zero-shot-first ordering in step 2.
- **Accuracy against reference systems** — against 3D X-ray radiography (XROMM) with subcutaneous markers in foraging marmosets, DeepLabCut trajectories (triangulated via Anipose, 11 markers) had a median error of 0.228 cm, 2.0% of the range of motion ([Moore et al., *J. Exp. Biol.* 2022](https://doi.org/10.1242/jeb.243998)). Against a Fastrak electromagnetic reference, agreement was in the millimeter range ([Kosourikhina et al., *PLOS ONE* 2022](https://doi.org/10.1371/journal.pone.0276258)).
- **Training-set coverage dominates** — the 25%-vs-75% participant comparison against Vicon, where the sparser model held up for adult joint angles but not for clinical parameters or for toddlers, and treadmill walking validated better than overground ([Verhoeven et al., *J. Biomech.* 2025](https://doi.org/10.1016/j.jbiomech.2025.112708)). This is the direct evidence for step 3.

## Alternatives considered

- **Lightning Pose instead of DeepLabCut.** On a 24-landmark infant general-movements task with near-identical training sets, Lightning Pose identified body parts at 99.75% versus DeepLabCut's 97.80% over 3,200+ unseen frames ([Kaur et al., *EMBC* 2024](https://doi.org/10.1109/EMBC53108.2024.10781538)). If your accuracy budget is that tight, it is worth evaluating — but it is not in `catalog/tools/`, so it is not a recipe you can follow here.
- **Plain Claude Code + the DeepLabCut API.** Reasonable if you already run DLC weekly and know the stage ordering. The skill mainly buys you the zero-shot-first discipline and the parameter defaults in one place.
- **The DeepLabCut GUI, no agent.** The right call for the labeling step itself — keypoint annotation is inherently interactive, and this recipe does not try to automate it. Use the agent for the surrounding pipeline: inference, masking, QC tables, kinematics, provenance.
- **A pose-free behavioral readout** (frame-differencing for freezing, centroid tracking for locomotion). Much cheaper, no GPU, no labeling. If your measure is "did it move" rather than "how did each limb move", do that instead.

## See also

- [DeepLabCut (Claude Skill)](../../catalog/tools/deeplabcut.html)
- [Localize an implant tip to a brain atlas subregion](localize-implant-tip-in-brain-atlas-subregion.html) — the histological counterpart for the same rodent experiment.
- [Sort spikes from a Neuropixels recording](sort-spikes-from-neuropixels-recording.html) — the neural side to align these kinematics against.
- [Extract event-related potentials from EEG epochs](extract-event-related-potentials-from-eeg.html) — the analogous single-skill, provenance-first signal-processing recipe.

## Sources

- [DeepLabCut skill — `awesome_cognitive_and_neuroscience_skills/skills/deeplabcut/SKILL.md`](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills/blob/master/skills/deeplabcut/SKILL.md) — catalog `last_verified` 2026-08-02.
- [Ye et al., *Nat. Commun.* (2024), doi:10.1038/s41467-024-48792-2](https://doi.org/10.1038/s41467-024-48792-2) — SuperAnimal pretrained pose estimation models; verified 2026-08-02 (this run).
- [Verhoeven et al., *J. Biomech.* (2025), doi:10.1016/j.jbiomech.2025.112708](https://doi.org/10.1016/j.jbiomech.2025.112708) — DeepLabCut validity vs Vicon in adults and toddlers; verified 2026-08-02 (this run).
- [Moore et al., *J. Exp. Biol.* (2022), doi:10.1242/jeb.243998](https://doi.org/10.1242/jeb.243998) — validation against 3D X-ray radiography.
- [Kosourikhina et al., *PLOS ONE* (2022), doi:10.1371/journal.pone.0276258](https://doi.org/10.1371/journal.pone.0276258) — validation of markerless 3D pose estimation.
- [Kaur et al., *EMBC* (2024), doi:10.1109/EMBC53108.2024.10781538](https://doi.org/10.1109/EMBC53108.2024.10781538) — Lightning Pose vs DeepLabCut head-to-head.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=track-animal-pose-in-behavioral-video&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Ftrack-animal-pose-in-behavioral-video.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
