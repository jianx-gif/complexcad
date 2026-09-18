import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().circle(100).circle(85,mode='s').finalize().extrude(-200).union(w0.sketch().arc((-99,-24),(0,-99),(99,-24)).segment((57,-24)).arc((58,-15),(57,-6)).segment((99,-6)).arc((0,99),(-99,-6)).segment((-57,-6)).arc((-58,-15),(-57,-24)).close().assemble().finalize().extrude(-183))