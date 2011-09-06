@echo off
for %%P in (python.exe) do (
  if not exist "%%~$PATH:P" (
    for %%_ in (
      C:\python27 ^
      C:\priv\prog\python27
    ) do (
      if exist %%_ (
        PATH %%PATH%%;%%_
        goto break
      )
    )
  )
)
:break
