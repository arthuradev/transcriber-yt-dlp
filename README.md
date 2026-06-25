# Transcriber

> Beautiful Windows terminal TUI for media downloads, GPU-only transcription, transcript cleanup, and organized output.
>
> Interface bonita para Windows no terminal: download de mídia, transcrição com GPU, limpeza de transcrições e organização de arquivos.

Built with a clean Rich-based terminal UI, keyboard menus (Questionary), and a
Pyfiglet startup banner. Safe by default: every operation is planned and shown as
a dry-run before anything happens, risky actions ask for confirmation, and
secrets are never committed or logged.

---

## English

### Features
- **Download** video/audio from any [yt-dlp](https://github.com/yt-dlp/yt-dlp)-supported site — single URLs, playlists, or a `.txt` batch file.
- **Metadata first**: probe and show title, site, duration, and available formats before downloading; pick a named profile or a specific format (advanced manual mode).
- **Dry-run + risk model**: every operation shows a plan and a risk level; high-risk operations (large batches, cookies) require strong confirmation.
- **Subtitles**: download existing subtitles/captions, preferring them over local transcription.
- **GPU-only transcription** with [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (`large-v3` by default). No CPU fallback — it aborts with a helpful message if CUDA is unavailable.
- **Optional AI cleanup** of transcripts via DeepSeek or any OpenAI-compatible provider. The model may only *format* (never add facts), and it always asks before sending text.
- **Organized output**: per-site/date/playlist folders, media IDs in filenames, and a duplicate-avoidance archive.
- **History, logs, and reports**: a local SQLite history, redacted logs, and JSON reports.
- **Personalization**: dark themes (default, purple, red, blue, monochrome, anime), optional WeatherAPI line, and Portuguese/English UI.

### Requirements
- Windows 10/11 (x64). This project is Windows-only for now.
- [uv](https://docs.astral.sh/uv/) (provisions Python 3.12 automatically).
- [ffmpeg](https://ffmpeg.org/) for audio extraction and some merges (optional but recommended).
- An NVIDIA GPU + CUDA **only** if you want local transcription.

### Quickstart (development)
```powershell
git clone https://github.com/arthuradev/transcriber-yt-dlp.git
cd transcriber-yt-dlp
powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1   # checks deps, syncs, creates .env
uv run transcriber
```
On first run the app asks for your language, theme, weather preference, output
folder, and confirms the GPU-only transcription policy.

### Optional features
- **Transcription** (GPU-only): `uv sync --extra transcription` and ensure CUDA is installed.
- **AI cleanup**: put `DEEPSEEK_API_KEY` (or `OPENAI_COMPATIBLE_API_KEY`) in `.env`.
- **Weather line**: set `WEATHERAPI_KEY` in `.env` and enable weather in settings.
- **Cookies** (advanced): opt-in per the warning; cookies are never auto-enabled, committed, or logged.

Secrets live only in `.env` (gitignored) — never in the saved config.

### Usage
The main menu offers: download video, download audio, download transcript/subtitles,
transcribe a local file, clean a transcript with AI, history, settings, and exit.
Each download flow is: paste a URL (or a `.txt` of URLs) → review metadata →
choose a profile → review the dry-run → confirm → download with progress → summary.

### Build a portable exe (Windows)
```powershell
powershell -ExecutionPolicy Bypass -File scripts/build_exe.ps1 -Clean      # dist\Transcriber.exe
powershell -ExecutionPolicy Bypass -File scripts/build_installer.ps1       # Inno Setup installer (needs ISCC)
```
The exe bundles the app and ASCII assets only — never secrets or user data.

### Status
Feature-complete release candidate (`v0.20.0`). Developed phase-by-phase
(`v0.1.0` … `v0.20.0`). **`v1.0.0` will only be created when explicitly approved
by the project owner.**

---

## Português

**Transcriber** é uma aplicação TUI para Windows executada no terminal: baixa
mídia, transcreve áudio/vídeo (apenas com GPU), limpa a formatação de
transcrições e organiza arquivos — de forma bonita, segura e configurável.

### Recursos
- **Download** de vídeo/áudio de qualquer site suportado pelo yt-dlp — URL única, playlists ou arquivo `.txt` em lote.
- **Metadados primeiro**: mostra título, site, duração e formatos antes de baixar; escolha um perfil ou um formato específico (modo manual avançado).
- **Simulação (dry-run) + risco**: toda operação mostra um plano e um nível de risco; operações de alto risco exigem confirmação forte.
- **Legendas**: baixa legendas existentes, preferindo-as à transcrição local.
- **Transcrição apenas por GPU** com faster-whisper (`large-v3` por padrão). Sem CPU — aborta com instruções se não houver CUDA.
- **Limpeza opcional por IA** (DeepSeek ou provedores compatíveis com OpenAI). A IA só *formata* (nunca inventa); sempre pergunta antes de enviar o texto.
- **Saída organizada**: pastas por site/data/playlist, ID nos nomes e arquivo de duplicatas.
- **Histórico, logs e relatórios**: histórico em SQLite, logs com redação e relatórios JSON.
- **Personalização**: temas escuros, linha de clima opcional (WeatherAPI) e interface em Português/Inglês.

### Início rápido
```powershell
git clone https://github.com/arthuradev/transcriber-yt-dlp.git
cd transcriber-yt-dlp
powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1
uv run transcriber
```
Na primeira execução, o app pergunta idioma, tema, clima, pasta de saída e
confirma a política de transcrição apenas por GPU.

As chaves de API ficam apenas no `.env` (ignorado pelo git) — nunca na config salva.

### Estado
Release candidate completo (`v0.20.0`), desenvolvido por fases. A versão
`v1.0.0` só será criada quando o dono do projeto decidir explicitamente.

---

## Responsible use / Uso responsável
Users are responsible for complying with copyright, platform terms, privacy
expectations, and local laws. Use only with content you have the right to access
and process. This is not a piracy or paywall-bypass tool.

Usuários são responsáveis por respeitar direitos autorais, termos das
plataformas, privacidade e leis locais. Use apenas com conteúdo que você tem
direito de acessar e processar. Este projeto não é ferramenta de pirataria nem
para contornar conteúdo pago.

## Development
Read before contributing or using an AI coding agent: `AGENTS.md`, `CLAUDE.md`,
`SDD.md`, `GSD.md`, `ARCHITECTURE.md`, `ARCHITECTURE_CONSTITUTION.md`,
`docs/adr/`, `ROADMAP.md`, `TASKS.md`.

Quality gate:
```powershell
uv run ruff format --check .
uv run ruff check .
uv run pyright
uv run coverage run -m pytest
uv run coverage report
uv run python scripts/quality_gate.py
```

## License
Apache-2.0.
