import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().arc((-85,29),(-65,10),(-48,-12)).segment((-48,-14)).segment((-46,-14)).arc((-29,-23),(-11,-29)).segment((-11,-30)).segment((85,-2)).segment((85,29)).segment((85,30)).arc((65,59),(48,81)).segment((48,83)).segment((-85,29)).assemble().finalize().extrude(-200)