import cadquery as cq
leg_length = 80.0
leg_width = 12.0
thickness = 8.0
fillet_radius = 2.0
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_offset = 10.0
rib_width = 6.0
rib_height = 4.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = 4
base = (
    cq.Workplane("XY")
    .rect(leg_length, leg_width)
    .extrude(thickness)
)
base = base.edges("|Z").fillet(fillet_radius)
base = base.edges("|Z").fillet(fillet_radius)
base = base.edges("|Z").chamfer(chamfer_distance)
base = base.faces(">Z").workplane().center(leg_length/2, leg_width/2).rect(rib_width, rib_height).extrude(thickness)
base = base.faces(">Z").workplane().center(leg_length/2, leg_width/2).rect(rib_width, rib_height).extrude(thickness)
base = base.faces(">Z").workplane().center(leg_length/2, leg_width/2).rect(rib_width, rib_height).extrude(thickness)
base = base.faces(">Z").workplane().center(leg_length/2, leg_width/2).rect(rib_width, rib_height).extrude(thickness)
base = base.faces(">Z").workplane().center(leg_length/2, leg_width/2).rect(rib_width, rib_height).extrude(thickness)
base = base.faces(">Z").workplane().center(leg_length/2, leg_width/2).rect(rib_width, rib_height).extrude(thickness)
base = base.faces(">Z").workplane().center(leg_length/2, leg_width/2).rect(rib_width, rib_height).cutBlind(-thickness)
base = base.faces(">Z").workplane().center(leg_length/2, leg_width/2).rect(rib_width, rib_height).cutBlind(-thickness)
base = base.faces(">Z").workplane().center(leg_length/2, leg_width/2).rect(rib_width, rib_height).cutBlind(-thickness)
base = base.faces(">Z").workplane().center(leg_length/2, leg_width/2).rect(leg_width, leg_length).cutBlind(-thickness)
base = base.faces(">Z").workplane().center(leg_length/2, leg_width/2).rect(leg_width, leg_length).cutBlind(-thickness)
base = base.faces(">Z").workplane().center(leg_length/2, leg_width/2).rect(leg_width, leg_length).cutBlind(-thickness)
base = base.faces(">Z").workplane().center(leg_length/2, leg_width/2).rect(leg_width, leg_length).cutBlind(-thickness)
base = base.faces(">Z").workplane().center(leg_length/2, leg_width/2).rect(leg_width, leg_length).cutBlind(-thickness)
base = base.faces(">Z").workplane().center(leg_length/2, leg_width/2).rect(rib_width, rib_height).cutBlind(-thickness)
base = base.faces(">Z").workplane().center(leg_length/2, leg_width/2).rect(rib_width, rib_height).cutBlind(-thickness)
base = base.faces(">Z").workplane().center(leg_length/2, leg_width/2).rect(leg_width, leg_length).cutBlind(-thickness)
base = base.faces(">Z").workplane().center(leg_length/2, leg_width/2).rect(leg_width, leg_length).cutBlind(-thickness)
base = base.faces(">Z").workplane().center(leg_length/2, leg_width/2).rect(rib_width, rib_height).cutBlind(-thickness)
base = base.faces(">Z").workplane().center(leg_length/2, leg_width/2).rect(rib_width, rib_height).cutBlind(-thickness)
base