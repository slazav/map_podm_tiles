# copy this file to settings.sh and modify values in it 
PATH="../mapsoft/vector/vmap3:../mapsoft/programs:$PATH"

# directory with source vmap files
vmap_dir=~/home/map_podm/vmap

# destination and temp directories
fig_crop_dir=./result/fig_crop
fig_dir=./result/fig
png_dir=./result/png
tile_dir=./result/tiles
tile_tmp_dir=./result/tiles_tmp
border_dir=./editborder/cgi-bin/tiles

use_edited_border=1
join_objects=1
#join_objects=

nom_rscale=100000 # just to get source map names
fig_rscale=89415 # scale in google proj units / m = 50000/cos(56d)

# scale and size of "big" google tile
sc=9
maxZoom=14

# tiles to create
x1=304
x2=315
y1=157
y2=164
#x1=309
#x2=309
#y1=162
#y2=162

### commonly used pre-calculated values ###

calc(){
  var=$1; shift
  eval "$var=\"\$(printf \"%s\n\" \"$*\" | bc -l)\""
}

tile_size_px=
calc tile_size_px "256*2^(${maxZoom}-${sc})"

# merc units (equator meters) per scale=1 tile
k="$(echo "frw 180,0" |\
  convs_pt2pt "sphere" "lonlat" "" "sphere" "merc" ""|\
  head -c 11)"

# size of map, cm
calc map_size_cm "100.0/$fig_rscale * $k/2^($sc-1)"

# dpi to get tile_size_px
calc tile_dpi "($tile_size_px+1) / $map_size_cm * 2.54"
