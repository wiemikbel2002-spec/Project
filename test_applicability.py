"""Test applicability pre-assessment module."""
import sys
sys.path.insert(0, '.')
from app.part4.applicability import check_applicability

PASS = 0
FAIL = 0

def check(label, got, expected):
    global PASS, FAIL
    if got == expected:
        print(f'  [PASS] {label}')
        PASS += 1
    else:
        print(f'  [FAIL] {label}: got {got}, expected {expected}')
        FAIL += 1

print('=== PART 4 APPLICABILITY PRE-ASSESSMENT TESTS ===\n')

# Case 1: Perfect Type A cylinder → Level 1 + 2 OK
print('[1] Type A cylinder, all conditions OK')
r = check_applicability(
    design_code_ok=True, smooth_contours=True, not_cyclic_service=True,
    component_type='cylinder', has_supplemental_loads=False,
    distance_ok=True, t_mm_check_ok=True,
)
check('Level 1 allowed', r.level1_allowed, True)
check('Level 2 allowed', r.level2_allowed, True)
check('Level 3 not required', r.level3_required, False)
check('Recommended', r.recommended_level, 'Level 1 or Level 2')
check('No reasons', len(r.reasons), 0)

# Case 2: Type A cylinder with supplemental loads → Level 2 only
print('\n[2] Type A cylinder WITH supplemental loads')
r = check_applicability(
    design_code_ok=True, smooth_contours=True, not_cyclic_service=True,
    component_type='cylinder', has_supplemental_loads=True,
    distance_ok=True, t_mm_check_ok=True,
)
check('Level 1 not allowed', r.level1_allowed, False)
check('Level 2 allowed', r.level2_allowed, True)
check('Recommended', r.recommended_level, 'Level 2')

# Case 3: Type C component → Level 3 only
print('\n[3] Type C (head-shell junction)')
r = check_applicability(
    design_code_ok=True, smooth_contours=True, not_cyclic_service=True,
    component_type='head_shell_junction', has_supplemental_loads=False,
    distance_ok=True, t_mm_check_ok=True,
)
check('Level 1 not allowed', r.level1_allowed, False)
check('Level 2 not allowed', r.level2_allowed, False)
check('Level 3 required', r.level3_required, True)
check('Recommended', r.recommended_level, 'Level 3')

# Case 4: Cyclic service → Level 3
print('\n[4] Cyclic service (fails condition c)')
r = check_applicability(
    design_code_ok=True, smooth_contours=True, not_cyclic_service=False,
    component_type='cylinder', has_supplemental_loads=False,
    distance_ok=True, t_mm_check_ok=True,
)
check('Level 1 not allowed', r.level1_allowed, False)
check('Level 2 not allowed', r.level2_allowed, False)
check('Level 3 required', r.level3_required, True)

# Case 5: No design code → Level 3
print('\n[5] No design code (fails condition a)')
r = check_applicability(
    design_code_ok=False, smooth_contours=True, not_cyclic_service=True,
    component_type='cylinder', has_supplemental_loads=False,
    distance_ok=True, t_mm_check_ok=True,
)
check('Level 1 not allowed', r.level1_allowed, False)
check('Level 2 not allowed', r.level2_allowed, False)
check('Level 3 required', r.level3_required, True)

# Case 6: Nozzle (Type B2) → Level 2, not Level 1
print('\n[6] Nozzle (Type B Class 2)')
r = check_applicability(
    design_code_ok=True, smooth_contours=True, not_cyclic_service=True,
    component_type='nozzle', has_supplemental_loads=False,
    distance_ok=True, t_mm_check_ok=True,
)
check('Level 1 not allowed', r.level1_allowed, False)
check('Level 2 allowed', r.level2_allowed, True)
check('Recommended', r.recommended_level, 'Level 2')

# Case 7: Multiple failures
print('\n[7] Multiple conditions fail')
r = check_applicability(
    design_code_ok=False, smooth_contours=False, not_cyclic_service=True,
    component_type='cylinder', has_supplemental_loads=False,
    distance_ok=True, t_mm_check_ok=True,
)
check('Level 1 not allowed', r.level1_allowed, False)
check('Level 3 required', r.level3_required, True)
check('2 reasons', len(r.reasons), 2)

total = PASS + FAIL
print(f'\n=== {PASS}/{total} passed, {FAIL} failed ===')
if FAIL:
    sys.exit(1)
