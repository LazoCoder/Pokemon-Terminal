#Script to change the terminal background if using xfce4-terminal

path=$HOME'/.config/xfce4/terminal/terminalrc'
sed -i '/BackgroundImage/d' $path
echo 'BackgroundImageFile='$1 >> $path
