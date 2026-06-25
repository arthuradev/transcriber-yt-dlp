; Inno Setup script for Transcriber.
; Build the exe first (scripts\build_exe.ps1), then:  ISCC scripts\installer.iss
; Bundles only the portable exe — never .env, config, history, logs, or downloads.

#define AppVersion "0.20.0"

[Setup]
AppName=Transcriber
AppVersion={#AppVersion}
AppPublisher=Arthur Alberto
DefaultDirName={autopf}\Transcriber
DefaultGroupName=Transcriber
DisableProgramGroupPage=yes
OutputDir=..\dist
OutputBaseFilename=Transcriber-Setup-{#AppVersion}
Compression=lzma
SolidCompression=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayName=Transcriber

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "..\dist\Transcriber.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Transcriber"; Filename: "{app}\Transcriber.exe"
Name: "{group}\Uninstall Transcriber"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\Transcriber.exe"; Description: "Launch Transcriber"; Flags: nowait postinstall skipifsilent
