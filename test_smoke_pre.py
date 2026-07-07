"""Smoke test for pre-assessment."""
from app import create_app
app = create_app()
client = app.test_client()

r = client.get('/part4/pre-assessment')
print(f'GET pre-assessment: {r.status_code} ({len(r.data)} bytes)')

r = client.post('/part4/pre-assessment', data={
    'design_code_ok': 'yes', 'smooth_contours': 'yes', 'not_cyclic': 'yes',
    'component_type': 'cylinder', 'has_supplemental_loads': '',
    'distance_ok': 'yes', 't_mm_ok': 'yes',
})
html = r.data.decode()
print(f'POST (Type A): {r.status_code} - L1 allowed={ "Level 1" in html and "Applicable" in html }')

r = client.post('/part4/pre-assessment', data={
    'design_code_ok': 'yes', 'smooth_contours': 'yes', 'not_cyclic': 'yes',
    'component_type': 'head_shell_junction', 'has_supplemental_loads': '',
    'distance_ok': 'yes', 't_mm_ok': 'yes',
})
html = r.data.decode()
print(f'POST (Type C): {r.status_code} - L3 required={ "Level 3" in html and "Required" in html }')

print('Pre-assessment smoke test OK')
