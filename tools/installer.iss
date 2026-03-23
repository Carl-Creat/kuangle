; 旷了吗 - Inno Setup 安装脚本
; 使用 Inno Setup 编译器打开此文件，生成 Windows 安装程序
; 下载 Inno Setup: https://jrsoftware.org/isinfo.php

#define MyAppName "旷了吗"
#define MyAppVersion "1.0"
#define MyAppPublisher "kuangle"
#define MyAppURL "https://github.com/Carl-Creat/kuangle"
#define MyAppExeName "app.py"

[Setup]
; 注意: AppId 在同一台机器上必须唯一
AppId={{8F2C4E3D-A1B5-4C6D-9E0F-1A2B3C4D5E6F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=
OutputDir=installer
OutputBaseFilename=kuangle-{#MyAppVersion}-setup
SetupIconFile=
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
ArchitecturesInstallIn64BitMode=x64

; 安装向导页面
WizardImageFile=
WizardSmallImageFile=

[Languages]
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; 注意: 以下路径需要先运行 pyinstaller 生成 dist/kuangle/ 后使用
; pyinstaller kuangle.spec
Source: "dist\kuangle\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; 如果用源码运行模式
; Source: "app.py"; DestDir: "{app}"; Flags: ignoreversion
; Source: "templates\*"; DestDir: "{app}\templates"; Flags: ignoreversion recursesubdirs createallsubdirs
; Source: "services\*"; DestDir: "{app}\services"; Flags: ignoreversion recursesubdirs createallsubdirs
; Source: "data\*"; DestDir: "{app}\data"; Flags: ignoreversion recursesubdirs createallsubdirs; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\dist\kuangle\app.exe"; WorkingDir: "{app}\dist\kuangle"; Comment: "学生安全签到工具"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\dist\kuangle\app.exe"; WorkingDir: "{app}\dist\kuangle"; Comment: "学生安全签到工具"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\dist\kuangle\app.exe"; WorkingDir: "{app}\dist\kuangle"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\dist\kuangle\启动旷了吗.bat"; Description: "启动程序"; Flags: nowait postinstall skipifsilent

[Registry]
; 可选：将 URL 协议注册到系统，实现浏览器直接打开 App
Root: HKCU; Subkey: "Software\Classes\kuangle"; ValueType: string; ValueName: ""; ValueData: "URL:旷了吗 Protocol"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\kuangle"; ValueType: string; ValueName: "URL Protocol"; ValueData: ""
Root: HKCU; Subkey: "Software\Classes\kuangle\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\dist\kuangle\app.exe"" ""%1"""

[Code]
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;
  // 检查 Python 是否安装
  if not FileExists(ExpandConstant('{pf}\Python*\python.exe')) and
     not FileExists(ExpandConstant('{userappdata}\Python*\python.exe')) then
  begin
    if MsgBox('检测到您未安装 Python 3.9+。' + #13#10 +
              '旷了吗需要 Python 才能运行。' + #13#10 + #13#10 +
              '是否现在前往 Python 官网下载？',
              mbConfirmation, MB_YESNO) = IDYES then
    begin
      ShellExec('open', 'https://www.python.org/downloads/', '', '', SW_SHOW, ewNoWait, ResultCode);
    end;
    Result := False;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  PythonExe: String;
begin
  if CurStep = ssPostInstall then
  begin
    // 安装完成后自动运行
    // （可选：引导用户完成初始设置）
  end;
end;
