import os

files = [
    r'C:\Users\navee\OneDrive\Desktop\studio\engine\src\compositions\CinematicEssay_Unslop.tsx',
    r'C:\Users\navee\OneDrive\Desktop\studio\engine\src\compositions\CinematicEssay_UV.tsx',
    r'C:\Users\navee\OneDrive\Desktop\studio\engine\src\compositions\CinematicEssay_Kimi.tsx',
    r'C:\Users\navee\OneDrive\Desktop\studio\engine\src\compositions\CinematicEssay_Craft.tsx'
]

logo_block = '''              {/* FLASH Official Brand Logo */}
              <div
                style={{
                  width: 140,
                  height: 140,
                  borderRadius: "50%",
                  overflow: "hidden",
                  border: "3px solid #00E5FF",
                  boxShadow: "0 0 35px rgba(0, 229, 255, 0.5), 0 0 50px rgba(255, 45, 149, 0.3)",
                  marginBottom: 20,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  background: "#07090E",
                }}
              >
                <Img
                  src={staticFile("assets/brand/logo.png")}
                  style={{ width: "100%", height: "100%", objectFit: "cover" }}
                />
              </div>

'''

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('staticFile("brand/profile.png")', 'staticFile("assets/brand/profile.png")')
    
    target = '{/* Profile Avatar with Expanding Wave Ring */}'
    if target in content and '{/* FLASH Official Brand Logo */}' not in content:
        content = content.replace(target, logo_block + target)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated logo in {os.path.basename(fpath)}')
    else:
        print(f'Already updated or target not found in {os.path.basename(fpath)}')
