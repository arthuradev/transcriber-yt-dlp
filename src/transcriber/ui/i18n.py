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
