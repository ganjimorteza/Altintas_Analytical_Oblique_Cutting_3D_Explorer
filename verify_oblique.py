"""Reproducibility check: algebraic reduction of Altintas (2012), Eqs. 2.48--2.53, 2.59.

Requires: numpy, scipy. Angles in radians internally.
This is a consistency check of the mathematical model, NOT experimental validation.
"""
import numpy as np
from scipy.optimize import brentq


def solve_oblique(alpha_n, beta_a, inclination):
    """Physical/principal branch, for the conventional moderate-angle regime."""
    a, b, i = alpha_n, beta_a, inclination

    def implicit_eta(eta):
        Q = np.sqrt(1 - 2 * np.sin(b)**2 * np.sin(eta)**2)
        return np.tan(eta) * (np.sin(a) + np.cos(a) / Q) - np.tan(i)

    eta = brentq(implicit_eta, -np.deg2rad(60), np.deg2rad(60), xtol=1e-14)
    Z = np.sin(b) * np.sin(eta)
    Q = np.sqrt(1 - 2 * Z * Z)
    ti = np.arcsin(Z)
    tn = np.arctan(np.tan(b) * np.cos(eta)) - a
    fi = np.arcsin(np.sqrt(2) * Z)
    fn = np.arctan(1 / Q) - tn

    X = np.cos(b) * np.cos(a) + np.sin(b) * np.cos(eta) * np.sin(a)
    Y = np.sin(b) * np.cos(eta) * np.cos(a) - np.cos(b) * np.sin(a)

    # All forces normalized by tau_s * b * h.
    Fc = 2 * (1 - Z * Z) / (np.cos(i) * (X - Q * Y))
    components = Fc * np.array([X * np.cos(i) + Z * np.sin(i),
                                Y,
                                Z * np.cos(i) - X * np.sin(i)])

    # Original Eqs. (2.48)--(2.52); the last is cross-multiplied to avoid 0/0.
    residuals = np.array([
        np.sin(ti) - np.sin(b) * np.sin(eta),
        np.tan(tn + a) - np.tan(b) * np.cos(eta),
        np.tan(eta) - (np.tan(i) * np.cos(fn - a) - np.cos(a) * np.tan(fi)) / np.sin(fn),
        np.sin(fi) - np.sqrt(2) * np.sin(ti),
        np.cos(fn + tn) * np.tan(fi) - np.tan(ti),
    ])

    # Cross-check Eq. (2.53) and Eq. (2.59) without simplification.
    D = (np.cos(tn + fn) * np.cos(ti) * np.cos(fi)
         + np.sin(ti) * np.sin(fi))
    Fc_original = 1 / (D * np.cos(i) * np.sin(fn))
    forces_original = Fc_original * np.array([
        np.cos(ti) * np.cos(tn) * np.cos(i) + np.sin(ti) * np.sin(i),
        np.cos(ti) * np.sin(tn),
        np.sin(ti) * np.cos(i) - np.cos(ti) * np.cos(tn) * np.sin(i),
    ])

    t, p = np.tan(eta), np.tan(i)
    A, C, K = np.sin(a), np.cos(a), np.cos(2*b)
    quartic_residual = ((A*A*K - C*C)*t**4 - 2*p*A*K*t**3
                        + (A*A + p*p*K - C*C)*t**2 - 2*p*A*t + p*p)
    return dict(eta=eta, theta_i=ti, theta_n=tn, phi_i=fi, phi_n=fn,
                Fc=Fc, forces=components, original_forces=forces_original,
                original_Fc=Fc_original, residuals=residuals,
                quartic_residual=quartic_residual)


def main():
    d2r = np.deg2rad
    sample = solve_oblique(d2r(10), d2r(30), d2r(15))
    print("Example: alpha_n=10 deg, beta_a=30 deg, i=15 deg")
    for k in ["eta", "theta_i", "theta_n", "phi_i", "phi_n"]:
        print(f"  {k:12s} = {np.rad2deg(sample[k]):.10f} deg")
    print(f"  Fc /(tau_s*b*h) = {sample['Fc']:.10f}")
    for label, value in zip(["F_tc", "F_fc", "F_rc"], sample['forces']):
        print(f"  {label:12s}/(tau_s*b*h) = {value:.10f}")
    print("  Max residual Eqs 2.48--2.52:", np.max(np.abs(sample['residuals'])))
    print("  Max difference Eq 2.59:", np.max(np.abs(sample['forces'] - sample['original_forces'])))
    print("  Quartic residual:", abs(sample['quartic_residual']))

    rng = np.random.default_rng(20261020)
    worst_eq = worst_F = worst_poly = 0.0
    n = 500
    for _ in range(n):
        a = d2r(rng.uniform(-10, 20))
        b = d2r(rng.uniform(5, 40))
        i = d2r(rng.uniform(-25, 25))
        result = solve_oblique(a, b, i)
        worst_eq = max(worst_eq, np.max(np.abs(result['residuals'])))
        worst_F = max(worst_F, np.max(np.abs(result['forces']-result['original_forces'])))
        worst_poly = max(worst_poly, abs(result['quartic_residual']))
    print(f"500 reproducible random cases: max equation residual={worst_eq:.3e}")
    print(f"500 reproducible random cases: max force difference={worst_F:.3e}")
    print(f"500 reproducible random cases: max quartic residual={worst_poly:.3e}")


if __name__ == '__main__':
    main()
