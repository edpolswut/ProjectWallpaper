# 🖥️ ProjectWallpaper
**ProjectWallpaper** é um papel de parede interativo e funcional para o **Wallpaper Engine**, acompanhado por uma API local em **Python**. O projeto transforma sua área de trabalho permitindo customizar atalhos e lançar aplicativos diretamente do wallpaper, acompanhar informações meteorológicas e astronômicas, além de interagir com um visualizador de áudio reativo à sua música.

---

## ✨ Principais Recursos

- 🕒 **Relógio Digital & Painel de Informações**
- 🌤️ **Previsão do Tempo Dinâmica**
- 🌙 **Fase da Lua Calculada**
- 🎵 **Visualizador de Áudio Reativo**
- 🚀 **Iniciador de Aplicativos**:
  - Servidor backend em FastAPI que lê atalhos (`.lnk`) de uma pasta dedicada (`C:\WallpaperShortcuts`).
  - Extração automática dos ícones dos atalhos `.lnk` com conversão para PNG estilizado.
  - Execução de aplicações com um clique na área do atalho.
- 🎛️ **Modo Edição e Layout Drag & Drop**:
  - Alterne entre o modo **Travado** e **Editando**.
  - Arraste e solte ícones livremente entre 4 zonas de atalho estratégicas distribuídas na tela.

---

## 🛠️ Tecnologias Utilizadas

### Frontend (Wallpaper Engine)
- **HTML5 & CSS3**: Design minimalista em *Dark Mode*, efeitos de *glassmorphism* (`backdrop-filter`), animações e transições suaves.
- **JavaScript (ES6+)**: Manipulação de DOM, chamadas assíncronas via `fetch`, gerenciamento de eventos de drag & drop e suporte ao `localStorage`.
- **HTML5 Canvas API**: Renderização e animação das barras de áudio em tempo real.
- **Phosphor Icons**: Iconografia moderna para relógio, clima, lua e controles.
- **Wallpaper Engine Web API**: Leitura dos dados do espectro de áudio do sistema (`window.wallpaperRegisterAudioListener`).

### Backend (API Local Python)
- **Python 3.8**
- **FastAPI**: Framework web leve e de alta performance para criação dos endpoints `/atalhos` e `/executar/{app_id}`.
- **Uvicorn**: Servidor ASGI para rodar a aplicação FastAPI na porta `60001`.
- **PyWin32 (`win32com`, `win32gui`, `win32ui`)**: Manipulação da API do Windows Shell para extração de ícones nativos de arquivos `.lnk` e `.exe`.
- **Pillow (PIL)**: Processamento e tratamento de imagens (conversão para tons de cinza mantendo canal Alpha/transparência).

---

## ⚙️ Pré-requisitos

1. **Sistema Operacional**: Windows 10 ou 11 (necessário para extração nativa de ícones e inicialização de arquivos `.lnk`).
2. **Python 3.8+** instalado no sistema.
3. **Wallpaper Engine** instalado via Steam.

---

## 🚀 Passo a Passo de Instalação e Configuração

### 1. Preparar a Pasta de Atalhos
O servidor busca atalhos na pasta padrão `C:\WallpaperShortcuts`.
- Crie a pasta em seu computador: `C:\WallpaperShortcuts`
- Cole os atalhos (`.lnk`) dos programas ou jogos que você deseja acessar pelo papel de parede dentro desta pasta.
  > *Exemplo: Cole o atalho do `VS Code.lnk`, `Discord.lnk`, `Steam.lnk`.*

### 2. Instalar Dependências do Python
Abra o terminal ou Prompt de Comando e instale as bibliotecas necessárias:

```bash
pip install fastapi uvicorn pywin32 pillow
```

### 3. Executar a API em Python
Execute o arquivo `ProjectWallpaper.py`:

```bash
python ProjectWallpaper.py
```

A API iniciará e ficará escutando em `http://127.0.0.1:60001`.
> **Dica**: Para que o papel de parede abra os programas automaticamente sempre que você ligar o computador, você pode configurar o `ProjectWallpaper.py` para ser executado na inicialização do Windows (adicionando um atalho na pasta `Shell:startup` ou via Agendador de Tarefas).

### 4. Configurar no Wallpaper Engine
1. Abra o **Wallpaper Engine**.
2. Clique em **Criar Wallpaper** (*Create Wallpaper*) no canto inferior esquerdo.
3. Escolha **Criar Web Wallpaper** (*Use Web Browser* / *HTML*).
4. Selecione o arquivo `ProjectWallpaper.html`.
5. Salve e aplique o wallpaper na sua área de trabalho.

---

## 📖 Como Usar

1. **Abrir Aplicativos**: Basta clicar sobre o ícone do aplicativo na tela. A API enviará um comando para o Windows executar o programa associado.
2. **Modo Edição (Drag & Drop)**:
   - Clique no botão **Travado** no canto inferior direito para alterar para **Editando**.
   - Arraste os ícones e solte-os em qualquer uma das 4 zonas disponíveis na tela (Top Left, Top Right, Bottom Right, Bottom Left).
   - Ao finalizar, clique novamente no botão para travar os ícones na posição desejada. A nova distribuição será memorizada automaticamente.
3. **Recarregar Atalhos**:
   - Caso adicione ou remova atalhos na pasta `C:\WallpaperShortcuts`, clique no botão **Refresh** para atualizar a lista na tela sem precisar reiniciar o Wallpaper Engine.

## 📝 Licença

Sinta-se à vontade para modificar e adaptar este projeto para o seu próprio setup!
