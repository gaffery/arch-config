# Defined in - @ line 0
function ff --description 'alias ff ffmpeg -y -f x11grab -r 25 -s 2560x1440 -i :0 -f pulse -i alsa_output.pci-0000_00_1b.0.analog-stereo.monitor -c:v libx264 -pix_fmt yuv420p -crf 20 -vf scale=1920:1080 -f ismv -c:a mp3 ~/screencast.mp4'
	ffmpeg -y -f x11grab -r 25 -s 2560x1440 -i :0 -f pulse -i alsa_output.pci-0000_00_1b.0.analog-stereo.monitor -c:v libx264 -pix_fmt yuv420p -crf 20 -vf scale=1920:1080 -f ismv -c:a mp3 ~/screencast.mp4 $argv;
end
