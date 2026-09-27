# Hysteresis Gate

Hysteresis Gate is a small Python library for change detection with separate rise and fall thresholds. You feed it a stream of numeric values; it hands back a boolean that only flips when the input crosses a threshold chosen for the direction of motion.

```python
from hysteresis_gate import HysteresisGate

gate = HysteresisGate(rise=10.0, fall=5.0)

gate.update(8.0)   # False - below rise, no change
gate.update(10.0)  # True  - reached rise, opens
gate.update(7.0)   # True  - in band, stays open
gate.update(5.0)   # False - reached fall, closes

gate.state         # False
gate.reset()        # back to closed, thresholds unchanged
```

## Why this exists

A noisy signal that wanders across a single threshold will make a naive `value > threshold` test chatter on every sample. Splitting the decision into a rise threshold and a lower fall threshold gives the output stickiness: once the gate opens, small dips below rise no longer close it, and once it closes, small blips above fall no longer reopen it. The trade-off is a dead band between the two thresholds where the output is whatever it last decided, so you must pick thresholds that bracket the noise floor rather than sit on top of it.

## Threshold convention

`rise` is inclusive for opening; `fall` is inclusive for closing. A value exactly on a threshold triggers that transition. `rise` must be greater than or equal to `fall`; setting `rise < fall` raises `ValueError`, since a gate that opens below where it closes has no well-defined band. When `rise == fall` the gate degenerates to a plain threshold, which is permitted and occasionally useful.

## Edge case worth knowing

Initial state defaults to closed. If your process boots while the signal is already above `rise`, the first `update` call will open the gate and you will see that transition. If you want to model "already open at startup", pass `initial=True` to the constructor or to `reset`.
