import json,subprocess,os,glob
D=json.load(open("durations.json"));M="/mnt/user-data/uploads/Downloads/hfv_musica.mp3"
names={"v1":"home","v2":"movel","v3":"tec","v4":"cert","v5":"inv","v6":"energia","v7":"valor"}
out="/home/claude/teste/helpfarm/video"
import sys
for v,ds in [(v,D[v]) for v in sys.argv[1:]]:
  n=len(ds); open(f"out/{v}/list.txt","w").write("".join(f"file 's{i}.mp4'\n" for i in range(n)))
  subprocess.run(["ffmpeg","-loglevel","error","-y","-f","concat","-safe","0","-i",f"out/{v}/list.txt","-c","copy",f"out/{v}/vid.mp4"],check=True)
  tot=sum(d+1.25 for d in ds)
  ins=[];flt=[];t=0
  for i,d in enumerate(ds):
    ins+=["-i",f"aud/hfx_{v}-{i+1}.mp3"];ms=int((t+0.35)*1000)
    flt.append(f"[{i+1}:a]aresample=48000,adelay={ms}|{ms},apad[a{i}]");t+=d+1.25
  ins+=["-stream_loop","-1","-i",M]
  flt.append(f"[{n+1}:a]aresample=48000,volume=0.08,afade=t=in:d=1,afade=t=out:st={tot-2:.2f}:d=2[m]")
  flt.append("".join(f"[a{i}]" for i in range(n))+f"[m]amix=inputs={n+1}:normalize=0:duration=longest,atrim=0:{tot:.3f}[aout]")
  fin=f"{out}/expl-{names[v]}-pt.mp4"
  subprocess.run(["ffmpeg","-loglevel","error","-y","-i",f"out/{v}/vid.mp4",*ins,"-filter_complex",";".join(flt),"-map","0:v","-map","[aout]","-c:v","copy","-c:a","aac","-b:a","128k","-shortest","-movflags","+faststart",fin],check=True)
  subprocess.run(["ffmpeg","-loglevel","error","-y","-ss",str(round(ds[0]+0.9,2)),"-i",fin,"-frames:v","1","-q:v","3",f"{out}/expl-{names[v]}-poster.jpg"],check=True)
  print(fin,round(tot,1),os.path.getsize(fin)//1024,"KB")
