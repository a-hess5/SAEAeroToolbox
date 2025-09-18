import aerosandbox as asb

# Here, all distances are in meters and all angles are in degrees.
airplane = asb.Airplane(
    name="Example Airplane",
    xyz_ref=[0.5, 0, 0],  # Reference for moments
    s_ref=9,  # Reference area
    c_ref=0.9,  # Reference chord
    b_ref=10,  # Reference span
    wings=[
        asb.Wing(
            name="Wing",
            symmetric=True,  # Should this wing be mirrored across the XZ plane?
            xsecs=[  # The wing's cross ("X") sections, or "XSecs"
                asb.WingXSec(  # Root
                    xyz_le=[0, 0, 0],  # Coordinates of the XSec's leading edge
                    chord=29*.0254,
                    twist=0,  # in degrees
                    airfoil=asb.Airfoil("goe244"),
                ),
                asb.WingXSec(  # Middle
                    xyz_le=[0, 42*.0254, 0],
                    chord=29*.0254,
                    twist=0,
                    airfoil=asb.Airfoil("goe244"),
control_surface_is_symmetric=False,  # Aileron
                    control_surface_deflection=0,  # in degrees
                    # (ctrl. surfs. are applied between this XSec and the next one.)
                ),

                asb.WingXSec(  # Tip
                    xyz_le=[14.5*.0254, 89.5*.0254, 0],
                    chord=14.5*.0254,
                    twist=0,
                    airfoil=asb.Airfoil("goe244"),
                )
            ]
        ),
        asb.Wing(
            name="H-stab",
            symmetric=True,
            xsecs=[
                asb.WingXSec(
                    xyz_le=[0, 0, 0],
                    chord=8.07*.0254,
                    airfoil=asb.Airfoil("naca0004")
                ),
                asb.WingXSec(
                    xyz_le=[0, 17.5*.0254, 0],
                    chord=8.07*.0254,
                    airfoil=asb.Airfoil("naca0004")
                ),
            ]
        ).translate([93.57*.0254, 0, -2.75*.0254]), # Used to translate all cross sections of the wing.
        # Vertical Stabilizers
        asb.Wing(
            name="Center V-stab",
            xsecs=[
                asb.WingXSec(
                    xyz_le=[0, 0, 0],
                    chord=12.11 * .0254,
                    airfoil=asb.Airfoil("naca0004")
                ),
                asb.WingXSec(
                    xyz_le=[6.06 * .0254, 0, 8 * .0254],
                    chord=6.05 * .0254,
                    airfoil=asb.Airfoil("naca0004")
                )
            ]
        ).translate([93.57 * .0254, 0, -2.75*.0254]),  # Centerline V-stab

        asb.Wing(
            name="Left V-stab",
            xsecs=[
                asb.WingXSec(
                    xyz_le=[0, 0, 0],
                    chord=12.11 * .0254,
                    airfoil=asb.Airfoil("naca0004")
                ),
                asb.WingXSec(
                    xyz_le=[6.06 * .0254, 0, 8 * .0254],
                    chord=6.05 * .0254,
                    airfoil=asb.Airfoil("naca0004")
                )
            ]
        ).translate([93.57 * .0254, -17.5 * .0254, -2.75*.0254]),  # Shift left

        asb.Wing(
            name="Right V-stab",
            xsecs=[
                asb.WingXSec(
                    xyz_le=[0, 0, 0],
                    chord=12.11 * .0254,
                    airfoil=asb.Airfoil("naca0004")
                ),
                asb.WingXSec(
                    xyz_le=[6.06 * .0254, 0, 8 * .0254],
                    chord=6.05 * .0254,
                    airfoil=asb.Airfoil("naca0004")
                )
            ]
        ).translate([93.57 * .0254, 17.5 * .0254, -2.75*.0254]),  # Shift right
    ],
    fuselages=[
        asb.Fuselage(
            name="Fuselage",
            xsecs=[
                # Nose section (rectangular)
                asb.FuselageXSec(xyz_c=[-15*.0254, 0, -2.75*.0254], width=3.5*.0254, height=3.5*.0254),

                # Main body (constant rectangle)
                asb.FuselageXSec(xyz_c=[-6.25*.0254, 0, -5*.0254], width=8*.0254, height=8*.0254),
                asb.FuselageXSec(xyz_c=[23.5*.0254, 0, -5*.0254], width=8*.0254, height=8*.0254),

                # Rear section (narrowing down)
                asb.FuselageXSec(xyz_c=[32.5*.0254, 0, -2.75*.0254], width=3.5*.0254, height=3.5*.0254),
                asb.FuselageXSec(xyz_c=[32.501*.0254, 0, -2.75*.0254], width=1*.0254, height=1*.0254),

                # Tail end (smallest rectangle)
                asb.FuselageXSec(xyz_c=[(32.501+63)*.0254, 0, -2.75*.0254], width=1*.0254, height=1*.0254),
            ]
        )
    ]
)

airplane.draw_three_view()
