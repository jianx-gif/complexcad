import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().segment((-24,-14),(-17,-14)).arc((0,-25),(17,-14)).segment((24,-14)).segment((24,8)).segment((17,8)).arc((0,20),(-17,8)).segment((-24,8)).close().assemble().finalize().extrude(5).union(w0.sketch().arc((14,16),(-15,-16),(18,11)).arc((16,14),(14,16)).assemble().circle(15,mode='s').finalize().extrude(60))
