parts = [base]
parts.append(place(fastener("washer", 'M4', 0), axis=(0, 0, 1), point=(30, 20, 0), seat=10, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 14, 0), axis=(0, 0, 1), point=(30, 20, 0), seat=10.9, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 0), axis=(0, 0, 1), point=(30, 20, 0), seat=-10, flip=True))
