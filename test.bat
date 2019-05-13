@echo off

echo                                        "Windows系统安全检查脚本"


 

echo "系统信息检查"

systeminfo >系统信息.log

echo "系统自动更新服务状态检查"

sc query wuauserv >系统更新.log

echo "端口信息检查"

netstat -anb >端口信息.log

echo "进程检查"

tasklist&net start >进程检查.log

echo "进程路径检查"

wmic process get name,executablepath,processid >进程路径检查.log

echo "默认共享检查"

net share >默认共享检查.log

echo "用户信息检查"

net user & net localgroup administrators >用户信息检查.log

echo "隐藏用户检查"

echo HKEY_LOCAL_MACHINE\SAM\SAM\Domains\Account\Users\Names [1 2 19]>d:\regg.ini&echo HKEY_LOCAL_MACHINE\SAM\SAM\ [1 2 19] >>d:\regg.ini & regini d:\regg.ini&reg query HKEY_LOCAL_MACHINE\SAM\SAM\Domains\Account\Users\Names >隐藏用户检查.log&del d:\regg.ini

echo "注册表启动项检查"

reg query HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run & reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run >注册表启动项检查.log

echo "安全策略检查"

secedit /export /cfg LocalGroupPolicy&type LocalGroupPolicy >安全策略检查.log

echo "IE浏览器记录检查"

reg query HKEY_CURRENT_USER\Software\Microsoft\Internet" "Explorer\TypedURLs >IE浏览器记录检查.log

echo "添加和卸载记录"

reg query HKEY_LOCAL_MACHINE\SOFTWARE\MICROSOFT\WINDOWS\CURRENTVERSION\UNINSTALL /s /v DisPlayname >添加和卸载记录.log

echo "异常状态检查"

reg query HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows" "NT\CurrentVersion\SvcHost /s /v netsvcs&reg query HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows" "NT\CurrentVersion\SvcHost /s /v LocalService >异常状态检查.log

echo "通信检查"\

netstat -a >通信检查.log

echo "CMD记录"

reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU >CMD记录.log

echo "文件记录检查"

reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths >文件记录检查.log

echo "文件记录检查2"

reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSaveMRU\* /v * >文件记录检查2.log

echo "程序记录"

reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedMRU >程序记录.log

echo "程序记录"

reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedMRU >程序记录.log

echo "C盘捆绑文件检查"

echo "正常可执行文件返回结果为1，不可执行文件结果为0，返回结果为2的，为存在捆绑内容文件。"

echo "请点击回车继续！"

set /p var=find /c /i "this program" c:\*  c:\Inetpub\*  C:\Users\Administrator\Desktop\* c:\temp\* >捆绑文件检查.log

%var%

if %ERRORLEVEL% == 0 goto yes

goto no

:yes

exit

:no

find /c /i "this program" c:\*  c:\wmpub\* c:\Inetpub\* C:\Documents and Settings\Administrator\桌面\* >捆绑文件检查.log
