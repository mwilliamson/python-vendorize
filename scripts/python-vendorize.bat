@setlocal enableextensions
@set errorlevel=
@python %~d0%~p0%~n0 %*
@endlocal
@exit /b %errorlevel%
