parts = [base]
parts.append(place(fastener("heatset", 14), axis=(0, 0, 1), point=(0, 0, 7.5), seat=-6.3, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 8, 1), axis=(0, 0, 1), point=(33, 0, 3), seat=2.4, flip=True))
parts.append(place(fastener("washer", 'M4', 2), axis=(0, 0, 1), point=(0, -33, 6.5), seat=4.7, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 8, 2), axis=(0, 0, 1), point=(0, -33, 6.5), seat=5.6, flip=False))
parts.append(place(fastener("washer", 'M4', 3), axis=(0, 0, 1), point=(-33, 0, 6.5), seat=4.7, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 8, 3), axis=(0, 0, 1), point=(-33, 0, 6.5), seat=5.6, flip=False))
parts.append(place(fastener("washer", 'M4', 4), axis=(0, 0, 1), point=(0, 33, 6.5), seat=4.7, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 8, 4), axis=(0, 0, 1), point=(0, 33, 6.5), seat=5.6, flip=False))
