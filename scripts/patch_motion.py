import os

p = r"C:\Users\navee\OneDrive\Desktop\studio\scripts\build_editorial_clean_compositions.py"
with open(p, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update cameraScale
code = code.replace(
    'const cameraScale = interpolate(frame, [0, 840], [1.0, 1.03], { extrapolateRight: "clamp" });',
    'const cameraScale = interpolate(frame, [0, 840], [1.0, 1.05], { extrapolateRight: "clamp" });'
)

# 2. Update Shots
code = code.replace(
    'const push = interpolate(shotFrame, [0, 80], [1.0, 1.02]);',
    'const push = interpolate(shotFrame, [0, 80], [1.0, 1.045]);\n            const driftY = interpolate(shotFrame, [0, 80], [14, -14]);'
)

code = code.replace(
    'const push = interpolate(shotFrame, [0, 90], [1.0, 1.025]);',
    'const push = interpolate(shotFrame, [0, 90], [1.0, 1.045]);\n            const driftY = interpolate(shotFrame, [0, 90], [14, -14]);'
)

code = code.replace(
    'const push = interpolate(shotFrame, [0, 90], [1.0, 1.02]);',
    'const push = interpolate(shotFrame, [0, 90], [1.0, 1.045]);\n            const driftY = interpolate(shotFrame, [0, 90], [14, -14]);'
)

code = code.replace(
    'const push = interpolate(shotFrame, [0, 100], [1.0, 1.025]);',
    'const push = interpolate(shotFrame, [0, 100], [1.0, 1.045]);\n            const driftY = interpolate(shotFrame, [0, 100], [14, -14]);'
)

code = code.replace(
    'const push = interpolate(shotFrame, [0, 100], [1.0, 1.02]);',
    'const push = interpolate(shotFrame, [0, 100], [1.0, 1.045]);\n            const driftY = interpolate(shotFrame, [0, 100], [14, -14]);'
)

code = code.replace(
    'const push = interpolate(shotFrame, [0, 110], [1.0, 1.025]);',
    'const push = interpolate(shotFrame, [0, 110], [1.0, 1.045]);\n            const driftY = interpolate(shotFrame, [0, 110], [14, -14]);'
)

code = code.replace(
    'const push = interpolate(shotFrame, [0, 180], [1.0, 1.02]);',
    'const push = interpolate(shotFrame, [0, 180], [1.0, 1.05]);\n            const driftY = interpolate(shotFrame, [0, 180], [18, -18]);'
)

# Replace transform scale with scale + translateY
code = code.replace('transform: `scale(${push})`,', 'transform: `scale(${push}) translateY(${driftY}px)`,')

with open(p, "w", encoding="utf-8") as f:
    f.write(code)

print("Patch applied to build_editorial_clean_compositions.py!")
