# Clip Tool

可以用于剪辑的工具调用说明。
主要可以使用`ffmpeg`和`ffprobe`这两个命令行工具，但是为了避免乱码问题，请调用封装后的脚本，所有参数都跟原来的命令一样，都会透传给实际的命令。

## 调用示例

ffmpeg
```powershell
pwsh -File scripts\ffmpeg.ps1 -i input.mp4 <...other ffmpeg parameters...>  out.mp4
```

ffprobe
```powershell
pwsh -File scripts\ffprobe.ps1 <...other ffmpeg parameters...>  input.mp4
```