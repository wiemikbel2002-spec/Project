UNITS_US = 'US'
UNITS_SI = 'SI'

def mm_to_inch(mm):
    return mm / 25.4

def inch_to_mm(inch):
    return inch * 25.4

def psi_to_mpa(psi):
    return psi * 0.00689476

def mpa_to_psi(mpa):
    return mpa / 0.00689476

def f_to_c(f):
    return (f - 32) * 5 / 9

def c_to_f(c):
    return c * 9 / 5 + 32
