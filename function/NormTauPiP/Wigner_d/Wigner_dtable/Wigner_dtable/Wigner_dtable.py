import quaternionic
import spherical
ell_max = 16  # Use the largest ℓ value you expect to need
theta = 1
phi = 0

wigner = spherical.Wigner(ell_max)
R = quaternionic.array.from_spherical_coordinates(theta, phi)
D = wigner.D(R)

print(D)