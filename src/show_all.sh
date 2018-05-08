for i in `seq 1 107`; do echo "$i" && ./repair_mesh.py $i n & ./repair_mesh.py $i; done
