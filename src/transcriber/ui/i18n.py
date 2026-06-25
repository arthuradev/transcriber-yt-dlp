"""Minimal internationalization.

User-facing strings are looked up by key and rendered in the active language,
falling back to English and then to the key itself. Code identifiers stay
English; only displayed text is translated.
"""

from __future__ import annotations

from transcriber.config.models import Language

_CATALOG: dict[str, dict[Language, str]] = {
    "menu.prompt": {
        Language.EN_US: "Select an option:",
        Language.PT_BR: "Selecione uma opção:",
    },
    "menu.download_video": {
        Language.EN_US: "Download video",
        Language.PT_BR: "Baixar vídeo",
    },
    "menu.download_audio": {
        Language.EN_US: "Download audio",
        Language.PT_BR: "Baixar áudio",
    },
    "menu.download_transcript": {
        Language.EN_US: "Download transcript / subtitles",
        Language.PT_BR: "Baixar transcrição / legendas",
    },
    "menu.transcribe_local": {
        Language.EN_US: "Transcribe local file",
        Language.PT_BR: "Transcrever arquivo local",
    },
    "menu.clean_transcript": {
        Language.EN_US: "Clean transcript with AI",
        Language.PT_BR: "Limpar transcrição com IA",
    },
    "menu.history": {
        Language.EN_US: "History",
        Language.PT_BR: "Histórico",
    },
    "menu.settings": {
        Language.EN_US: "Settings",
        Language.PT_BR: "Configurações",
    },
    "menu.exit": {
        Language.EN_US: "Exit",
        Language.PT_BR: "Sair",
    },
    "shell.coming_soon_title": {
        Language.EN_US: "Coming soon",
        Language.PT_BR: "Em breve",
    },
    "shell.not_implemented": {
        Language.EN_US: "'{label}' is not implemented yet (coming in a later phase).",
        Language.PT_BR: "'{label}' ainda não está implementado (chega em uma fase futura).",
    },
    "shell.press_enter": {
        Language.EN_US: "Press Enter to return to the menu",
        Language.PT_BR: "Pressione Enter para voltar ao menu",
    },
    "shell.goodbye": {
        Language.EN_US: "Goodbye.",
        Language.PT_BR: "Até logo.",
    },
    "firstrun.choose_theme": {
        Language.EN_US: "Choose a theme:",
        Language.PT_BR: "Escolha um tema:",
    },
    "firstrun.weather_enable": {
        Language.EN_US: "Show weather on startup?",
        Language.PT_BR: "Mostrar clima ao iniciar?",
    },
    "firstrun.weather_city": {
        Language.EN_US: "Weather city (e.g. London):",
        Language.PT_BR: "Cidade do clima (ex.: São Paulo):",
    },
    "firstrun.output_dir": {
        Language.EN_US: "Output folder:",
        Language.PT_BR: "Pasta de saída:",
    },
    "firstrun.llm_enable": {
        Language.EN_US: "Enable optional AI transcript cleanup?",
        Language.PT_BR: "Ativar limpeza opcional de transcrição com IA?",
    },
    "firstrun.gpu_ack": {
        Language.EN_US: "Transcription is GPU-only (no CPU fallback). Continue?",
        Language.PT_BR: "A transcrição é apenas por GPU (sem CPU). Continuar?",
    },
    "firstrun.done": {
        Language.EN_US: "Setup complete.",
        Language.PT_BR: "Configuração concluída.",
    },
    "weather.unavailable": {
        Language.EN_US: "Weather unavailable",
        Language.PT_BR: "Clima indisponível",
    },
    "media.metadata_title": {
        Language.EN_US: "Media metadata",
        Language.PT_BR: "Metadados da mídia",
    },
    "media.title": {
        Language.EN_US: "Title",
        Language.PT_BR: "Título",
    },
    "media.site": {
        Language.EN_US: "Site",
        Language.PT_BR: "Site",
    },
    "media.duration": {
        Language.EN_US: "Duration",
        Language.PT_BR: "Duração",
    },
    "media.uploader": {
        Language.EN_US: "Uploader",
        Language.PT_BR: "Autor",
    },
    "media.url": {
        Language.EN_US: "URL",
        Language.PT_BR: "URL",
    },
    "media.formats": {
        Language.EN_US: "Formats",
        Language.PT_BR: "Formatos",
    },
    "media.playlist": {
        Language.EN_US: "Playlist",
        Language.PT_BR: "Playlist",
    },
    "media.items": {
        Language.EN_US: "Items",
        Language.PT_BR: "Itens",
    },
    "media.more_formats": {
        Language.EN_US: "... and {count} more format(s)",
        Language.PT_BR: "... e mais {count} formato(s)",
    },
    "media.more_items": {
        Language.EN_US: "... and {count} more item(s)",
        Language.PT_BR: "... e mais {count} item(ns)",
    },
    "plan.title": {
        Language.EN_US: "Dry run (no download yet)",
        Language.PT_BR: "Simulação (ainda sem download)",
    },
    "plan.profile": {
        Language.EN_US: "Profile",
        Language.PT_BR: "Perfil",
    },
    "plan.format": {
        Language.EN_US: "Format",
        Language.PT_BR: "Formato",
    },
    "plan.output": {
        Language.EN_US: "Output folder",
        Language.PT_BR: "Pasta de saída",
    },
    "plan.items": {
        Language.EN_US: "Items",
        Language.PT_BR: "Itens",
    },
    "plan.risk": {
        Language.EN_US: "Risk",
        Language.PT_BR: "Risco",
    },
    "plan.warnings": {
        Language.EN_US: "Warnings",
        Language.PT_BR: "Avisos",
    },
    "plan.confirm": {
        Language.EN_US: "Proceed with this plan?",
        Language.PT_BR: "Prosseguir com este plano?",
    },
    "plan.confirm_strong": {
        Language.EN_US: "This is a high-risk operation. Type the confirmation to proceed.",
        Language.PT_BR: "Operação de alto risco. Digite a confirmação para prosseguir.",
    },
    "plan.cancelled": {
        Language.EN_US: "Cancelled.",
        Language.PT_BR: "Cancelado.",
    },
    "plan.execution_later": {
        Language.EN_US: "Execution will be available in a later phase.",
        Language.PT_BR: "A execução estará disponível em uma fase futura.",
    },
    "plan.enter_url": {
        Language.EN_US: "Paste a URL:",
        Language.PT_BR: "Cole uma URL:",
    },
    "plan.select_profile": {
        Language.EN_US: "Select a profile:",
        Language.PT_BR: "Selecione um perfil:",
    },
    "plan.manual_format": {
        Language.EN_US: "Manual format...",
        Language.PT_BR: "Formato manual...",
    },
    "plan.select_format": {
        Language.EN_US: "Select a format:",
        Language.PT_BR: "Selecione um formato:",
    },
    "plan.probe_failed": {
        Language.EN_US: "Could not read metadata: {error}",
        Language.PT_BR: "Não foi possível ler os metadados: {error}",
    },
    "risk.low": {Language.EN_US: "low", Language.PT_BR: "baixo"},
    "risk.medium": {Language.EN_US: "medium", Language.PT_BR: "médio"},
    "risk.high": {Language.EN_US: "high", Language.PT_BR: "alto"},
    "download.downloading": {
        Language.EN_US: "Downloading",
        Language.PT_BR: "Baixando",
    },
    "download.success_title": {
        Language.EN_US: "Download complete",
        Language.PT_BR: "Download concluído",
    },
    "download.partial_title": {
        Language.EN_US: "Partly completed",
        Language.PT_BR: "Parcialmente concluído",
    },
    "download.failed_title": {
        Language.EN_US: "Download failed",
        Language.PT_BR: "Falha no download",
    },
    "download.summary": {
        Language.EN_US: "{ok} succeeded, {skipped} skipped, {failed} failed",
        Language.PT_BR: "{ok} concluído(s), {skipped} ignorado(s), {failed} com falha",
    },
    "source.prompt": {
        Language.EN_US: "What do you want to download from?",
        Language.PT_BR: "De onde você quer baixar?",
    },
    "source.single": {
        Language.EN_US: "A single URL",
        Language.PT_BR: "Uma única URL",
    },
    "source.batch": {
        Language.EN_US: "A .txt file with URLs",
        Language.PT_BR: "Um arquivo .txt com URLs",
    },
    "source.file": {
        Language.EN_US: "Path to the .txt file:",
        Language.PT_BR: "Caminho do arquivo .txt:",
    },
    "batch.found": {
        Language.EN_US: "{count} item(s) found",
        Language.PT_BR: "{count} item(ns) encontrado(s)",
    },
    "batch.none": {
        Language.EN_US: "No items could be read from the file.",
        Language.PT_BR: "Nenhum item pôde ser lido do arquivo.",
    },
    "batch.unavailable": {
        Language.EN_US: "Batch input is not available.",
        Language.PT_BR: "Entrada em lote não está disponível.",
    },
    "transcribe.enter_file": {
        Language.EN_US: "Path to the audio/video file:",
        Language.PT_BR: "Caminho do arquivo de áudio/vídeo:",
    },
    "transcribe.file_missing": {
        Language.EN_US: "File not found: {path}",
        Language.PT_BR: "Arquivo não encontrado: {path}",
    },
    "transcribe.working": {
        Language.EN_US: "Transcribing (GPU)...",
        Language.PT_BR: "Transcrevendo (GPU)...",
    },
    "transcribe.gpu_required": {
        Language.EN_US: "GPU required",
        Language.PT_BR: "GPU necessária",
    },
    "transcribe.saved": {
        Language.EN_US: "Transcript saved",
        Language.PT_BR: "Transcrição salva",
    },
    "transcribe.summary": {
        Language.EN_US: "Language: {language} | {segments} segment(s)",
        Language.PT_BR: "Idioma: {language} | {segments} segmento(s)",
    },
    "transcribe.failed": {
        Language.EN_US: "Transcription failed: {error}",
        Language.PT_BR: "Falha na transcrição: {error}",
    },
    "media.subtitles": {
        Language.EN_US: "Subtitles",
        Language.PT_BR: "Legendas",
    },
    "subtitle.select_language": {
        Language.EN_US: "Select a subtitle language:",
        Language.PT_BR: "Selecione um idioma de legenda:",
    },
    "subtitle.none": {
        Language.EN_US: "No subtitles found. Use 'Transcribe local file' instead.",
        Language.PT_BR: "Nenhuma legenda encontrada. Use 'Transcrever arquivo local'.",
    },
    "subtitle.playlist_unsupported": {
        Language.EN_US: "Subtitle download supports a single video URL.",
        Language.PT_BR: "O download de legendas suporta uma única URL de vídeo.",
    },
    "subtitle.saved": {
        Language.EN_US: "Subtitles saved",
        Language.PT_BR: "Legendas salvas",
    },
    "subtitle.failed": {
        Language.EN_US: "Subtitle download failed: {error}",
        Language.PT_BR: "Falha no download de legendas: {error}",
    },
    "subtitle.auto_suffix": {
        Language.EN_US: "{lang} (auto)",
        Language.PT_BR: "{lang} (automática)",
    },
    "cleanup.enter_file": {
        Language.EN_US: "Path to the transcript file:",
        Language.PT_BR: "Caminho do arquivo de transcrição:",
    },
    "cleanup.file_missing": {
        Language.EN_US: "File not found: {path}",
        Language.PT_BR: "Arquivo não encontrado: {path}",
    },
    "cleanup.warning": {
        Language.EN_US: "Only the transcript text is sent to the provider (not audio/video).",
        Language.PT_BR: "Apenas o texto da transcrição é enviado ao provedor (não áudio/vídeo).",
    },
    "cleanup.confirm": {
        Language.EN_US: "Send the transcript text for AI cleanup?",
        Language.PT_BR: "Enviar o texto da transcrição para limpeza por IA?",
    },
    "cleanup.no_key": {
        Language.EN_US: "Set DEEPSEEK_API_KEY or OPENAI_COMPATIBLE_API_KEY in .env first.",
        Language.PT_BR: "Defina DEEPSEEK_API_KEY ou OPENAI_COMPATIBLE_API_KEY no .env primeiro.",
    },
    "cleanup.select_profile": {
        Language.EN_US: "Select a cleanup style:",
        Language.PT_BR: "Selecione um estilo de limpeza:",
    },
    "cleanup.cancelled": {
        Language.EN_US: "Cancelled.",
        Language.PT_BR: "Cancelado.",
    },
    "cleanup.saved": {
        Language.EN_US: "Cleaned transcript saved",
        Language.PT_BR: "Transcrição limpa salva",
    },
    "cleanup.failed": {
        Language.EN_US: "Cleanup failed: {error}",
        Language.PT_BR: "Falha na limpeza: {error}",
    },
    "cookies.title": {
        Language.EN_US: "Cookies (advanced)",
        Language.PT_BR: "Cookies (avançado)",
    },
    "cookies.warning": {
        Language.EN_US: "Browser cookies will be sent to the site. Use only on sites you trust.",
        Language.PT_BR: "Cookies do navegador serão enviados ao site. Use só em sites confiáveis.",
    },
    "cookies.confirm": {
        Language.EN_US: "Use your browser cookies for this download?",
        Language.PT_BR: "Usar os cookies do navegador neste download?",
    },
    "history.title": {
        Language.EN_US: "Recent operations",
        Language.PT_BR: "Operações recentes",
    },
    "history.empty": {
        Language.EN_US: "No history yet.",
        Language.PT_BR: "Nenhum histórico ainda.",
    },
    "history.time": {
        Language.EN_US: "Time",
        Language.PT_BR: "Hora",
    },
    "history.operation": {
        Language.EN_US: "Operation",
        Language.PT_BR: "Operação",
    },
    "history.status": {
        Language.EN_US: "Status",
        Language.PT_BR: "Estado",
    },
    "settings.title": {
        Language.EN_US: "Settings",
        Language.PT_BR: "Configurações",
    },
    "settings.theme": {
        Language.EN_US: "Theme",
        Language.PT_BR: "Tema",
    },
    "settings.language": {
        Language.EN_US: "Language",
        Language.PT_BR: "Idioma",
    },
    "settings.weather": {
        Language.EN_US: "Weather",
        Language.PT_BR: "Clima",
    },
    "settings.llm": {
        Language.EN_US: "AI cleanup",
        Language.PT_BR: "Limpeza por IA",
    },
    "settings.output": {
        Language.EN_US: "Output folder",
        Language.PT_BR: "Pasta de saída",
    },
    "settings.prompt": {
        Language.EN_US: "Change a setting:",
        Language.PT_BR: "Alterar uma configuração:",
    },
    "settings.change_theme": {
        Language.EN_US: "Change theme",
        Language.PT_BR: "Alterar tema",
    },
    "settings.change_language": {
        Language.EN_US: "Change language",
        Language.PT_BR: "Alterar idioma",
    },
    "settings.back": {
        Language.EN_US: "Back",
        Language.PT_BR: "Voltar",
    },
    "settings.saved": {
        Language.EN_US: "Saved. Some changes apply after restart.",
        Language.PT_BR: "Salvo. Algumas mudanças se aplicam após reiniciar.",
    },
    "common.on": {
        Language.EN_US: "on",
        Language.PT_BR: "ligado",
    },
    "common.off": {
        Language.EN_US: "off",
        Language.PT_BR: "desligado",
    },
    "health.title": {
        Language.EN_US: "Diagnostics",
        Language.PT_BR: "Diagnóstico",
    },
    "health.check": {
        Language.EN_US: "Check",
        Language.PT_BR: "Verificação",
    },
    "health.status": {
        Language.EN_US: "Status",
        Language.PT_BR: "Estado",
    },
    "health.detail": {
        Language.EN_US: "Detail",
        Language.PT_BR: "Detalhe",
    },
    "health.ok": {
        Language.EN_US: "ok",
        Language.PT_BR: "ok",
    },
    "health.missing": {
        Language.EN_US: "missing",
        Language.PT_BR: "ausente",
    },
}


class Translator:
    """Resolves message keys to localized strings for one language."""

    def __init__(self, language: Language = Language.EN_US) -> None:
        self.language = language

    def __call__(self, key: str, /, **kwargs: object) -> str:
        entry = _CATALOG.get(key)
        if entry is None:
            return key
        template = entry.get(self.language) or entry.get(Language.EN_US) or key
        return template.format(**kwargs) if kwargs else template
