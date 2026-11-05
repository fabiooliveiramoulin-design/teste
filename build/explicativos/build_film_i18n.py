import subprocess, os, json
V = "/home/claude/video"; A = "/mnt/user-data/uploads/Downloads"; C = f"{V}/clips"; L = os.sys.argv[1]; S = f"{V}/segs_{L}"; G = f"{V}/i18n/{L}"
os.makedirs(S, exist_ok=True)
ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "25", "-an"]
def run(cmd): subprocess.run(cmd, check=True, stderr=subprocess.DEVNULL if "-q" not in os.sys.argv else None)
BASE = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,fps=25"

# (scene, kind, src, dur, narration offset, lower-third)
P = [
 (1,"clip","c01",9.0,.4,None),(2,"clip","c02",9.0,.4,"s02"),(3,"clip","c03",8.0,.4,"s03"),
 (4,"clip","c04",12.0,.4,"s04"),(5,"clip","c05",12.0,.4,"s05"),(6,"clip","c06",15.0,.2,"s06"),
 (7,"clip","c07",11.0,.3,None),(8,"clip","c08",9.0,.6,None),(9,"clip","c09",12.0,.4,"s09"),
 (10,"clip","c10",10.0,.5,None),
 (11,"split",("cL11",0.0,"p1_clima"),7.5,.4,None),(12,"split",("cL12",0.0,"p2_umidade"),8.0,.3,None),
 (13,"split",("cL11",7.5,"p3_pragas"),4.0,.3,None),(14,"split",("cL12",8.0,"p4_solo"),11.0,.3,None),
 (15,"split",("cL11",11.5,"p5_gado"),8.3,.3,None),
 (16,"mosaic",None,9.5,.5,None),(17,"end","c17",10.5,.8,None),
]
CROPX = {"cL11": 0, "cL12": 760}

def seg(i, kind, src, d, lt):
    out = f"{S}/s{i:02d}.mp4"
    if kind == "clip":
        vf = f"[0:v]{BASE},tpad=stop_mode=clone:stop_duration=6,trim=0:{d},setpts=PTS-STARTPTS[v]"
        inp = ["-i", f"{C}/{src}.mp4"]
        if lt:
            inp += ["-loop", "1", "-t", str(d), "-i", f"{G}/lt/{lt}.png"]
            vf += f";[1:v]format=rgba,fade=in:st=1.0:d=0.5:alpha=1,fade=out:st={d-1.2}:d=0.5:alpha=1[l];[v][l]overlay=0:0[v]"
        run(["ffmpeg", "-y", *inp, "-filter_complex", vf, "-map", "[v]", "-t", str(d), *ENC, out])
    elif kind == "split":
        c, st, p = src; x = CROPX[c]
        vf = (f"[0:v]{BASE},setpts=1.4*PTS,fps=25,trim={st}:{st+d},setpts=PTS-STARTPTS,crop=960:1080:{x}:0[l];"
              f"[1:v]scale=960:1080,fps=25,tpad=stop_mode=clone:stop_duration=3,trim=0:{d},setpts=PTS-STARTPTS[r];"
              f"[l][r]hstack=2,drawbox=x=958:y=0:w=4:h=1080:color=0x8FCB5A@0.9:t=fill[v]")
        run(["ffmpeg", "-y", "-i", f"{C}/{c}.mp4", "-i", f"{G}/anim/{p}.mp4", "-filter_complex", vf, "-map", "[v]", "-t", str(d), *ENC, out])
    elif kind == "mosaic":
        img = f"{G}/13_culturas.jpg"; parts = []; fc = f"color=c=0x2E1D10:s=1920x1080:d={d}:r=25[bg];[0:v]fps=25,split=4[i0][i1][i2][i3];"
        q = [(0,0),(960,0),(0,540),(960,540)]
        for k,(qx,qy) in enumerate(q):
            fc += f"[i{k}]crop=960:540:{qx}:{qy},format=rgba,fade=in:st={k*1.3}:d=0.7:alpha=1[q{k}];"
        fc += "[bg][q0]overlay=0:0[a];[a][q1]overlay=960:0[b];[b][q2]overlay=0:540[c];[c][q3]overlay=960:540,"
        fc += f"scale=2304:1296,zoompan=z='1+0.06*on/({int(d*25)})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=25[v]"
        run(["ffmpeg", "-y", "-loop", "1", "-t", str(d), "-i", img, "-filter_complex", fc, "-map", "[v]", "-t", str(d), *ENC, out])
    elif kind == "end":
        cl = 6.5; fd = 1.0; hold = d - cl + fd
        fc = (f"[0:v]{BASE},tpad=stop_mode=clone:stop_duration=4,trim=0:{cl},setpts=PTS-STARTPTS[a];"
              f"[1:v]scale=2112:1188,zoompan=z='1.1-0.1*on/({int(hold*25)})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=25,trim=0:{hold},setpts=PTS-STARTPTS[b];"
              f"[a][b]xfade=transition=fade:duration={fd}:offset={cl-fd},fade=out:st={d-1.2}:d=1.2[v]")
        run(["ffmpeg", "-y", "-i", f"{C}/{src}.mp4", "-loop", "1", "-t", str(hold), "-i", f"{G}/14_final.jpg", "-filter_complex", fc, "-map", "[v]", "-t", str(d), *ENC, out])
    return out

only = [int(a) for a in os.sys.argv[2:] if a.isdigit()]
t = 0.0; starts = []
for (i, kind, src, d, off, lt) in P:
    starts.append((i, t + off));
    if (not only or i in only) and "--mix" not in os.sys.argv:
        if kind == "clip" and not lt: import shutil; shutil.copy(f"{V}/segs/s{i:02d}.mp4", f"{S}/s{i:02d}.mp4")
        else: print("seg", i, flush=True); seg(i, kind, src, d, lt)
    t += d
total = t; print("total", total)
json.dump({"starts": starts, "total": total}, open(f"{V}/timeline_{L}.json", "w"))
if only or "--segs" in os.sys.argv: raise SystemExit

open(f"{S}/list.txt","w").write("".join(f"file 's{i:02d}.mp4'\n" for i,*_ in P))
run(["ffmpeg","-y","-f","concat","-safe","0","-i",f"{S}/list.txt","-vf","fade=in:st=0:d=0.8","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-r","25",f"{V}/video_mudo_{L}.mp4"])

ins = []; fc = ""
for k,(i,st) in enumerate(starts):
    ins += ["-i", f"{V}/aud/{L}_{i:02d}.wav"]; ms = int(st*1000)
    fc += f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[n{k}];"
fc += "".join(f"[n{k}]" for k in range(len(starts))) + f"amix=inputs={len(starts)}:normalize=0,volume=1.0,apad,atrim=0:{total}[nar];"
m = len(starts); ins += ["-i", f"{A}/hfv_musica.mp3"]
fc += (f"[{m}:a]aresample=48000,aformat=channel_layouts=stereo,apad,atrim=0:{total},afade=in:st=0:d=1.5,afade=out:st={total-3.5}:d=3.5,volume=0.20[mus];"
       f"[nar]asplit=2[nar1][nar2];[mus][nar2]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[duck];"
       f"[nar1][duck]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[out]")
run(["ffmpeg","-y",*ins,"-filter_complex",fc,"-map","[out]","-t",str(total),"-c:a","pcm_s16le",f"{V}/trilha_{L}.wav"])
run(["ffmpeg","-y","-i",f"{V}/video_mudo_{L}.mp4","-i",f"{V}/trilha_{L}.wav","-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",f"{V}/HelpFarm_Filme_{L}_1080p.mp4"])
print("ok")
