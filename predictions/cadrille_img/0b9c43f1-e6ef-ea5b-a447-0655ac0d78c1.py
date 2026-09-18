import cadquery as cq
w0=cq.Workplane('YZ',origin=(-79,0,0))
w1=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.sketch().arc((-20,-69),(58,-33),(54,51)).close().assemble().finalize().extrude(153).union(w1.sketch().arc((-24,-63),(-22,-64),(-21,-66)).arc((59,-59),(96,13)).arc((87,15),(95,19)).arc((-58,81),(-24,-63)).assemble().finalize().extrude(200))