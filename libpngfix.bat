for %%i in (*.png) do identify %%i
for %%i in (*.png) do convert %%i -strip %%i
for %%i in (*.png) do identify %%i