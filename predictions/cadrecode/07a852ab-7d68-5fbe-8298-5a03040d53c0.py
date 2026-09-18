import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,25))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-27,-99),(27,-99)).segment((27,-84)).arc((87,0),(27,84)).segment((27,99)).segment((-27,99)).segment((-27,84)).arc((-87,0),(-27,-84)).close().assemble(),mode='s').finalize().extrude(-50)