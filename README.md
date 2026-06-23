# Transcriber

> Beautiful Windows terminal TUI for media downloads, GPU-only transcription, transcript cleanup, and organized output.

> Interface bonita para Windows no terminal: download de mídia, transcrição com GPU, limpeza de transcrições e organização de arquivos.

## English

**Transcriber** is a Windows-only terminal TUI application designed to make media downloads and transcription workflows simple, safe, and visually pleasant.

It uses a clean terminal interface, keyboard navigation, startup animation, configurable weather/status display, yt-dlp for media extraction/download, faster-whisper for GPU-only transcription, and optional LLM-powered transcript formatting.

### Status
This repository is developed phase-by-phase. Each phase is tagged as `v0.x.0`. Version `v1.0.0` will only be created when explicitly approved by the project owner.

### Main goals
- Beautiful terminal TUI built with Rich, Questionary, and Pyfiglet.
- Windows-only user experience.
- Download supported media URLs using yt-dlp.
- Support single URLs, playlists, and batch `.txt` files.
- GPU-only transcription with faster-whisper.
- Optional transcript cleanup through DeepSeek or OpenAI-compatible providers.
- Safe dry-run first execution model.
- User-configurable output folders, language, weather, themes, and providers.
- Public repository without personal secrets or local configuration.

### Non-goals
- This is not a piracy tool.
- This is not a bypass tool for private/paywalled content.
- This is not cross-platform yet.
- This is not a GUI desktop app yet.
- This does not use CPU fallback for transcription.

## Português

**Transcriber** é uma aplicação TUI para Windows executada no terminal. Ela foi pensada para baixar mídia, transcrever áudio/vídeo, limpar a formatação de transcrições e organizar arquivos de forma bonita, segura e configurável.

O projeto usa uma interface limpa no terminal, navegação com setas do teclado, animação inicial, clima/horário configurável, yt-dlp para download, faster-whisper para transcrição com GPU e integração opcional com LLM para formatar transcrições.

### Estado
O projeto é desenvolvido por fases. Cada fase recebe uma tag `v0.x.0`. A versão `v1.0.0` só será criada quando o dono do projeto decidir explicitamente.

### Objetivos principais
- Interface terminal bonita com Rich, Questionary e Pyfiglet.
- Experiência Windows-only.
- Download de URLs suportadas pelo yt-dlp.
- Suporte a URL única, playlists e arquivos `.txt` com múltiplas URLs.
- Transcrição GPU-only com faster-whisper.
- Limpeza opcional de transcrições com DeepSeek ou provedores compatíveis com OpenAI API.
- Modelo seguro com dry-run antes de executar.
- Configuração de idioma, clima, pastas, temas e provedores.
- Repositório público sem dados pessoais, tokens, cookies ou configs locais.

## Responsible use / Uso responsável
Users are responsible for complying with copyright, platform terms, privacy expectations, and local laws. This project should be used only with content the user has the right to access and process.

Usuários são responsáveis por respeitar direitos autorais, termos das plataformas, privacidade e leis locais. Use apenas com conteúdo que você tem direito de acessar e processar.

## Development
Read these files before contributing or using an AI coding agent:

1. `AGENTS.md`
2. `CLAUDE.md`
3. `SDD.md`
4. `GSD.md`
5. `ARCHITECTURE.md`
6. `ARCHITECTURE_CONSTITUTION.md`
7. `docs/adr/`
8. `ROADMAP.md`
9. `TASKS.md`

## License
Apache-2.0.
