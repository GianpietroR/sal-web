# Backup notturno del database SAL Web.
# Copia data/sal.db su disco C: (fisicamente indipendente da D:) e conserva le ultime 14 copie.
$src = 'D:\Software SAL\sal-web\data'
$dst = 'C:\SAL-backup'
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item "$src\sal.db" ("{0}\sal-{1}.db" -f $dst, (Get-Date -Format 'yyyy-MM-dd')) -Force
Get-ChildItem $dst -Filter 'sal-*.db' | Sort-Object Name -Descending | Select-Object -Skip 14 | Remove-Item -Force
