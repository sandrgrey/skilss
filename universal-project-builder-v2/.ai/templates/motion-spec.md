# Motion specification template

- SCENE_ID: TODO
- REFERENCE_EVIDENCE: TODO (file/page/frame/link or 'original design')
- TRIGGER: scroll / clock / gesture / state
- PROGRESS_RANGE: [0,1]
- STAGE_MODE: FLUID / FIXED_STAGE / HYBRID
- STAGE_W / STAGE_H: N/A (unless fixed stage)
- SCALE_POLICY: N/A / width_lock / contain / cover
- DURATION_OR_SCROLL_LENGTH: TODO
- PHASES: [ {id, start, end, easing, visual_effect} ]
- LAYERS: [ {id, source_asset, start_state, end_state, z_index} ]
- VIDEO_SEAMS: [ {from, to, progress, crossfade_half_width, verified_frames} ]
- MOBILE_BEHAVIOR: TODO
- REDUCED_MOTION: TODO
- FAILURE_FALLBACK: TODO
- VALIDATION_FRAMES: 0, 0.25, 0.50, 0.75, 1.00 (adjust to important events)

## Acceptance notes
At each validation frame: inspect typography, safe zones, overlap, contrast, correspondence to source and reverse-scroll behavior.
