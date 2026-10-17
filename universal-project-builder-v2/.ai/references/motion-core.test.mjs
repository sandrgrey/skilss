import test from 'node:test';
import assert from 'node:assert/strict';
import { clamp, lerp, ramp, span, staggerWindow, clipProgress, crossfadeMix, msWindow } from './motion-core.mjs';
import preset from './marlin-timeline.json' with { type: 'json' };

test('clamp and interpolation at boundaries', () => {
  assert.equal(clamp(-3), 0);
  assert.equal(clamp(3), 1);
  assert.equal(lerp(10, 20, 0.25), 12.5);
  assert.throws(() => clamp(0, 3, 1), RangeError);
});

test('linear ramp and ease-out span', () => {
  assert.equal(ramp(-1, [0, 1]), 0);
  assert.equal(ramp(0.5, [0, 1]), 0.5);
  assert.equal(ramp(2, [0, 1]), 1);
  assert.equal(span(0, [0, 1]), 0);
  assert.equal(span(0.5, [0, 1]), 0.875);
  assert.equal(span(1, [0, 1]), 1);
  assert.throws(() => span(0.5, [1, 1]), RangeError);
});

test('stagger windows and source timing', () => {
  const [a, b] = staggerWindow(0, 0.1, 0.025, 2);
  assert.equal(a, 0.05);
  assert.ok(Math.abs(b - 0.15) < 1e-12);
  assert.deepEqual(msWindow(8000, 14000, 20000), [0.4, 0.7]);
  assert.deepEqual(msWindow(...preset.phasesMs.move2, preset.totalMs), [0.775, 0.9]);
});

test('video seam blending and clip mapping', () => {
  assert.deepEqual(clipProgress(0, 0.5), { a: 0, b: 0 });
  assert.deepEqual(clipProgress(0.5, 0.5), { a: 1, b: 0 });
  assert.deepEqual(clipProgress(1, 0.5), { a: 1, b: 1 });
  assert.equal(crossfadeMix(0.48, 0.5, 0.02), 0);
  assert.equal(crossfadeMix(0.5, 0.5, 0.02), 0.5);
  assert.equal(crossfadeMix(0.52, 0.5, 0.02), 1);
});

test('invalid inputs rejected', () => {
  assert.throws(() => clipProgress(0.5, 1));
  assert.throws(() => crossfadeMix(0.5, 0.01, 0.02));
  assert.throws(() => msWindow(3, 1, 10));
  assert.throws(() => staggerWindow(0, 0, 0.1, 1));
});
