# Analytical Oblique Cutting — Interactive 3D Explorer

**Status:** research demonstration; a consistency check of the *maximum-shear-stress* closure in Chapter 2 of Altintas (2012), not experimental validation or proof of literature priority.

**Author of this research note and visualization:** Morteza Ganji (ORCID: https://orcid.org/0009-0003-3601-4308).

**Repository:** https://github.com/ganjimorteza/Altintas_Analytical_Oblique_Cutting_3D_Explorer

## Explore

Open `index.html` locally in Chrome/Edge, or use the project's GitHub Pages URL once Pages is enabled. No internet access, dependencies or browser extensions are required to use the 3D explorer. The controls let you vary cutting-edge inclination `i`, normal rake `alpha_n`, average friction angle `beta_a`, shear strength `tau_s`, width `b`, and undeformed chip thickness `h`.

The explorer implements:

1. An algebraic **quartic equation in tan(eta)** obtained from Altintas Eqs. (2.48)–(2.52), using the maximum-shear-stress closure. Its roots are *found numerically*, then screened against the unsquared equation and an admissible angular branch. "Algebraic reduction" does **not** mean that the app evaluates a general quartic formula in radicals.
2. Explicit formulas for cutting-force components from Eqs. (2.53) and (2.59), excluding edge/rubbing/ploughing loads.
3. A separate numerical solver for the original velocity Eq. (2.50) and numerical force/angle residuals. This is **not** an independent physical validation, and is not an exact reproduction of the textbook's relaxation iteration.
4. Two switchable 3D views: a tool/workpiece and a force-sphere construction.

## Coordinate frames (important)

- **Fixed workpiece frame** `(Xw, Yw, Zw)`: `Xw` and `Yw` follow the rectangular workpiece edges; `Zw` is the outward work-surface normal. In the visualization, the cutting velocity is fixed along `+Xw`.
- **Tool-local Altintas frame** `(x, y, z)`: `x` lies on the machined plane normal to the straight cutting edge; `y` lies **along the cutting edge**; `z` is normal to the `xy` cut plane, just as in Altintas Fig. 2.5. The *local frame* rotates as cutting-edge inclination `i` changes while the workpiece stays stationary.

The coordinate transform used for vectors is

```
  [Xw]   [ cos(i)  sin(i)  0 ] [x]
  [Yw] = [-sin(i)  cos(i)  0 ] [y]
  [Zw]   [   0       0     1 ] [z]
```

Thus `V_local=(cos i, sin i, 0)` becomes `V_world=(1,0,0)`; the local `+y` edge direction is `(sin i,cos i,0)` in world axes. The workpiece dimensions and tool shape are schematic, not a CAD-equivalent cutting simulation.

## Mathematical domain and limits

Intended for the app's bounded inputs `-60° <= i <= 60°`, `-10° <= alpha_n <= 25°`, `0° <= beta_a <= 40°`, with a principal physically admissible shear branch, `0° < phi_n < 90°` and positive resultant. A nonphysical sign or angular branch is flagged in the interface. The algebra uses ideal straight/sharp cutting edges, a thin shear plane and an effective average friction angle.

The tool does not represent the real edge radius, flank contact, chip curling, localized thermal softening, material strain hardening, or experimental cutting-force error. The force sphere is a visualization of force-vector decompositions, not an experimental measurement.

## Reproduce numerical consistency checks

```bash
python -m pip install -r requirements.txt
python verify_oblique.py
```

The Python script checks a representative example plus 500 deterministic random angle combinations against the original textbook equations. It solves a scalar residual with SciPy and is thus algorithmically independent of the browser's quartic-root solver.

## Files

- `index.html`: self-contained browser-based application; served directly by GitHub Pages.
- `technical_note.pdf`: derivation and model scope.
- `verify_oblique.py`: numerical reproducibility script.
- `screenshot.png`: preview of updated workpiece/tool coordinate frames.
- `requirements.txt`: Python dependencies.

## Publishing

1. Upload the **contents of this folder (not the ZIP archive)** to the existing repository `https://github.com/ganjimorteza/Altintas_Analytical_Oblique_Cutting_3D_Explorer`, ensuring `index.html` is in the repository root. Do not delete or overwrite existing material without checking it first.
2. In repository **Settings → Pages**, select **Deploy from a branch**, `main` (or the actual default branch), `/(root)`, and Save. Wait for GitHub to show the published website link. Its expected form is `https://ganjimorteza.github.io/Altintas_Analytical_Oblique_Cutting_3D_Explorer/`, but it has not been verified as live.
3. After confirming the Pages website and all mathematical checks, archive this version in Zenodo via *New upload*, using the same files and an appropriate license selected by the author. Obtain the DOI **only after publishing** the record.
4. If desired, use a GitHub release and link Zenodo to that version. Do not fabricate the DOI or GitHub Pages URL before deployment.

**Licensing:** No license is asserted in this draft package. The owner must choose and add appropriate license(s) (e.g., code MIT; original report/figures CC BY 4.0 if desired) before publishing. The book itself and scanned pages are **not included**.

## Reference

Y. Altintas, *Manufacturing Automation: Metal Cutting Mechanics, Machine Tool Vibrations, and CNC Design*, 2nd ed., Cambridge University Press (2012), Section 2.5, especially Figs. 2.5–2.7 and Eqs. (2.48)–(2.53), (2.59).
