;= @echo off
;= rem Call DOSKEY and use this file as the macrofile
;= %SystemRoot%\system32\doskey /listsize=1000 /macrofile=%0%
;= rem In batch mode, jump to the end of the file
;= goto:eof
;= Add aliases below here

e.=explorer .
e..=explorer $1

pwd=cd
clear=cls
history=cat "%CMDER_ROOT%\config\.history"
unalias=alias /d $1
vi=vim $*
setp=setx /M PATH "$1;%PATH%"

ls=ls --show-control-chars -F --color $*
ll=ls -alh --color $*
l=ls -alh --color $*


;= rem docker
dk=bash "%CMDER_ROOT%\config\docker.sh" $*

;= rem sublime
sbl="C:\Program Files\Sublime Text 3\subl.exe" $*
subl="C:\Program Files\Sublime Text 3\subl.exe" $*
seta="C:\Program Files\Sublime Text 3\subl.exe" "c:/cmder_mini/config/user-aliases.cmd"
hosts="C:\Program Files\Sublime Text 3\subl.exe" "C:\Windows\System32\drivers\etc\hosts"


;= rem dumpbin
ckbin64="C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.13.26128\bin\Hostx64\x64\dumpbin.exe" $*
ckbin86="C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.13.26128\bin\Hostx64\x86\dumpbin.exe" $*
ckbin="C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.13.26128\bin\Hostx64\x86\dumpbin.exe" $*
ckbindeps64="C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.13.26128\bin\Hostx64\x64\dumpbin.exe" /DEPENDENTS $*
ckbindeps86="C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.13.26128\bin\Hostx64\x86\dumpbin.exe" /DEPENDENTS $*
ckbindeps="C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.13.26128\bin\Hostx64\x64\dumpbin.exe" /DEPENDENTS $*

;= rem git alias
gc=git add . & git commit -m $*
gs=git status
gp=git push
gd=git diff $*
gl=git log --oneline --all --graph --decorate  $*


;= rem access directoy
cd=cd /d $*

..=cd ..
...=cd ../..

.1=cd ..
.2=cd ../..
.3=cd ../../..

.d=cd /d "d:\"
.c=cd /d "c:\"
.e=cd /d "e:\"
.f=cd /d "f:\"

.cmder=cd /d "%CMDER_ROOT%"
.dsk=cd /d "C:\Users\luuil\Desktop"
.work=cd /d "D:\hymlcv_svr\trunk"
.my=cd /d "D:\aMyProj"
.blog=cd /d "d:\aMyProj\hexo-blog-source\blog"
