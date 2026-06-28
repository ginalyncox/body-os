# 3D-Printable Enclosure — Scout Rolling Aid

Rounded, low-profile body for a Raspberry Pi 4/5 + speaker + USB mic on a differential-drive chassis. Designed for makerspace printing (PLA/PETG, no supports on main shell).

---

## Design goals

- **Rounded edges** — no sharp corners (safe around flares / low vision)
- **Low center of gravity** — electronics in upper shell, battery on chassis below
- **Speaker up + forward** — voice projects toward you when Scout rolls up
- **Mic on top** — away from speaker cone (reduces echo)
- **Status LED visible** — front ring shows tier color
- **Service access** — hinged or slide-off lid for SD card / USB

---

## Bill of materials (printed + bought)

| Part | Qty | Notes |
|------|-----|-------|
| `scout-body-bottom.stl` | 1 | Chassis mount plate |
| `scout-body-shell.stl` | 1 | Main upper shell |
| `scout-lid.stl` | 1 | Top access panel |
| `scout-bumper.stl` | 1 | Front foam retention |
| M3×8 screws | 8 | Shell to base |
| M3 heat-set inserts | 8 | Optional, for durability |
| Pool noodle slice | 1 | 15 mm thick bumper foam |
| Zip ties | 4 | Cable management |

---

## Overall dimensions

| Measurement | Value |
|-------------|-------|
| Outer diameter | 180 mm |
| Shell height | 120 mm |
| Base plate thickness | 4 mm |
| Internal Pi clearance | 90 × 60 × 25 mm |
| Speaker grille diameter | 50 mm |
| Mic hole diameter | 8 mm |
| Wheel cutout clearance | 70 mm between wheels |

Fits standard 2-wheel kits with ~150–200 mm wheelbase.

---

## Print settings

| Setting | Value |
|---------|-------|
| Material | PETG (preferred) or PLA |
| Layer height | 0.2 mm |
| Walls | 3 perimeters |
| Infill | 20% gyroid (shell), 40% (base plate) |
| Supports | **None** on shell (designed support-free) |
| Brim | Recommended for base plate only |

---

## Assembly order

1. Print all STLs from `enclosure/` (generate with OpenSCAD — see below)
2. Press-fit or screw heat-set inserts into shell posts
3. Mount Pi to base plate with M2.5 standoffs (6 mm)
4. Attach USB speaker behind front grille; route 3.5 mm cable to Pi
5. Press ReSpeaker or USB mic into top hole; hot-glue if loose
6. Route motor wires through rear notch
7. Snap pool noodle into bumper clip; attach bumper to front
8. Screw shell to chassis base plate
9. Velcro battery under chassis (never inside hot Pi compartment)

---

## Status LED wiring (optional)

Front ring diffused with thin PLA insert:

| Tier | Color |
|------|-------|
| Green | Solid green |
| Yellow | Solid amber |
| Red | Slow red pulse |
| Black | Off or very dim blue |

Wire common-cathode RGB LED to Pi GPIO 12/13/16 with 220 Ω resistors.

---

## OpenSCAD source

Generate STLs locally:

```bash
cd robot/enclosure
openscad -o scout-body-shell.stl scout-body.scad
```

Or open `scout-body.scad` in OpenSCAD GUI and export each part.

**Don't have OpenSCAD?** Use the dimensional diagram below and ask makerspace staff to adapt, or print a simple rounded box in Tinkercad using these numbers.

---

## Dimensional diagram (top view)

```
              ┌─────────────────┐
             /    mic ●          \
            │   ┌───────────┐     │
            │   │  Pi 4/5   │     │  ← shell
            │   └───────────┘     │
            │    ╭─────────╮      │
            │    │ speaker │      │  ← grille forward
             \   ╰─────────╯     /
              └───┬─────────┬───┘
                  │ bumper  │
              ════╧═════════╧════  ← chassis + wheels
```

---

## Tuning for your build

After first print:

1. Check Pi USB ports clear the shell by 2 mm
2. Trim speaker grille if muffled
3. Add felt ring around mic if echo persists
4. Mark wheel odometry on floor tape — update `config.yaml` waypoints

---

## Files

| File | Purpose |
|------|---------|
| `scout-body.scad` | Parametric OpenSCAD model |
| `hardware.md` | Electronics / motor wiring |
