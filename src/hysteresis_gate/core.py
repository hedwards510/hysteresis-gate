"""Hysteresis gate: change detection with separate rise/fall thresholds."""


class HysteresisGate:
    """A boolean state machine with distinct rise and fall thresholds.

    The gate is either open (True) or closed (False). A new value opens it
    when the input climbs at or above `rise`; it closes only when the input
    falls at or below `fall`. Values strictly between the thresholds leave
    the state unchanged, which is the entire point: a noisy signal that
    hovers around a single threshold won't chatter the output.

    We pick the interpretation that `rise` is the *inclusive* boundary for
    opening and `fall` is the *inclusive* boundary for closing. A value
    exactly equal to a threshold triggers the corresponding transition, so
    the band between thresholds is (fall, rise) exclusive on both ends. This
    is the only choice that makes the thresholds fully symmetric: whatever
    a threshold equals, it crosses it.
    """

    def __init__(self, rise: float, fall: float, *, initial: bool = False):
        if rise < fall:
            raise ValueError(
                f"rise threshold ({rise}) must be >= fall threshold ({fall}); "
                "if they are equal the gate degenerates to a plain threshold."
            )
        self.rise = rise
        self.fall = fall
        self._open = bool(initial)

    @property
    def state(self) -> bool:
        """Current gate state. True means open, False means closed."""
        return self._open

    def update(self, value: float) -> bool:
        """Feed in a new value and return the (possibly changed) state.

        On each call exactly one transition rule applies:
        * if value >= rise: open the gate (and stay open while above rise)
        * elif value <= fall: close the gate (and stay closed while below fall)
        * otherwise: leave the state untouched.

        The order matters when rise == fall: the rise branch wins, which is
        correct because in that degenerate case the gate behaves like a plain
        threshold and a value exactly at the threshold should count as risen.
        """
        if value >= self.rise:
            self._open = True
        elif value <= self.fall:
            self._open = False
        return self._open

    def reset(self, *, initial: bool = False) -> None:
        """Reset the state without changing the thresholds."""
        self._open = bool(initial)
