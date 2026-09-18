import cadquery as cq

# Parameters
length = 80.0
width = 60.0
height = 40.0
shell_thickness = 2.0
fillet_radius = 1.5
stiffener_web_thickness = 3.0
stiffener_flange_width = 8.0
stiffener_depth = 12.0
stiffener_spacing = 15.0
num_stiffeners = int((height - 2*stiffener_flange_width) // stiffener_spacing) + 1

# Base solid box
base = cq.Workplane('XY').box(length, width, height)
# Create thin-walled rectangular shell (open top)
shell = base.shell(-shell_thickness)
# Apply fillet to outer edges except the open top rim
edges_to_fillet = shell.edges('>Z')
model = shell.edges('>Z').fillet(fillet_radius)
# Add internal stiffeners via cut extrudes on each side wall
for i in range(num_stiffeners):
    z_pos = -height/2 + stiffener_flange_width + i*stiffener_spacing
    # Left wall (-X)
    model = model.faces('<X').workplane(centerOption='CenterOfMass', offset=0).pushPoints([ (0, z_pos) ]).rect(stiffener_depth, stiffener_web_thickness).extrude(-stiffener_flange_width)
    # Right wall (+X)
    model = model.faces('>X').workplane(centerOption='CenterOfMass', offset=0).pushPoints([ (0, z_pos) ]).rect(stiffener_depth, stiffener_web_thickness).extrude(-stiffener_flange_width)

result = model