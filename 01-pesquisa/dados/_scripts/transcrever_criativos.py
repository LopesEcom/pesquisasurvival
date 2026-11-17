# Transcreve os primeiros 60 s de cada vídeo de criativo (gancho + começo do corpo) com faster-whisper (modelo small, local).
# Saída: criativos-concorrentes/transcricoes.json  {adArchiveId: {idioma, texto, gancho}}
import json, os, glob, sys, subprocess, tempfile, wave
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
from faster_whisper import WhisperModel
D = r"E:/Raio-X Survival Europa/01-pesquisa/dados/"
OUT = D + 'criativos-concorrentes/transcricoes.json'
res = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
res = {k: v for k, v in res.items() if 'erro' not in v}
try:
    m = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=2, download_root=r'E:/tmp-claude/whisper')
    MODELO = 'small'
except Exception as e:
    print('small falhou:', e, flush=True)
    m = WhisperModel('base', device='cpu', compute_type='int8', cpu_threads=2, download_root=r'E:/tmp-claude/whisper')
    MODELO = 'base'
print('modelo', MODELO, flush=True)
arqs = sorted(set(glob.glob(D + 'criativos-concorrentes/*/paginas/criativos/*.mp4') + glob.glob(D + 'biblioteca/paginas/criativos/*.mp4') + glob.glob(D + 'biblioteca/europa/paginas/criativos/*.mp4')))
print(len(arqs), 'vídeos', flush=True)
tmp = r'E:/claude-tmp/trecho.wav'
for a in arqs:
    aid = os.path.basename(a)[:-4]
    if aid in res: continue
    try:
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', a, '-t', '60', '-ac', '1', '-ar', '16000', tmp], check=True)
        w = wave.open(tmp, 'rb'); audio = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768.0; w.close()
        segs, info = m.transcribe(audio, beam_size=1, vad_filter=True)
        segs = list(segs)
        texto = ' '.join(s.text.strip() for s in segs)
        gancho = ' '.join(s.text.strip() for s in segs if s.start < 6)
        res[aid] = {'idioma': info.language, 'texto': texto, 'gancho': gancho or texto[:140]}
    except Exception as e:
        res[aid] = {'erro': str(e)[:150]}
    json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(aid, res[aid].get('idioma'), (res[aid].get('gancho') or '')[:80], flush=True)
print('FIM')
