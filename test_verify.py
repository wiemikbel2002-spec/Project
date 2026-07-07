from app.part3.level1 import assess_level1
from app.part3.level2 import assess_level2

print('=' * 60)
print('LEVEL 1 VERIFICATION')
print('=' * 60)

tests = [
    ('Ex1',  'SA-285 Grade C',                  1.0,     None,   True,  'A', 68,   38),
    ('Ex2',  'SA-53 Grade B',                   0.5,     None,   False, 'B', -7,   -7),
    ('Ex3',  'SA-516 Grade 70 (normalized)',    1.5,     None,   True,  'D', -14,  -44),
    ('Ex4',  'SA-516 Grade 65',                 1.0,     None,   True,  'B', 31,   1),
    ('Ex5',  'SA-204 Grade B',                  2.75,    None,   True,  'A', 108,  108),
    ('Ex7',  'SA-204 Grade A',                  1.6875,  1.7165, True,  'A', 93,   93),
    ('Ex8',  'SA-414 Grade G',                  1.26,    None,   False, 'A', 80,   80),
    ('Ex12', 'SA-515 Grade 70',                 1.5625,  None,   True,  'A', 89.2, 89.2),
    ('Ex14', 'SA-516 Grade 70 (not normalized)', 0.625,  None,   False, 'B', 5,    5),
    ('Ex15', 'SA-516 Grade 70 (not normalized)', 0.5625, None,   False, 'B', -1,   -1),
]

passed = 0
for name, mat, tn, ta, pwht, expc, e1, ef in tests:
    r = assess_level1(mat, tn, pwht=pwht, actual_thickness=ta, units='US')
    ok = (r.curve == expc and abs(r.mat_step1 - e1) < 0.2 and abs(r.mat_final - ef) < 0.2)
    if ok:
        passed += 1
    status = 'PASS' if ok else 'FAIL'
    print(f'{name}: Curve={r.curve} MAT1={r.mat_step1:.1f} MATf={r.mat_final:.1f} [{status}]')

print(f'\nLevel 1: {passed}/{len(tests)} passed')

print()
print('=' * 60)
print('LEVEL 2 - EXAMPLE 4 VERIFICATION')
print('=' * 60)

r = assess_level2(
    material='SA-516 Grade 65', nominal_thickness=1.0, inside_diameter=90.0,
    allowable_stress=18600, joint_efficiency=1.0, design_pressure=250,
    fca=0.125, loss=0.0, pwht=True, cet=-10, component_type='cylinder', units='US',
)
expected = {250: -29, 240: -32, 200: -43, 150: -85, 100: -155}
for rr in r.rows:
    for pe, me in expected.items():
        if abs(rr.pressure - pe) < 2:
            print(f'P={rr.pressure:.0f}: MAT={rr.mat:.1f} (expected ~{me})')

print()
print('=' * 60)
print('LEVEL 2 - EXAMPLE 5 VERIFICATION')
print('=' * 60)

r = assess_level2(
    material='SA-204 Grade B', nominal_thickness=2.75, inside_diameter=232.0,
    allowable_stress=17500, joint_efficiency=1.0, design_pressure=390,
    fca=0.125, loss=0.0, pwht=True, component_type='cylinder', units='US',
)
expected = {390: 108, 351: 98, 312: 88, 273: 78, 234: 68, 195: 48, 156: -155}
for rr in r.rows:
    for pe, me in expected.items():
        if abs(rr.pressure - pe) < 2:
            print(f'P={rr.pressure:.0f}: MAT={rr.mat:.1f} (expected ~{me})')
