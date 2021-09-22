Function Gzip-File([ValidateScript({Test-Path $_})][string]$File){

    $srcFile = Get-Item -Path $File
    $newFileName = "$($srcFile.FullName).gz"

    try
    {
        $srcFileStream = New-Object System.IO.FileStream($srcFile.FullName,([IO.FileMode]::Open),([IO.FileAccess]::Read),([IO.FileShare]::Read))
        $dstFileStream = New-Object System.IO.FileStream($newFileName,([IO.FileMode]::Create),([IO.FileAccess]::Write),([IO.FileShare]::None))
        $gzip = New-Object System.IO.Compression.GZipStream($dstFileStream,[System.IO.Compression.CompressionMode]::Compress)
        $srcFileStream.CopyTo($gzip)
    }
    catch
    {
        Write-Host "$_.Exception.Message" -ForegroundColor Red
    }
    finally
    {
        $gzip.Dispose()
        $srcFileStream.Dispose()
        $dstFileStream.Dispose()
    }
}

# Minify the html
$files = Get-ChildItem ./ -recurse -force -include *min..html | where-object{$_.fullname -notlike '*node_modules*'}
foreach($file in $files){
    Gzip-File file.FullName
}
