import cadquery as cq

# Parameters
outer_radius = 30.0
housing_length = 60.0
flange_width = 15.0
flange_height = 10.0
wall_thickness = 2.0
flange_hole_diameter = 6.0
flange_hole_spacing = 40.0

class BrakeCaliperHousing:
    def __init__(self, outer_radius, housing_length, flange_width, flange_height, wall_thickness,
                 hole_diameter, hole_spacing):
        self.outer_radius = outer_radius
        self.housing_length = housing_length
        self.flange_width = flange_width
        self.flange_height = flange_height
        self.wall_thickness = wall_thickness
        self.hole_diameter = hole_diameter
        self.hole_spacing = hole_spacing

    def _base_profile(self):
        return (
            cq.Workplane("XZ")
            .moveTo(0, 0)
            .lineTo(self.outer_radius, 0)
            .lineTo(self.outer_radius, self.housing_length)
            .lineTo(self.outer_radius + self.flange_width, self.housing_length)
            .lineTo(self.outer_radius + self.flange_width, self.housing_length + self.flange_height)
            .lineTo(self.outer_radius, self.housing_length + self.flange_height)
            .lineTo(0, self.housing_length + self.flange_height)
            .close()
        )

    def build(self):
        solid = self._base_profile().revolve()
        thin = solid.shell(self.wall_thickness)
        drilled = (
            thin
            .faces(">Z")
            .workplane()
            .rarray(self.hole_spacing, 0, 2, 1)
            .hole(self.hole_diameter)
        )
        return drilled

# Instantiate and build the part
part = BrakeCaliperHousing(
    outer_radius=outer_radius,
    housing_length=housing_length,
    flange_width=flange_width,
    flange_height=flange_height,
    wall_thickness=wall_thickness,
    hole_diameter=flange_hole_diameter,
    hole_spacing=flange_hole_spacing,
)
result = part.build()
