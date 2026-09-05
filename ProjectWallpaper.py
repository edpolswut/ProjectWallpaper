import os
import win32com.client
import win32gui
import win32ui
import win32con
from PIL import Image
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PASTA_ATALHOS = "C:/WallpaperShortcuts"

if not os.path.exists(PASTA_ATALHOS):
    os.makedirs(PASTA_ATALHOS)

app.mount("/icones", StaticFiles(directory=PASTA_ATALHOS), name="icones")

@app.get("/atalhos")
def listar_atalhos():
    atalhos = []
    arquivos = os.listdir(PASTA_ATALHOS)
    
    for arquivo in arquivos:
        if arquivo.endswith(".lnk"):
            nome_base = arquivo.replace(".lnk", "")
            caminho_lnk = os.path.join(PASTA_ATALHOS, arquivo)
            caminho_png = os.path.join(PASTA_ATALHOS, f"{nome_base}.png")
            
            if f"{nome_base}.png" not in arquivos:
                sucesso = extrair_icone_para_png(caminho_lnk, caminho_png)
                icone_url = f"http://localhost:60001/icones/{nome_base}.png" if sucesso else None
            else:
                icone_url = f"http://localhost:60001/icones/{nome_base}.png"
            
            atalhos.append({
                "id": nome_base,
                "nome": nome_base.replace("_", " "),
                "icone_url": icone_url
            })
            
    return atalhos

def extrair_icone_para_png(caminho_lnk: str, caminho_png_saida: str):
    
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        atalho = shell.CreateShortCut(caminho_lnk)
        
        alvo = atalho.TargetPath
        local_icone = atalho.IconLocation
        caminho_icone = alvo
        indice_icone = 0
        
        if local_icone and "," in local_icone:
            partes = local_icone.split(",")
            if len(partes) == 2 and partes[0].strip():
                caminho_icone = partes[0].strip()
                indice_icone = int(partes[1].strip())

        if not caminho_icone or not os.path.exists(caminho_icone):
            return False

        large, small = win32gui.ExtractIconEx(caminho_icone, indice_icone)
        if not large:
            return False

        hicon = large[0]
        
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, 32, 32)
        
        hdc_mem = hdc.CreateCompatibleDC()
        hdc_mem.SelectObject(hbmp)
        
        win32gui.DrawIconEx(hdc_mem.GetSafeHdc(), 0, 0, hicon, 32, 32, 0, None, win32con.DI_NORMAL)
        
        bmpinfo = hbmp.GetInfo()
        bmpstr = hbmp.GetBitmapBits(True)
        img = Image.frombuffer(
            'RGBA',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRA', 0, 1
        )
        
        # 1. Separa os canais da imagem (Red, Green, Blue, Alpha)
        r, g, b, alpha = img.split()
        
        # 2. Converte a imagem base para Tons de Cinza
        img_cinza = img.convert('L')
        
        # 3. Junta a imagem cinza com a transparência original
        img_final = Image.merge('LA', (img_cinza, alpha))
        
        img_final.save(caminho_png_saida, 'PNG')
        
        win32gui.DestroyIcon(large[0])
        if small: win32gui.DestroyIcon(small[0])
        
        return True
    except Exception as e:
        print(f"Erro ao extrair ícone de {caminho_lnk}: {e}")
        return False

@app.post("/executar/{app_id}")
def executar_app(app_id: str):
    caminho_atalho = os.path.join(PASTA_ATALHOS, f"{app_id}.lnk")
    if os.path.exists(caminho_atalho):
        os.startfile(caminho_atalho)
        return {"status": "sucesso", "mensagem": f"Abrindo {app_id}"}
    
    return {"status": "erro", "mensagem": "Atalho não encontrado"}

if __name__ == "__main__":
    import uvicorn
    import sys
    
    caminho_log = os.path.join(PASTA_ATALHOS, "wallpaper_api.log")
    
    sys.stdout = open(caminho_log, "a", encoding="utf-8")
    sys.stderr = sys.stdout
    
    uvicorn.run(app, host="127.0.0.1", port=60001)