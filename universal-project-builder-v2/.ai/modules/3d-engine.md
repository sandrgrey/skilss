# 3D Experience

Load only for scenes with actual 3D content. Choose the native platform-specific engine (e.g. React Three Fiber for React, Three.js, Babylon.js, native graphics) only when justified. Avoid WebGL for static decorative images.

## Asset pipeline
Confirm permitted GLB/GLTF assets, dimensions, orientations, materials, animations, texture budgets, LODs and fallback preview images. Inspect model bounds to set camera and orbit limits; prevent extreme zoom or invisible objects.

## Interaction contract
- Mouse, touch, keyboard where applicable; orbit/zoom with limits.
- Loading progress, canvas failure fallback, WebGL unsupported/disabled state.
- Accessible product information outside the 3D canvas.
- Responsive camera framing and device pixel ratio cap.
- Suspend rendering when hidden, reuse materials/geometries, dispose scene resources.
- If a CMS uploads GLB, validate content type, filesize, permissions and storage; do not trust filenames.

## 3D with cinematic page
Explicitly define whether scroll controls camera, object, or the overall document; avoid simultaneous contradictory inputs. Provide reduced-motion mode with static frames.

## Quality gates
Verify model orientation, zoom extremes, material colors, interaction latency, memory leaks on scene changes, mobile touch conflict and fallback states.
