import subprocess
import os

def master_audio(in_path: str, out_path: str, target_i: float = -14.0, max_tp: float = -1.5):
    # Step 1: Measure current integrated loudness
    cmd = ["ffmpeg", "-i", in_path, "-af", "ebur128=peak=true", "-f", "null", "-"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    cur_i = None
    for line in r.stderr.splitlines():
        if "I:" in line and "LUFS" in line:
            parts = line.strip().split()
            for i, p in enumerate(parts):
                if p == "I:":
                    try:
                        cur_i = float(parts[i+1])
                    except:
                        pass
    print(f"[{os.path.basename(in_path)}] Current I: {cur_i} LUFS")
    
    diff_db = -14.0 - cur_i
    # Compensate for AAC intersample peaks: limit pre-AAC to -3.0 dBFS
    af = f"volume={diff_db:.2f}dB,alimiter=limit=0.707:attack=5:release=50:asc=true"
    
    cmd_master = [
        "ffmpeg", "-y", "-i", in_path,
        "-af", af,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        out_path
    ]
    subprocess.run(cmd_master, check=True)
    
    # Measure result
    cmd_ver = ["ffmpeg", "-i", out_path, "-af", "ebur128=peak=true", "-f", "null", "-"]
    r_ver = subprocess.run(cmd_ver, capture_output=True, text=True)
    final_i = None
    final_tp = None
    for line in r_ver.stderr.splitlines():
        if "I:" in line and "LUFS" in line:
            parts = line.strip().split()
            for i, p in enumerate(parts):
                if p == "I:":
                    try:
                        final_i = float(parts[i+1])
                    except:
                        pass
        if "Peak:" in line and "dBFS" in line:
            parts = line.strip().split()
            for i, p in enumerate(parts):
                if "Peak:" in p:
                    try:
                        final_tp = float(parts[i+1])
                    except:
                        pass
    print(f"[{os.path.basename(out_path)}] -> Final I: {final_i} LUFS, Peak: {final_tp} dBFS\n")
    return final_i, final_tp

if __name__ == "__main__":
    master_audio("out/reel_pillar_a_how_chatgpt_works_720p.mp4", "out/reel_pillar_a_mastered.mp4")
    master_audio("out/reel_pillar_b_best_tool_for_job_720p.mp4", "out/reel_pillar_b_mastered.mp4")
