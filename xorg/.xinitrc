xrandr --output HDMI2 --auto --right-of HDMI3
xsetroot -cursor_name left_ptr
xrdb -merge ~/.Xresources
numlockx &
sxhkd -m 1 &
exec bspwm
