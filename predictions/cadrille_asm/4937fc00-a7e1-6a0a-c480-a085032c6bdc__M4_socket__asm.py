parts = [base]
parts.append(place(fastener("heatset", 12), axis=(0, 0, 1), point=(-30, -20, 0), seat=1.5, flip=False))
parts.append(place(fastener("heatset", 12), axis=(0, 0, 1), point=(-30, -20, 0), seat=2.5, flip=False))
parts.append(place(fastener("heatset", 12), axis=(0, 0, 1), point=(30, -20, 0), seat=1.5, flip=False))
parts.append(place(fastener("washer", 'M4', 1), axis=(0, 0, 1), point=(-30, -20, 0), seat=-1.5, flip=True))
