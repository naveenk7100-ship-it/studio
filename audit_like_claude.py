#!/usr/bin/env python3
"""
Independent video audit for FLASH reels. Same metrics the reviewer uses.
Usage:  python audit_like_claude.py path/to/video.mp4 [--web]   (needs ffmpeg + ffprobe in PATH, pip install numpy pillow)
Prints a PASS/FAIL table and writes <video>.audit.json. Do not change thresholds.
"""
import sys, os, json, subprocess, tempfile, glob, shutil
import numpy as np
from PIL import Image, ImageFilter

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, errors="replace")

def probe(p):
    j = json.loads(run(["ffprobe","-v","error","-print_format","json","-show_format","-show_streams",p]).stdout)
    v = next(s for s in j["streams"] if s["codec_type"]=="video")
    a = next((s for s in j["streams"] if s["codec_type"]=="audio"), None)
    return dict(duration=float(j["format"]["duration"]), size_mb=os.path.getsize(p)/1e6,
                bitrate_mbps=float(j["format"].get("bit_rate",0))/1e6, width=v["width"], height=v["height"],
                fps=eval(v["r_frame_rate"]), sample_rate=int(a["sample_rate"]) if a else 0)

def loudness(p):
    r = run(["ffmpeg","-hide_banner","-nostats","-i",p,"-af","ebur128=peak=true","-f","null","-"]).stderr
    I = peak = None
    for l in r.splitlines():
        if "I:" in l and "LUFS" in l: I = float(l.split("I:")[1].split("LUFS")[0])
        if "Peak:" in l and "dBFS" in l: peak = float(l.split("Peak:")[1].split("dBFS")[0])
    return I, peak

def frames(p, d, fps, scale, fmt="gray"):
    run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i",p,"-vf",f"fps={fps},scale={scale},format={fmt}",os.path.join(d,"f%05d.png")])
    return sorted(glob.glob(os.path.join(d,"f*.png")))

def motion_per_second(p):
    d = tempfile.mkdtemp()
    fs = frames(p, d, 10, "108:192")
    im = [np.asarray(Image.open(x)).astype(float) for x in fs]
    diff = np.array([np.abs(im[i]-im[i-1]).mean() for i in range(1,len(im))])
    shutil.rmtree(d)
    return [round(float(diff[i:i+10].mean()),2) for i in range(0,len(diff),10)]

def empty_area_per_second(p):
    d = tempfile.mkdtemp()
    fs = frames(p, d, 1, "180:320")
    out = []
    for x in fs:
        I = Image.open(x).convert("L"); a = np.asarray(I).astype(float); bg = np.median(a)
        bl = np.asarray(I.filter(ImageFilter.GaussianBlur(3))).astype(float)
        g = np.abs(np.diff(bl,axis=1))[:-1,:] + np.abs(np.diff(bl,axis=0))[:,:-1]
        flat = (np.abs(bl[:-1,:-1]-bg) < 14) & (g < 2.0)
        out.append(round(float(flat.mean())*100,1))
    shutil.rmtree(d)
    return out

def caption_margin_check(p):
    """Caption text must stay >= 5% from both sides (clipped words fail). Looks at the lower-middle caption zone."""
    d = tempfile.mkdtemp()
    fs = frames(p, d, 4, "360:640")
    bad = 0; worst = 100.0
    for x in fs:
        a = np.asarray(Image.open(x)).astype(float)
        zone = a[int(640*0.72):int(640*0.87), :]
        mask = zone > 235            # bright text pixels
        cols = np.where(mask.sum(axis=0) > 1)[0]
        if len(cols) < 8: continue
        left = cols.min()/360*100; right = (359-cols.max())/360*100
        m = min(left, right); worst = min(worst, m)
        if m < 5.0: bad += 1
    shutil.rmtree(d)
    return bad, round(worst,1), len(fs)

def phrase_end_ratios(p):
    wav = os.path.join(tempfile.gettempdir(), "audit_tmp.wav")
    run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i",p,"-ac","1","-ar","16000",wav])
    import wave
    w = wave.open(wav); x = np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)/32768
    env = np.array([np.sqrt((x[i:i+320]**2).mean()) for i in range(0,len(x)-320,160)])
    th = env.max()*0.05; v = env > th; segs=[]; s=None; g=0
    for k,q in enumerate(v):
        if q:
            if s is None: s=k
            g=0; e=k
        else:
            g+=1
            if s is not None and g>=8: segs.append((s,e)); s=None
    if s is not None: segs.append((s,e))
    segs=[(a,b) for a,b in segs if b-a>=8]
    r=[round(float(env[max(a,b-2):b+1].mean()/np.median(env[a:b+1])),2) for a,b in segs]
    return len(segs), sum(1 for z in r if z>0.5)

def main():
    p = sys.argv[1]; web = "--web" in sys.argv
    pr = probe(p); I, peak = loudness(p)
    mot = motion_per_second(p); emp = empty_area_per_second(p)
    capbad, capworst, capn = caption_margin_check(p)
    nph, abrupt = phrase_end_ratios(p)
    srt = sorted(mot)
    checks = [
        ("size/bitrate", f"{pr['size_mb']:.1f} MB, {pr['bitrate_mbps']:.1f} Mbps", pr["bitrate_mbps"] <= (3.5 if web else 12.0)),
        ("sample rate 48000", pr["sample_rate"], pr["sample_rate"] == 48000),
        ("resolution", f"{pr['width']}x{pr['height']}", pr["height"] > pr["width"]),
        ("duration 30-60 s", round(pr["duration"],1), 30 <= pr["duration"] <= 60.5),
        ("loudness -14 +/-0.5", I, I is not None and abs(I+14) <= 0.5),
        ("peak <= -1.5 dBFS", peak, peak is not None and peak <= -1.5),
        ("motion median >= 3.0", srt[len(srt)//2], srt[len(srt)//2] >= 3.0),
        ("no second < 1.5", min(mot), min(mot) >= 1.5),
        ("empty area max <= 35%", max(emp), max(emp) <= 35.0),
        ("empty area mean <= 25%", round(sum(emp)/len(emp),1), sum(emp)/len(emp) <= 25.0),
        ("caption clipped frames = 0", f"{capbad}/{capn} frames, worst margin {capworst}%", capbad == 0),
        ("abrupt phrase ends <= 15%", f"{abrupt}/{nph}", nph == 0 or abrupt/nph <= 0.15),
    ]
    print(f"\nAUDIT: {os.path.basename(p)}")
    for n, v, ok in checks: print(f"  [{'PASS' if ok else 'FAIL'}] {n}: {v}")
    print("  motion/sec:", mot); print("  empty%/sec:", emp)
    print("  OVERALL:", "PASS" if all(c[2] for c in checks) else "FAIL")
    json.dump(dict(file=p, probe=pr, loudness=I, peak=peak, motion=mot, empty=emp,
                   checks=[dict(name=n, value=str(v), ok=bool(ok)) for n,v,ok in checks]),
              open(p+".audit.json","w"), indent=1)

if __name__ == "__main__":
    main()
