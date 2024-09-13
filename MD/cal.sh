for i in 300 450 600 750 900
do
  cd $i
  lmp -i npt.lammps 
  cd ..
done
