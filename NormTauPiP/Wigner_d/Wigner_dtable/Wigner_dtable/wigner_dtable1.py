import quaternionic
import spherical
ell_max = 16  # Use the largest ℓ value you expect to need
(theta, phi) = (0, 0)
D = wigner.D(R)

R = quaternionic.array.from_spherical_coordinates(theta, phi)
def wigner_d(expiβ, ell_min, ell_max, out=None, workspace=None):
    """Compute Wigner's d matrix dˡₘₚ,ₘ(β)

    This is a simple wrapper for the Wigner.d method.  If you plan on calling this
    function more than once, you should probably construct a Wigner object and call
    the `d` method explicitly.

    See that function's documentation for more details.

    """
    return spherical.Wigner(ell_max, ell_min).d(expiβ, out=out, workspace=workspace)

print(wigner_d(0, 0, 1))