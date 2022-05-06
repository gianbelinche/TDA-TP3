unameOut="$(uname -s)"
ROJO="\033[0;31m"
VERDE="\033[0;32m"

case "${unameOut}" in
    MINGW*)     
        PYTHON=python
        ;;
    *)
        PYTHON=python3
        ;;
esac

comprobar() {
    RUTA=$1
    SOL="$2, $3" # Formatear segun quede la salida
    RES=$($PYTHON main.py $RUTA)

    if [ "$RES" = "$SOL" ]; then
        echo -e "${VERDE}Test '$RUTA' Passed"
    else
        echo -e "${ROJO}Test '$RUTA' failed"
        echo -e "Esperado: $SOL"
        echo -e "Recibido: $RES"
    fi
}

comprobar "tests/bifurcaciones1.txt" 18 3
comprobar "tests/bifurcaciones2.txt" 24 3
comprobar "tests/cycle1.txt" 9 3
comprobar "tests/directo1.txt" 12 4
comprobar "tests/directo2.txt" 18 3
comprobar "tests/multiple1.txt" 24 4
comprobar "tests/multiple2.txt" 85 10
comprobar "tests/mult_correctas1.txt" 30 5
comprobar "tests/pesado1.txt" 30 20
