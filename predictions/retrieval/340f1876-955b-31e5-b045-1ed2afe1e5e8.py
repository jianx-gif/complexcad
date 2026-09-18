import cadquery as cq

flange_size = 80.0
flange_thickness = 5.0
hub_diameter = 40.0
loft_height = 30.0
fillet_radius = 2.0
central_hole_dia = 10.0
mounting_hole_dia = 5.0
mounting_hole_offset = 30.0
slot_width = 10.0
slot_length = 30.0
rib_thickness = 3.0
rib_height = loft_height * 0.6
rib_count = 4
rib_spacing_angle = 360 / rib_count

class LoftedFlangeHub:
    def __init__(self):
        self.part = None
    def build_body(self):
        wp = cq.Workplane("XY")
        wp = wp.rect(flange_size, flange_size)
        wp = wp.workplane(offset=loft_height).circle(hub_diameter / 2)
        self.part = wp.loft()
        return self
    def add_central_hole(self):
        self.part = self.part.faces(">Z").workplane().hole(central_hole_dia)
        return self
    def add_mounting_holes(self):
        self.part = (
            self.part.faces("<Z")
            .workplane()
            .pushPoints([
                (mounting_hole_offset, 0),
                (-mounting_hole_offset, 0),
                (0, mounting_hole_offset),
                (0, -mounting_hole_offset),
            ])
            .hole(mounting_hole_dia)
        )
        return self
    def add_slot(self):
        slot = (
            cq.Workplane("XY")
            .center(flange_size / 2 - slot_length / 2, 0)
            .rect(slot_length, slot_width)
            .extrude(flange_thickness + loft_height)
        )
        self.part = self.part.cut(slot)
        return self
    def add_ribs(self):
        ribs = (
            cq.Workplane("XY")
            .polarArray(radius=hub_diameter/2, startAngle=0, angle=rib_spacing_angle, count=rib_count)
            .rect(rib_thickness, rib_height)
            .extrude(flange_thickness)
            .translate((0, 0, loft_height/2))
        )
        self.part = self.part.union(ribs)
        return self
    def apply_fillet(self):
        self.part = self.part.faces(">Z").edges().fillet(fillet_radius)
        return self
    def build(self):
        return (
            self.build_body()
            .add_central_hole()
            .add_mounting_holes()
            .add_slot()
            .add_ribs()
            .apply_fillet()
            .part
        )

result = LoftedFlangeHub().build()
