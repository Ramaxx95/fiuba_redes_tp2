# TP2: SDN
## Integrantes
* Herrera Alexis 			104639 
* La Torre Gabriel	  87796	 
* Lozano Ramiro 		  98263
* Valmaggia Matias 	  105621

## Instrucciones scripts

### Correr controlador
Posicionarse en la carpeta **"pox"** y correr el siguiente comando por CLI:  
    `./pox.py samples.pretty_log log.level --DEBUG forwarding.l2_learning firewall`

### Correr topologia
Para levantar la topologia hay que usar ***mininet*** usando el archivo ***topology.py*** en la carpeta principal de este repositorio:  
    `sudo mn --custom 'topology.py' --topo topology --mac --arp --switch ovsk --controller remote`  
    
Si se desea usar una topologia de mas de 2 switches se puede agregar la cantidad como argumento (en el siguiente ejemplo se hace una topologia de 4 switches):  
    `sudo mn --custom 'topology.py' --topo topology,4 --mac --arp --switch ovsk --controller remote`  

### Pruebas de trafico
Para este tipo de pruebas se usa la herramienta ***iperf*** que la vamos a levantar usando ***xterm*** para los hosts que se desean probar:  
> Levantamos una ventana para el *host 1*:
> 
> `mininet> xterm h1`
> 
> Y en la misma podemos levantar un servidor:
> 
> `iperf3 -s -p [numero de puerto a recibir mensajes]`
> 
> O un cliente:
> 
> `iperf3 -c [ip host servidor] -p [numero de puerto] [-u]`  

