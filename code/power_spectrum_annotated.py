"""
power_spectrum_annotated.py
----------------------------
Annotated, importable version of the in-class `power_simple.py` demo
(ATOC 4815/5815, 10/20 and 10/22 lectures on Fourier series/transforms
and power spectra).

WHAT THIS SCRIPT DOES
----------------------
In class, `power_simple.py` computed a power spectrum as a flat,
top-to-bottom script -- useful for seeing every step happen in order,
but not something another script can reuse. The in-class task on
10/20 was exactly this: "calculate power spectrum within function,
which is saved in a separate file (i.e., you'll need to import it)".
This file is that refactor: the same math from `power_simple.py`,
wrapped in one function, `power_spectrum(T, data)`, that you can
`import` the same way you've been importing from `weather.py`.

If you already did this refactor yourself in class, compare your
version against this one -- they should agree. If you didn't get to
finish it, use this one for the homework; the math is identical to
what was on the slides.

THE IDEA, CONNECTED BACK TO LECTURE
-------------------------------------
From 10/20: any signal can be written as a sum of sines and cosines
(Euler's formula, `e^(ikx) = cos(kx) + i*sin(kx)`) -- the same idea as
projecting a vector onto a set of orthogonal basis vectors, except the
"vectors" here are orthogonal *functions* and the "dot product" is an
integral. `np.fft.fft` does exactly that projection for you, for a
*discrete*, evenly-sampled signal -- it returns one complex number per
frequency, telling you how much of that frequency is "in" your signal.

We don't care about the *phase* of each frequency (where in its cycle
it starts) -- only how much *energy* each frequency carries, the same
way electrical power P = U*I or radiative power S = E*H doesn't care
about the phase of the oscillating fields either. Squaring the
magnitude of each FFT coefficient, `np.abs(ft1[i])**2`, throws away
phase and keeps only that energy -- that's the "power" in "power
spectrum".

ONE-SIDED, NOT TWO-SIDED
--------------------------
For a REAL-valued signal (ours always is -- pixel brightness, not a
complex number), the FFT is symmetric: the energy at frequency i and
the energy at frequency (n-i) are the same physical frequency, just
reflected to the "negative frequency" side of the FFT output. Rather
than plot both halves, we fold them together: `pow1[i] = pow2p[i] +
pow2n[i]` adds the positive-frequency bin and its mirror-image
negative-frequency bin into one number per *physical* frequency. That
halves the length of what you plot and avoids double-counting nothing
-- it's genuinely the same energy counted once instead of split in
two places.

NOTE ON MAX FREQUENCY (the "n=10, f=5/2" slide)
--------------------------------------------------
With n evenly-spaced samples, the highest frequency you can resolve at
all is the Nyquist frequency, n/2 samples per the record length T --
you need at least two samples per cycle to see a wave exists. That's
why the loop below only goes up to `n//2 + 1`: there is no new
information past that point, only the mirror image already folded in
above.

USING THIS ON YOUR OWN DATA (the homework)
---------------------------------------------
`power_spectrum(T, data)` takes:
  - `data`: your 1-D signal, evenly sampled (e.g. pixel brightness
    along a straight flight track, one value per sample point).
  - `T`: the physical length the record spans (e.g. the total
    distance in km along your track) -- this is what converts the
    dimensionless FFT bin number into a real frequency (here, cycles
    per km, i.e. 1 / wavelength).
It returns `(frq, power)`, ready to `plt.loglog(frq[1:], power[1:])`
(skip index 0, the zero-frequency/"DC" term, since log(0) is
undefined and that term is just the signal's mean, not a wave).
"""

import numpy as np


def power_spectrum(T, data):
    """One-sided power spectrum of a real, evenly-sampled 1-D signal.

    Parameters
    ----------
    T : float
        Physical length spanned by `data` (e.g. total time in seconds,
        or total distance in km). Converts FFT bin number -> frequency.
    data : array_like
        The evenly-sampled signal itself.

    Returns
    -------
    frq : ndarray
        Frequencies, in units of (1 / units of T) -- e.g. 1/km if T is
        in km, i.e. cycles per km.
    power : ndarray
        One-sided power at each frequency in `frq` (same length as
        `frq`; index 0 is the zero-frequency / mean term).
    """
    n = len(data)
    ft1 = np.fft.fft(data)

    pow2p = np.zeros(n // 2 + 1)   # positive-frequency branch
    pow2n = np.zeros(n // 2 + 1)   # mirrored negative-frequency branch
    pow1 = np.zeros(n // 2 + 1)    # one-sided power (both branches folded together)
    frq = np.zeros(n // 2 + 1)

    # wave number 0 (the mean / "DC" term) has no mirror partner to fold in
    pow2p[0] = np.abs(ft1[0]) ** 2
    pow2n[0] = pow2p[0]
    pow1[0] = pow2p[0] + pow2n[0]
    frq[0] = 0

    for i in range(1, n // 2 + 1):
        pow2p[i] = np.abs(ft1[i]) ** 2         # positive-frequency bin i
        frq[i] = float(i) / float(n)            # dimensionless frequency (cycles/sample)
        pow2n[i] = np.abs(ft1[n - i]) ** 2      # its mirror at the negative-frequency end
        pow1[i] = pow2p[i] + pow2n[i]

    frqT = frq * float(n) / float(T)   # rescale cycles/sample -> cycles per unit of T
    return frqT, pow1


if __name__ == '__main__':
    # Self-test, same shape as the in-class demo: a single pure sine
    # wave should produce a power spectrum with exactly one spike, at
    # exactly the frequency we put into the wave -- if this doesn't
    # come out clean, something above is broken.
    import matplotlib.pyplot as plt

    T = 2.0                                   # record length [s]
    xx = np.linspace(0, T, 10)
    f_true = 0.5                            # [Hz] -- pick anything below Nyquist
    y1 = np.sin(2 * np.pi * f_true * xx)

    frq, p1 = power_spectrum(T, y1)

    f, p = plt.subplots(2, 1, figsize=(4, 7))
    p[0].plot(xx, y1, 'bo')
    p[0].set_xlabel("Time [s]")
    p[0].set_title(f"{f_true} Hz test signal")
    p[1].plot(frq, p1, 'bo')
    p[1].set_xlabel("Frequency [Hz]")
    p[1].set_title("Power spectrum -- should peak at {} Hz".format(f_true))
    plt.tight_layout()
    plt.show()
