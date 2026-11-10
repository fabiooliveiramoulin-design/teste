import json,subprocess,os,sys
v,lang=sys.argv[1],sys.argv[2]
D=json.load(open(f"durations_{lang}.json"));M="/mnt/user-data/uploads/Downloads/hfv_musica.mp3"
names={"v6":"energia","v7":"valor"}; out="/home/claude/teste/helpfarm/video"; ds=D[v]; vd=f"out/{v}_{lang}"
n=len(ds); open(f"{vd}/list.txt","w").write("".join(f"file 's{i}.mp4'\n" for i in range(n)))
subprocess.run(["ffmpeg","-loglevel","error","-y","-f","concat","-safe","0","-i",f"{vd}/list.txt","-c","copy",f"{vd}/vid.mp4"],check=True)
tot=sum(d+1.25 for d in ds); ins=[];flt=[];t=0
for i,d in enumerate(ds):
    ins+=["-i",f"aud/hfx_{lang}_{v}-{i+1}.mp3"];ms=int((t+0.35)*1000)
    flt.append(f"[{i+1}:a]aresample=48000,adelay={ms}|{ms},apad[a{i}]");t+=d+1.25
ins+=["-stream_loop","-1","-i",M]
flt.append(f"[{n+1}:a]aresample=48000,volume=0.08,afade=t=in:d=1,afade=t=out:st={tot-2:.2f}:d=2[m]")
flt.append("".join(f"[a{i}]" for i in range(n))+f"[m]amix=inputs={n+1}:normalize=0:duration=longest,atrim=0:{tot:.3f}[aout]")
fin=f"{out}/expl-{names[v]}-{lang}.mp4"
subprocess.run(["ffmpeg","-loglevel","error","-y","-i",f"{vd}/vid.mp4",*ins,"-filter_complex",";".join(flt),"-map","0:v","-map","[aout]","-c:v","copy","-c:a","aac","-b:a","128k","-shortest","-movflags","+faststart",fin],check=True)
subprocess.run(["ffmpeg","-loglevel","error","-y","-ss",str(round(ds[0]+0.9,2)),"-i",fin,"-frames:v","1","-q:v","3",f"{out}/expl-{names[v]}-{lang}-poster.jpg"],check=True)
print(fin,round(tot,1),os.path.getsize(fin)//1024,"KB")
