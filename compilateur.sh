if [ "$#" -ne 1 ]; then
    echo "Il faut exactement un argument"
	exit 2
else
	python src/anasyn.py -p --show-ident-table "$1"
	python src/machine_virtuelle.py tests/code.txt
fi
echo $#
