@echo off

echo                                        "Windowsϵͳ��ȫ���ű�"


 

echo "ϵͳ��Ϣ���"

systeminfo >ϵͳ��Ϣ.log

echo "ϵͳ�Զ����·���״̬���"

sc query wuauserv >ϵͳ����.log

echo "�˿���Ϣ���"

netstat -anb >�˿���Ϣ.log

echo "���̼��"

tasklist&net start >���̼��.log

echo "����·�����"

wmic process get name,executablepath,processid >����·�����.log

echo "Ĭ�Ϲ�����"

net share >Ĭ�Ϲ�����.log

echo "�û���Ϣ���"

net user & net localgroup administrators >�û���Ϣ���.log

echo "�����û����"

echo HKEY_LOCAL_MACHINE\SAM\SAM\Domains\Account\Users\Names [1 2 19]>d:\regg.ini&echo HKEY_LOCAL_MACHINE\SAM\SAM\ [1 2 19] >>d:\regg.ini & regini d:\regg.ini&reg query HKEY_LOCAL_MACHINE\SAM\SAM\Domains\Account\Users\Names >�����û����.log&del d:\regg.ini

echo "ע�����������"

reg query HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run & reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run >ע�����������.log

echo "��ȫ���Լ��"

secedit /export /cfg LocalGroupPolicy&type LocalGroupPolicy >��ȫ���Լ��.log

echo "IE�������¼���"

reg query HKEY_CURRENT_USER\Software\Microsoft\Internet" "Explorer\TypedURLs >IE�������¼���.log

echo "��Ӻ�ж�ؼ�¼"

reg query HKEY_LOCAL_MACHINE\SOFTWARE\MICROSOFT\WINDOWS\CURRENTVERSION\UNINSTALL /s /v DisPlayname >��Ӻ�ж�ؼ�¼.log

echo "�쳣״̬���"

reg query HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows" "NT\CurrentVersion\SvcHost /s /v netsvcs&reg query HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows" "NT\CurrentVersion\SvcHost /s /v LocalService >�쳣״̬���.log

echo "ͨ�ż��"\

netstat -a >ͨ�ż��.log

echo "CMD��¼"

reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU >CMD��¼.log

echo "�ļ���¼���"

reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths >�ļ���¼���.log

echo "�ļ���¼���2"

reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSaveMRU\* /v * >�ļ���¼���2.log

echo "�����¼"

reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedMRU >�����¼.log

echo "�����¼"

reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedMRU >�����¼.log

echo "C�������ļ����"

echo "������ִ���ļ����ؽ��Ϊ1������ִ���ļ����Ϊ0�����ؽ��Ϊ2�ģ�Ϊ�������������ļ���"

echo "�����س�������"

set /p var=find /c /i "this program" c:\*  c:\Inetpub\*  C:\Users\Administrator\Desktop\* c:\temp\* >�����ļ����.log

%var%

if %ERRORLEVEL% == 0 goto yes

goto no

:yes

exit

:no

find /c /i "this program" c:\*  c:\wmpub\* c:\Inetpub\* C:\Documents and Settings\Administrator\����\* >�����ļ����.log
