import cadquery as cq

housing_length = 80.0
housing_height = 40.0
housing_width = 60.0
wall_thickness = 2.0
vent_radius = 2.0
vent_rows = 4
vent_cols = 5
vent_spacing_x = 12.0
vent_spacing_y = 8.0
mounting_hole_diameter = 4.0
mounting_hole_spacing_x = 30.0
mounting_hole_spacing_y = 20.0
mounting_hole_rows = 2
mounting_hole_cols = 2
chamfer_size = 0.5
rib_width = 20.0
rib_thickness = 4.0
rib_height = 15.0

class GearTrainHousing:
    def __init__(self):
        self.length = housing_length
        self.height = housing_height
        self.width = housing_width
        self.thickness = wall_thickness
        self.vent_r = vent_radius
        self.vent_rows = vent_rows
        self.vent_cols = vent_cols
        self.vent_dx = vent_spacing_x
        self.vent_dy = vent_spacing_y
        self.mount_d = mounting_hole_diameter
        self.mount_rows = mounting_hole_rows
        self.mount_cols = mounting_hole_cols
        self.mount_dx = mounting_hole_spacing_x
        self.mount_dy = mounting_hole_spacing_y
        self.chamfer = chamfer_size
        self.rib_w = rib_width
        self.rib_t = rib_thickness
        self.rib_h = rib_height

    def build_profile(self):
        wp = cq.Workplane('XY')
        spline_pts = [
            (self.width, self.height * 0.75),
            (self.width * 0.9, self.height * 0.5),
            (self.width, self.height * 0.25),
            (self.width, 0.0)
        ]
        return (
            wp.moveTo(0, 0)
            .lineTo(0, self.height)
            .lineTo(self.width, self.height)
            .spline(spline_pts)
            .close()
        )

    def extrude_body(self, profile):
        return profile.extrude(self.length)

    def apply_shell(self, solid):
        return solid.shell(self.thickness)

    def add_vent_holes(self, solid):
        return (
            solid.faces('>X')
            .workplane()
            .rarray(self.vent_dx, self.vent_dy, self.vent_cols, self.vent_rows)
            .hole(self.vent_r * 2)
        )

    def add_mounting_holes(self, solid):
        return (
            solid.faces('<Z')
            .workplane()
            .rarray(self.mount_dx, self.mount_dy, self.mount_cols, self.mount_rows)
            .hole(self.mount_d)
        )

    def add_top_rib(self, solid):
        rib = (
            solid.faces('>Z')
            .workplane()
            .rect(self.rib_w, self.rib_t)
            .extrude(self.rib_h)
        )
        return solid.union(rib)

    def apply_chamfer(self, solid):
        edges = solid.edges()
        if len(edges.objects) == 0:
            return solid
        return edges.chamfer(self.chamfer)

    def assemble(self):
        profile = self.build_profile()
        body = self.extrude_body(profile)
        shelled = self.apply_shell(body)
        vented = self.add_vent_holes(shelled)
        mounted = self.add_mounting_holes(vented)
        ribbed = self.add_top_rib(mounted)
        final = self.apply_chamfer(ribbed)
        return final

result = GearTrainHousing().assemble()
