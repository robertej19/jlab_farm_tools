file_to_compile=$1
exe_name=$2
echo $file_to_compile
echo $exe_name

cython --embed -o script_in_cython.c $file_to_compile
g++ -I/usr/include/python3.6m script_in_cython.c -lpython3.6m -o $exe_name
rm script_in_cython.c
