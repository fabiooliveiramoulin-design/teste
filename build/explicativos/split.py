# Corta narração contínua em cenas: escolhe, para cada fronteira esperada (proporcional aos caracteres), a pausa mais próxima.
import json,subprocess,sys,re
def pauses(f,n=-38,d=0.18):
    o=subprocess.run(["ffmpeg","-i",f,"-af",f"silencedetect=noise={n}dB:d={d}","-f","null","-"],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",o)]; en=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",o)]
    return list(zip(st,en))
def dur(f): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]))
def plan(f,lines,n=-38,d=0.18,mp=0.25):
    P=pauses(f,n,d); T=dur(f); w=[len(l) for l in lines]; tot=sum(w); cuts=[]; acc=0; used=set()
    # tempo de fala útil (sem silêncio inicial/final)
    s0=P[0][1] if P and P[0][0]<0.05 else 0; s1=P[-1][0] if P and P[-1][1]>T-0.05 else T
    for i in range(len(lines)-1):
        acc+=w[i]; exp=s0+(s1-s0)*acc/tot
        cand=[(abs((a+b)/2-exp),j) for j,(a,b) in enumerate(P) if j not in used and a>s0+0.5 and b<s1-0.5 and (b-a)>=mp]
        d,j=min(cand); used.add(j); a,b=P[j]; cuts.append(((a+b)/2,round(d,2),round(b-a,2)))
    cuts.sort(); return cuts,T,s0,s1
if __name__=="__main__":
    f,lang,vid=sys.argv[1:4]; L=json.load(open("i18n.json"))["scripts"][lang][vid]
    c,T,s0,s1=plan(f,L); print(T,s0,s1); [print(x) for x in c]

def plan_auto(f,lines):
    for n,d,mp in [(-38,0.18,0.25),(-34,0.15,0.18),(-30,0.12,0.12),(-26,0.1,0.1)]:
        try:
            r=plan(f,lines,n,d,mp)
            if max(c[1] for c in r[0])<2.5: return r
        except ValueError: pass
    raise SystemExit("sem cortes: "+f)
