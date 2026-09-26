import ctypes, wave, sys, numpy as np, espeakng_loader as E
lib=ctypes.CDLL(E.get_library_path())
sr=lib.espeak_Initialize(1,500,E.get_data_path().encode(),0)
buf=[]
CB=ctypes.CFUNCTYPE(ctypes.c_int,ctypes.POINTER(ctypes.c_short),ctypes.c_int,ctypes.c_void_p)
@CB
def cb(wav,n,ev):
    if n>0: buf.append(np.ctypeslib.as_array(wav,(n,)).copy())
    return 0
lib.espeak_SetSynthCallback(cb)
def synth(text,out,voice='ms+f3',rate=150,pitch=55):
    buf.clear(); lib.espeak_SetVoiceByName(voice.encode())
    lib.espeak_SetParameter(1,rate,0); lib.espeak_SetParameter(3,pitch,0); lib.espeak_SetParameter(4,40,0)
    t=text.encode('utf-8'); lib.espeak_Synth(t,len(t)+1,0,0,0,0x1000,None,None); lib.espeak_Synchronize()
    x=np.concatenate(buf) if buf else np.zeros(1,np.int16)
    w=wave.open(out,'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(x.tobytes()); w.close()
    return len(x)/sr
if __name__=='__main__': print(synth(sys.argv[1],sys.argv[2]), sr)
