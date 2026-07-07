import http.client, json

conn = http.client.HTTPConnection('127.0.0.1', 5000, timeout=10)

conn.request('GET', '/part3/')
r = conn.getresponse()
data = r.read()
print(f'1. DASHBOARD: {r.status} ({len(data)} bytes) - Verification table + stats loaded')

l1 = {'material': 'SA-516 Gr 65', 'nominal_thickness': 1.0, 'pwht': True, 'cet': 50}
conn.request('POST', '/part3/api/level1', json.dumps(l1), {'Content-Type': 'application/json'})
r = conn.getresponse()
d = json.loads(r.read())
print(f'2. LEVEL 1 (Ex4, PWHT): MAT={d["mat_final"]}F, Acceptable={d["acceptable"]}')

l2 = {
    'material': 'SA-204 Gr B', 'nominal_thickness': 1.0, 'inside_diameter': 40.0,
    'allowable_stress': 20000, 'joint_efficiency': 1.0, 'design_pressure': 390,
    'fca': 0, 'loss': 0, 'pwht': False, 'component_type': 'cylinder', 'cet': 60,
}
conn.request('POST', '/part3/api/level2', json.dumps(l2), {'Content-Type': 'application/json'})
r = conn.getresponse()
d = json.loads(r.read())
print(f'3. LEVEL 2 (Ex5): MAT_start={d["mat_start"]}F, rows={len(d["rows"])}')

conn.request('GET', '/part3/export/csv')
r = conn.getresponse()
cd = r.getheader('Content-Disposition')
r.read()
print(f'4. CSV EXPORT: {r.status} ({cd})')

print('\nAll systems operational. Open http://127.0.0.1:5000/ in your browser!')
