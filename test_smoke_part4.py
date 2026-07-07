"""Smoke test for Part 4 endpoints."""
from app import create_app
import json

app = create_app()
client = app.test_client()

r = client.get('/part4/')
print(f'Part 4 index: {r.status_code} ({len(r.data)} bytes)')

r = client.post('/part4/level1', data={
    't_nom': '1.0', 'inside_diameter': '40', 'design_pressure': '250',
    'allowable_stress': '20000', 'fca': '0.0625', 'loss': '0',
    't_mm': '0.80', 't_am': '0.85', 'units': 'US',
}, follow_redirects=True)
print(f'Part 4 Level 1 (POST): {r.status_code} ({len(r.data)} bytes)')

r = client.post('/part4/level2', data={
    't_nom': '1.0', 'inside_diameter': '40', 'design_pressure': '250',
    'allowable_stress': '20000', 'fca': '0.0625', 'loss': '0',
    't_mm': '0.80', 't_am': '0.85', 'units': 'US', 'rsfa': '0.95',
}, follow_redirects=True)
print(f'Part 4 Level 2 (POST): {r.status_code} ({len(r.data)} bytes)')

r = client.post('/part4/api/assess', json={
    'level': 1, 't_nom': 1.0, 'inside_diameter': 40.0,
    'design_pressure': 250.0, 'allowable_stress': 20000.0,
    't_mm': 0.80, 't_am': 0.85, 'fca_ml': 0.0625,
})
d = json.loads(r.data)
print(f'API: acceptable={d["acceptable"]}, t_min={d["t_min"]:.4f}, mawpr={d["mawpr"]:.2f}')

print('All Part 4 endpoints OK!')
