import numpy as np, wave
SR=44100; TOTAL=143.0; N=int(SR*TOTAL); BPM=120; BEAT=60/BPM; BAR=4*BEAT
rng=np.random.default_rng(7)
L=np.zeros(N); R=np.zeros(N); REV=np.zeros(N)
def mf(m): return 440*2**((m-69)/12)
def add(sig,t,gain=1.0,pan=0.0,rev=0.0):
    i=int(t*SR); 
    if i>=N: return
    s=sig[:N-i]*gain; l=np.cos((pan+1)*np.pi/4); r=np.sin((pan+1)*np.pi/4)
    L[i:i+len(s)]+=s*l*1.414; R[i:i+len(s)]+=s*r*1.414; REV[i:i+len(s)]+=s*rev
def env(n,a,d_rate=None,rel=None,sustain_len=None):
    t=np.arange(n)/SR; e=np.minimum(1,t/max(a,1e-4))
    if d_rate: e*=np.exp(-t*d_rate)
    if rel: 
        k=int(rel*SR); e[-k:]*=np.linspace(1,0,k)
    return e
def pluck(f,dur=0.6,bright=1.0):
    n=int(dur*SR); t=np.arange(n)/SR; s=np.zeros(n)
    for k in range(1,8): s+=(1/k**1.4)*np.sin(2*np.pi*k*f*t)*np.exp(-t*(4+k*2.5/bright))
    return s*env(n,.003,rel=.05)
def bell(f,dur=1.6):
    n=int(dur*SR); t=np.arange(n)/SR
    s=np.sin(2*np.pi*f*t)*np.exp(-t*2.2)+.35*np.sin(2*np.pi*2.756*f*t)*np.exp(-t*4.5)+.15*np.sin(2*np.pi*5.4*f*t)*np.exp(-t*8)+.25*np.sin(2*np.pi*2*f*t)*np.exp(-t*3)
    return s*env(n,.002,rel=.1)
def pad(freqs,dur,att=.6,rel=.8):
    n=int(dur*SR); t=np.arange(n)/SR; s=np.zeros(n)
    for f in freqs:
        for det in (-0.08,0,0.08):
            ff=f*2**(det/12)
            for k in range(1,9): s+=(1/k**1.6)*np.sin(2*np.pi*k*ff*t+rng.random()*6.28)
    s/= (len(freqs)*3)
    s*=1+.15*np.sin(2*np.pi*.25*t)
    return s*env(n,att,rel=rel)
def bass(f,dur):
    n=int(dur*SR); t=np.arange(n)/SR
    s=np.sin(2*np.pi*f*t)+.35*np.sin(2*np.pi*2*f*t)+.1*np.sin(2*np.pi*3*f*t)
    return np.tanh(1.5*s)*env(n,.005,d_rate=2.5,rel=.03)
def kick():
    n=int(.35*SR); t=np.arange(n)/SR; ph=2*np.pi*np.cumsum(45+95*np.exp(-t*28))/SR
    return np.sin(ph)*np.exp(-t*9)*1.0 + 0.3*rng.standard_normal(n)*np.exp(-t*300)
def noise_hp(n,a=0.97):
    x=rng.standard_normal(n); y=np.empty(n); y[0]=x[0]
    y[1:]=x[1:]-a*x[:-1]; return y
def hat(open_=False):
    n=int((.25 if open_ else .06)*SR); t=np.arange(n)/SR
    return noise_hp(n,.99)*np.exp(-t*(14 if open_ else 70))*.5
def clap():
    n=int(.3*SR); t=np.arange(n)/SR; x=noise_hp(n,.6)
    e=np.exp(-t*18)*(1+.6*np.sin(2*np.pi*90*t).clip(0))
    return x*e*.6
def lp(x,a):  # one-pole lowpass
    y=np.empty_like(x); acc=0.0
    # vectorised via lfilter-like recursion using cumulative trick is complex; chunked python loop is fine for short signals
    for i in range(len(x)): acc+=a*(x[i]-acc); y[i]=acc
    return y
def whoosh(dur=.8,up=True):
    n=int(dur*SR); t=np.arange(n)/SR; x=rng.standard_normal(n)
    # crude sweeping bandpass: mix of differently smoothed noise
    k=np.linspace(0,1,n) if up else np.linspace(1,0,n)
    lo=np.convolve(x,np.ones(40)/40,'same'); hi=x-np.convolve(x,np.ones(6)/6,'same')
    s=(1-k)*lo*3+k*hi
    e=np.sin(np.pi*np.linspace(0,1,n))**2
    return s*e*.35
def riser(dur):
    n=int(dur*SR); k=np.linspace(0,1,n); x=noise_hp(n,.9)
    t=np.arange(n)/SR; tone=np.sin(2*np.pi*np.cumsum(200+1400*k**2)/SR)*.15
    return (x*.25+tone)*k**2.5
def pop(f=900):
    n=int(.12*SR); t=np.arange(n)/SR; ph=2*np.pi*np.cumsum(f+700*t/.12)/SR
    return np.sin(ph)*np.exp(-t*35)*.5

# progression D A Bm G
CH=[(62,66,69,74),(61,64,69,73),(62,66,71,74),(62,67,71,74)]
BS=[38,33,35,31]
MEL=[(0,74,1),(1,76,1),(2,78,1.5),(3.5,81,.5),(4,76,2),(6.5,73,.5),(7,76,1),(8,78,1),(9,74,1),(10,78,1),(11,81,1),(12,79,1.5),(13.5,78,.5),(14,76,1),(15,74,1)]
nbars=int(np.ceil(TOTAL/BAR))
def section(b):
    t=b*BAR
    if b<5: return 'intro'
    if b<49: return 'main'
    if b<59: return 'break'
    if b<67: return 'final'
    return 'outro'
melody_bars=set(list(range(21,29))+list(range(37,45))+list(range(59,67)))
side=np.ones(N)
for b in range(nbars):
    t0=b*BAR; sec=section(b); c=CH[b%4]; root=BS[b%4]
    if t0>=TOTAL: break
    # pad
    pg={'intro':.18,'main':.13,'break':.2,'final':.14,'outro':.18}[sec]
    add(pad([mf(m-12) for m in c[:3]],BAR+.9,att=.4 if sec!='intro' else 1.2),t0,pg,0,.5)
    # arp pluck (8ths; 16ths in final)
    if not (sec=='intro' and b==0):
        step=BEAT/2 if sec!='final' else BEAT/4
        pat=[0,1,2,3,2,1,2,3] if sec!='final' else [0,1,2,3,2,3,1,2,0,2,1,3,2,1,3,2]
        ag={'intro':.16,'main':.14,'break':.12,'final':.12,'outro':.12}[sec]
        for i,pi in enumerate(pat):
            tt=t0+i*step
            if sec=='outro' and b>=70: break
            add(pluck(mf(c[pi]+12),.5),tt,ag*(1 if i%2==0 else .75),(-.35 if i%2 else .35),.35)
    # drums + bass
    if sec in('main','final'):
        for q in range(4):
            tb=t0+q*BEAT
            add(kick(),tb,.55,0,0)
            i=int(tb*SR); k=int(.25*SR); 
            if i+k<N: side[i:i+k]=np.minimum(side[i:i+k],1-.45*np.exp(-np.arange(k)/SR*14))
            add(hat(),tb+BEAT/2,.22,.3,.05)
            add(hat(),tb+BEAT/4*3,.08,-.3,.02) if sec=='final' else None
            if q in(1,3): add(clap(),tb,.32,0,.3)
            # bass on 8ths with rhythm
        for (o,dur) in [(0,.45),(1,.2),(1.5,.45),(2.5,.2),(3,.45),(3.5,.4)]:
            add(bass(mf(root),dur),t0+o*BEAT,.30,0,0)
        if b%8==7: add(hat(True),t0+3.5*BEAT,.18,.2,.2)
    if sec=='intro' and b>=3:
        for q in range(8): add(hat(),t0+q*BEAT/2,.12,.3,.05)
    if sec=='break':
        add(bass(mf(root),BAR*.9)*np.linspace(1,.3,int(BAR*.9*SR)),t0,.18,0,0)
    if sec=='outro' and b<71:
        add(bass(mf(root),BAR*.9)*np.linspace(1,.3,int(BAR*.9*SR)),t0,.15,0,0)
    # melody
    if b in melody_bars:
        mb=(b-min(x for x in melody_bars if x<=b and (x-min(melody_bars))%1==0))%4
        base=b-(b%4)
        if b%4==0:
            for (o,m,d) in MEL: add(bell(mf(m),1.6),base*BAR+o*BEAT,.16,.15,.5)
# risers & final hit
add(riser(BAR*1.0),4*BAR,.35,0,.2); add(riser(BAR),58*BAR,.35,0,.2)
for tb in (5*BAR,59*BAR): add(bell(mf(62),3),tb,.18,0,.6); add(kick(),tb,.3)
add(pad([mf(m-12) for m in (62,66,69,74)],6,att=.3,rel=3),137.0,.2,0,.8)
add(bell(mf(74),4),137.0,.18,0,.8); add(bell(mf(78),4),137.1,.12,.2,.8); add(bell(mf(81),4),137.2,.1,-.2,.8)
# sfx
starts=[0,10,20,31,41,51,61,72,81,91,98,106,118,126,134]
for s in starts[1:]: add(whoosh(.7),s-.45,.35,0,.2)
for s in starts[1:10]: add(pop(900),s+.65,.18,0,.2); add(pop(1300),s+1.85,.08,0,.2)
# apply sidechain to everything except drums? (approx: whole mix, gentle)
L*=side**.6; R*=side**.6
# reverb
IRn=int(2.2*SR); t=np.arange(IRn)/SR; ir=rng.standard_normal((2,IRn))*np.exp(-t*3.2); ir[:, :int(.02*SR)]*=np.linspace(0,1,int(.02*SR))
def conv(x,h):
    n=len(x)+len(h)-1; nf=1<<(n-1).bit_length()
    return np.fft.irfft(np.fft.rfft(x,nf)*np.fft.rfft(h,nf),nf)[:len(x)]
RL=conv(REV,ir[0]); RR=conv(REV,ir[1]); sc=.06
L+=RL*sc; R+=RR*sc
mix=np.stack([L,R],1)
# fades
fi=int(.5*SR); fo=int(5*SR); mix[:fi]*=np.linspace(0,1,fi)[:,None]; mix[-fo:]*=np.linspace(1,0,fo)[:,None]**1.5
mix=np.tanh(mix/np.max(np.abs(mix))*1.3)
mix=mix/np.max(np.abs(mix))*0.89
w=wave.open('music.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix*32767).astype('<i2').tobytes()); w.close(); print('ok', mix.shape)
