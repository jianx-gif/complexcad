import cadquery as cq

class Measures:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

class LBracket:
    def __init__(self, workplane, measures):
        self.model = workplane
        self.measures = measures
        self.build()

    def build(self):
        m = self.measures
        wp = (
            cq.Workplane("XY")
            .polyline([
                (0, 0),
                (m.horizontal_length, 0),
                (m.horizontal_length, m.thickness),
                (m.thickness, m.thickness),
                (m.thickness, m.vertical_length),
                (0, m.vertical_length),
            ])
            .close()
            .extrude(m.thickness_z)
        )
        wp = (
            wp.edges("|Z")
            .filter(lambda e: abs(e.Center().x) < 1e-6 and abs(e.Center().y) < 1e-6)
            .fillet(m.inner_fillet_radius)
        )
        wp = (
            wp.faces(">Z")
            .workplane()
            .center(m.horizontal_length/2, m.thickness/2)
            .hole(m.through_hole_diameter)
        )
        wp = (
            wp.faces(">Z")
            .workplane()
            .center(m.thickness/2, m.vertical_length/2)
            .rect(m.mount_hole_pattern_spacing, m.mount_hole_pattern_spacing, forConstruction=True)
            .vertices()
            .hole(m.mount_hole_diameter)
        )
        if m.add_rib:
            rib = (
                cq.Workplane("XY")
                .rect(m.rib_width, m.rib_height)
                .extrude(m.thickness_z)
                .translate((m.thickness/2, m.thickness/2, 0))
            )
            wp = wp.union(rib)
        self.model = wp

measures = Measures(
    horizontal_length=80.0,
    vertical_length=60.0,
    thickness=10.0,
    thickness_z=10.0,
    inner_fillet_radius=6.0,
    through_hole_diameter=8.0,
    mount_hole_diameter=5.0,
    mount_hole_pattern_spacing=30.0,
    add_rib=True,
    rib_width=15.0,
    rib_height=30.0,
)

result = LBracket(cq.Workplane("XY"), measures).model
