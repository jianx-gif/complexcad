import cadquery as cq

# Parameters
base_socket_radius = 12.0
housing_height = 80.0
top_cover_width = 60.0
top_cover_height = 40.0
step_count = 6
vent_slot_width = 30.0
vent_slot_height = 5.0
vent_slot_depth = 20.0
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
chamfer_distance = 1.0

class LampHousing:
    def __init__(self,
                 base_radius,
                 height,
                 top_width,
                 top_height,
                 steps,
                 vent_width,
                 vent_height,
                 vent_depth,
                 hole_dia,
                 hole_spacing,
                 chamfer):
        self.base_radius = base_radius
        self.height = height
        self.top_width = top_width
        self.top_height = top_height
        self.steps = steps
        self.step_height = height / steps
        self.vent_width = vent_width
        self.vent_height = vent_height
        self.vent_depth = vent_depth
        self.hole_dia = hole_dia
        self.hole_spacing = hole_spacing
        self.chamfer = chamfer

    def loft_body(self):
        wp = cq.Workplane("XY").circle(self.base_radius)
        for i in range(1, self.steps + 1):
            interp = i / self.steps
            width = (1 - interp) * (2 * self.base_radius) + interp * self.top_width
            height = (1 - interp) * (2 * self.base_radius) + interp * self.top_height
            wp = wp.workplane(offset=self.step_height).rect(width, height)
        solid = wp.loft(combine=True)
        return solid

    def add_vent(self, solid):
        slot = (
            cq.Workplane("XY")
            .rect(self.vent_width, self.vent_height)
            .extrude(self.vent_depth)
        )
        slot = slot.translate((self.top_width/2 - self.vent_depth/2, 0, self.height/2))
        return solid.cut(slot)

    def add_mounting_holes(self, solid):
        positions = [
            (-self.hole_spacing/2, -self.hole_spacing/2),
            ( self.hole_spacing/2, -self.hole_spacing/2),
            (-self.hole_spacing/2,  self.hole_spacing/2),
            ( self.hole_spacing/2,  self.hole_spacing/2),
        ]
        top = solid.faces('>Z').workplane()
        for x, y in positions:
            top = top.pushPoints([(x, y)]).hole(self.hole_dia)
        return top

    def add_chamfer(self, solid):
        return solid.faces('>Z').edges().chamfer(self.chamfer)

    def build(self):
        body = self.loft_body()
        body = self.add_vent(body)
        body = self.add_mounting_holes(body)
        body = self.add_chamfer(body)
        return body

result = LampHousing(
    base_radius=base_socket_radius,
    height=housing_height,
    top_width=top_cover_width,
    top_height=top_cover_height,
    steps=step_count,
    vent_width=vent_slot_width,
    vent_height=vent_slot_height,
    vent_depth=vent_slot_depth,
    hole_dia=mount_hole_diameter,
    hole_spacing=mount_hole_spacing,
    chamfer=chamfer_distance,
).build()