import cadquery as cq

outer_radius = 30
height = 45
wall_thickness = 2
inner_radius = outer_radius - wall_thickness
rim_fillet = 0.8
slot_width = 3
slot_height = 10
slot_count = 12
rib_radius = 10
rib_height = 6
rib_offset = inner_radius - rib_radius - 0.5

def firstSolid(self):
    return self.newObject([self.findSolid()])

cq.Workplane.firstSolid = firstSolid

base = (
    cq.Workplane("XY")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, height)
    .lineTo(inner_radius, height)
    .lineTo(inner_radius, 0)
    .close()
    .revolve()
    .faces(">Z").edges().fillet(rim_fillet)
)

vented = (
    base
    .faces("|Z").workplane()
    .polarArray(radius=outer_radius - wall_thickness/2, count=slot_count, startAngle=0, angle=360)
    .rect(slot_width, slot_height)
    .cutBlind(-wall_thickness)
)

rib = (
    cq.Workplane("XY")
    .center(rib_offset, 0)
    .circle(rib_radius)
    .extrude(rib_height)
)

result = vented.union(rib)
