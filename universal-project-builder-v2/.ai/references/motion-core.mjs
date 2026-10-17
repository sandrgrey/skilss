/** Framework-independent animation primitives inspired by Marlin's scroll.ts.
 * Original site's numeric preset is intentionally kept in marlin-timeline.json.
 * This helper is for reuse in *new* projects; it is not a byte-identical copy.
 */

/** Clamp finite x to a finite, ordered inclusive range. */
export function clamp(x, min = 0, max = 1) {
  if (![x, min, max].every(Number.isFinite) || min > max) {
    throw new RangeError('Expected finite x/min/max and min <= max');
  }
  return Math.max(min, Math.min(x, max));
}

/** Linear interpolation; t may be outside 0...1 if extrapolation is desired. */
export function lerp(start, end, t) {
  if (![start, end, t].every(Number.isFinite)) throw new TypeError('Finite inputs required');
  return start + (end - start) * t;
}

/** Normalized linear phase. Safe for p outside window; window must be ascending. */
export function ramp(p, [start, end]) {
  assertWindow(p, start, end);
  return clamp((p - start) / (end - start));
}

/** Cubic ease-out phase identical in formula to Water.pdf `span`. */
export function span(p, window) {
  const t = ramp(p, window);
  return 1 - (1 - t) ** 3;
}

/** A staggered phase window for item i. */
export function staggerWindow(start, duration, delay, index) {
  if (![start, duration, delay, index].every(Number.isFinite) || duration <= 0 || delay < 0 || !Number.isInteger(index) || index < 0) {
    throw new RangeError('Invalid stagger arguments');
  }
  const first = start + delay * index;
  return [first, first + duration];
}

/** Fractional progress along one of two video clips. */
export function clipProgress(globalProgress, seam = 0.5) {
  if (!Number.isFinite(globalProgress) || !Number.isFinite(seam) || seam <= 0 || seam >= 1) {
    throw new RangeError('Expected progress finite and seam between 0 and 1');
  }
  return {
    a: clamp(globalProgress / seam),
    b: clamp((globalProgress - seam) / (1 - seam)),
  };
}

/** Opacity of incoming video B during a symmetric seam crossfade. */
export function crossfadeMix(p, seam = 0.5, halfWidth = 0.02) {
  if (!Number.isFinite(seam) || !Number.isFinite(halfWidth) || halfWidth <= 0 || seam - halfWidth < 0 || seam + halfWidth > 1) {
    throw new RangeError('Invalid seam or halfWidth');
  }
  return ramp(p, [seam - halfWidth, seam + halfWidth]);
}

/** Convert a prototype time range (milliseconds) into normalized progress. */
export function msWindow(startMs, endMs, totalMs) {
  if (![startMs, endMs, totalMs].every(Number.isFinite) || totalMs <= 0 || startMs < 0 || endMs <= startMs || endMs > totalMs) {
    throw new RangeError('Invalid source timeline');
  }
  return [startMs / totalMs, endMs / totalMs];
}

function assertWindow(p, start, end) {
  if (![p, start, end].every(Number.isFinite) || start >= end) {
    throw new RangeError('Expected finite progress and strictly ascending window');
  }
}
