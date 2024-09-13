for i in -0.001 -0.0005 0 0.0005 0.001
do
        mkdir e_$i
        cp ./dpgen.restart ./d33.lammps ./UniPero.pb e_$i
        cd e_$i
        sed -i "s/variable VALUEZ  equal 0/variable VALUEZ  equal $i/g" d33.lammps
        lmp -i d33.lammps
        cd ..
done
