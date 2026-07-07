"""
Part 4 - General Metal Loss Verification

Tests the key formulas against expected values from Annex 4A examples.

Test cases:
  Ex4-A: Cylinder, uniform moderate loss → Level 1 PASS
  Ex4-B: Cylinder, severe loss → Level 1 FAIL
  Ex4-C: Cylinder, moderate loss, Level 2 with RSFa=0.95 → PASS
"""

import sys, math
sys.path.insert(0, '.')

from app.part4.core import (
    compute_t_ml, compute_d_ml, compute_r_t, compute_L,
    compute_remaining_life, assess_level1, assess_level2,
)
from app.part4.tables import lookup_q, compute_q_from_formula
from app.part4.models import Part4VesselData

PASS = 0
FAIL = 0

def check(label, got, expected, tol=1e-4):
    global PASS, FAIL
    if abs(got - expected) <= tol:
        print(f"  [PASS] {label}: {got} ~ {expected}")
        PASS += 1
    else:
        print(f"  [FAIL] {label}: got {got}, expected {expected}")
        FAIL += 1

def check_bool(label, got, expected):
    global PASS, FAIL
    if got == expected:
        print(f"  [PASS] {label}: {got}")
        PASS += 1
    else:
        print(f"  [FAIL] {label}: got {got}, expected {expected}")
        FAIL += 1

print("=" * 60)
print("  PART 4 - GENERAL METAL LOSS VERIFICATION")
print("=" * 60)

# -----------------------------------------------------------------------
# SECTION 1: Basic formulas (Eq 4.3 – 4.8)
# -----------------------------------------------------------------------
print("\n[1] FORMULA VALIDATION\n")

# Eq 4.3
t_ml = compute_t_ml(1.0, 0.0625)
check("Eq (4.3) t_ml", t_ml, 0.9375)

# Eq 4.4 - internal FCA
d_ml = compute_d_ml(40.0, 0.0625, internal=True)
check("Eq (4.4) D_ml (internal)", d_ml, 40.125)

# Eq 4.5 - external FCA
d_ml_ext = compute_d_ml(40.0, 0.0625, internal=False)
check("Eq (4.5) D_ml (external)", d_ml_ext, 40.0)

# Eq 4.6
rt = compute_r_t(0.85, 0.0625, 0.9375)
check("Eq (4.6) R_t", rt, (0.85 - 0.0625) / 0.9375)  # = 0.84

# Eq 4.7 - check L = Q * sqrt(D_ml * t_ml)
# For Rt ≈ 0.84, Q(0.84) ≈ interpolated from table
q_val = lookup_q(0.84, rsfa=0.9)
L = compute_L(q_val, 40.125, 0.9375)
print(f"  [INFO] Q(0.84, RSFa=0.9) = {q_val:.4f}, L = {L:.4f}")
check("Q > 0", q_val > 0, True)
check("L > 0", L > 0, True)

# Eq 4.8
rlife = compute_remaining_life(0.85, 0.52, 0.01)
check("Eq (4.8) remaining life", rlife, (0.85 - 0.52) / 0.01)

# Q should be large as Rt -> 1 (approaches infinity)
q_high = lookup_q(0.99, rsfa=0.9)
check_bool("Q large as Rt -> 1", q_high > 50, True)

# -----------------------------------------------------------------------
# SECTION 2: Table 4.8 - Q lookup consistency
# -----------------------------------------------------------------------
print("\n[2] TABLE 4.8 - Q FACTOR CONSISTENCY\n")

# Q should be monotonic non-decreasing with Rt
prev_q = -1
for rt in [i/100.0 for i in range(0, 101, 5)]:
    q = lookup_q(rt, 0.9)
    check_bool(f"  Q monotonic at Rt={rt:.2f}", q >= prev_q, True)
    prev_q = q

# Q should be 0 at Rt=0
q0 = lookup_q(0.0, 0.9)
check("Q(0, 0.9)", q0, 0.0)

# -----------------------------------------------------------------------
# SECTION 3: Level 1 Assessment (Ex4-A - PASS case)
# -----------------------------------------------------------------------
print("\n[3] LEVEL 1 - Ex4-A (Uniform moderate loss, PASS)\n")

data_a = Part4VesselData(
    component_type='cylinder',
    material='SA-516 Gr 65',
    t_nom=1.0,
    inside_diameter=40.0,
    design_pressure=250.0,
    allowable_stress=20000.0,
    joint_efficiency=1.0,
    fca_ml=0.0625,
    loss=0.0,
    t_mm=0.80,
    t_am=0.85,
    units='US',
)
r_a = assess_level1(data_a)
check_bool("Ex4-A Acceptable", r_a.acceptable, True)
check("Ex4-A t_ml", r_a.t_ml, 0.9375, 1e-4)
check("Ex4-A R_t", r_a.r_t, (0.80 - 0.0625) / 0.9375, 1e-4)
check("Ex4-A MAWPr > 0", r_a.mawpr > 0, True)
check_bool("Ex4-A avg check", r_a.avg_check_pass, True)
check_bool("Ex4-A min check", r_a.min_thk_check_pass, True)
check_bool("Ex4-A MAWP check", r_a.mawp_check_pass, True)

# -----------------------------------------------------------------------
# SECTION 4: Level 1 Assessment (Ex4-B - FAIL case)
# -----------------------------------------------------------------------
print("\n[4] LEVEL 1 - Ex4-B (Severe loss, FAIL)\n")

data_b = Part4VesselData(
    component_type='cylinder',
    material='SA-516 Gr 65',
    t_nom=1.0,
    inside_diameter=40.0,
    design_pressure=2500.0,
    allowable_stress=20000.0,
    joint_efficiency=1.0,
    fca_ml=0.0625,
    loss=0.0,
    t_mm=0.45,
    t_am=0.50,
    units='US',
)
r_b = assess_level1(data_b)
check_bool("Ex4-B Acceptable", r_b.acceptable, False)
check("Ex4-B t_ml", r_b.t_ml, 0.9375, 1e-4)
check("Ex4-B R_t", r_b.r_t, (0.45 - 0.0625) / 0.9375, 1e-4)

# -----------------------------------------------------------------------
# SECTION 5: Level 2 Assessment (Ex4-C - Moderate loss, RSFa=0.95)
# -----------------------------------------------------------------------
print("\n[5] LEVEL 2 - Ex4-C (Moderate loss, RSFa=0.95, PASS)\n")

data_c = Part4VesselData(
    component_type='cylinder',
    material='SA-516 Gr 65',
    t_nom=1.0,
    inside_diameter=40.0,
    design_pressure=250.0,
    allowable_stress=20000.0,
    joint_efficiency=1.0,
    fca_ml=0.0625,
    loss=0.0,
    t_mm=0.80,
    t_am=0.85,
    units='US',
)
r_c = assess_level2(data_c, rsfa=0.95)
check_bool("Ex4-C Acceptable", r_c.acceptable, True)
check("Ex4-C t_ml", r_c.t_ml, 0.9375, 1e-4)
check("Ex4-C R_t", r_c.r_t, (0.80 - 0.0625) / 0.9375, 1e-4)
check("Ex4-C RSFa", r_c.rsfa, 0.95)

# Q should be lower (more restrictive) for RSFa=0.95 vs 0.9 at same Rt
q_a = lookup_q(r_a.r_t, 0.9)
q_c = lookup_q(r_c.r_t, 0.95)
check_bool("L2 Q <= L1 Q (stricter)", q_c <= q_a + 1e-3, True)

# -----------------------------------------------------------------------
# SECTION 6: API endpoint roundtrip
# -----------------------------------------------------------------------
print("\n[6] API ROUNDTRIP TEST\n")

from flask import Flask
from app.routes.part4 import part4_bp

app = Flask(__name__)
app.register_blueprint(part4_bp, url_prefix='/part4')
client = app.test_client()

# Test the Q-table API
resp = client.get('/part4/api/q-table?rsfa=0.9')
check_bool("Q-table API status 200", resp.status_code, 200)

# Test assessment API
resp = client.post('/part4/api/assess', json={
    'level': 1,
    'component_type': 'cylinder',
    'material': 'SA-516 Gr 65',
    't_nom': 1.0,
    'inside_diameter': 40.0,
    'design_pressure': 250.0,
    'allowable_stress': 20000.0,
    'joint_efficiency': 1.0,
    'fca_ml': 0.0625,
    'loss': 0.0,
    't_mm': 0.80,
    't_am': 0.85,
    'units': 'US',
})
check_bool("Assess API status 200", resp.status_code, 200)
import json
data = json.loads(resp.data)
check_bool("Assess API acceptable", data['acceptable'], True)

# -----------------------------------------------------------------------
# SUMMARY
# -----------------------------------------------------------------------
total = PASS + FAIL
print("\n" + "=" * 60)
print(f"  RESULTS: {PASS}/{total} passed, {FAIL}/{total} failed")
print("=" * 60)

if FAIL > 0:
    sys.exit(1)
