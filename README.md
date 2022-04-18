# MINICPS Version 2

## Vorbereitung
Zur Installation kann entweder die schon vorbereitete Virtual Machine verwendet werden, die unter [LINK EINFÜGEN] zu finden ist oder eine neue virtuelle Maschine angelegt werden. Als Basis dient hier die virtuelle Maschine von MiniNet mit Ubuntu 18.4, die unter <a href="https://github.com/mininet/mininet/releases/download/2.3.0/mininet-2.3.0-210211-ubuntu-18.04.5-server-amd64-ovf.zip">MiniNet VM</a> zu finden ist. (Der VM wurden in der Konfiguration 4GB Arbeitsspeicher und 3 Kerne zur Verfügung gestellt. 2GB RAM sollten ausreichend sein, bei der Leistung sollte aber nicht gespart werden.)

Zuerst muss ein X11 Server auf dem Host-Gerät gestartet werden. Für Windows 10 empfielt sich der VcXsrv-Server. Mit einem passenden Eintrag in einem SSH-Tool zu X11-Forwarding wie in Putty (Category > Connection > SSH > X11 -> "Enable X11 forwarind" + "X display location: localhost:0.0"). Getestet werden kann diese Konfiguration, wenn eine Verbindung mit der VM hergestellt wird und  ```xterm``` in der Konsole ausführt; im Anschluss daran sollte sich im Host-OS ein Fenster öffnen mit einer Konsole. 

Nun müssen alle Softwarepakete installiert werden, die für die Ausführung und Kompilierung von MiniCPS 2.0 benötigt werden: 

1. Um das rt-labs PN-Feldgerät kompilieren zu können, ist eine aktuelle Version von CMAKE notwendig. Diese kann mit den folgenden Befehlen installiert werden (wie hier erklärt <a href="https://askubuntu.com/questions/355565/how-do-i-install-the-latest-version-of-cmake-from-the-command-line">Ask Ubuntu</a>): 
```
sudo apt remove --purge --auto-remove cmake
sudo apt purge --auto-remove cmake
sudo apt update && \
sudo apt install -y software-properties-common lsb-release && \
sudo apt clean all
wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | sudo tee /etc/apt/trusted.gpg.d/kitware.gpg >/dev/null
sudo apt-add-repository "deb https://apt.kitware.com/ubuntu/ $(lsb_release -cs) main"
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 6AF7F09730B3F0A4
sudo apt update
sudo apt install kitware-archive-keyring
sudo rm /etc/apt/trusted.gpg.d/kitware.gpg
sudo apt update
sudo apt install cmake
```

Es wird cmake 3.14 oder später benötigt. Diese kann mit ```cmake --version``` überprüft werden. 


2. Für die Ausführung der ProfiNet-Controllersimulation ist eine Python 3 Version > 3.6 notwendig. Diese kann mit folgenden Befehlen aktualisiert werden (wie hier beschrieben <a href="https://www.itsupportwale.com/blog/how-to-upgrade-to-python-3-7-on-ubuntu-18-10/">How to upgrade to python 3.7 on Ubuntu 18.10</a>)
```
sudo apt-get install python3.7
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2
sudo update-alternatives --config python3
```
Am Schluss sollte Python 3.7 asugewählt werden, um standardmäßig Python 3.7 zu Verwenden, wenn ```python3``` ausgeführt wird.

Um ```numpy``` zu installieren muss noch folgendes Paket zusätzlich installiert werden: 
```
sudo apt-get install python3.7-dev
pip3 install cython
```

3. Außerdem wird in der ProfiNet-Simulation das Paket ```scapy``` verwendet. Da dieses aber über pip nicht alle notwendigen Drittpakete installiert, muss man es manuell über das Git-Repo installieren. Das geht wie folgt: 
```
git clone https://github.com/secdev/scapy
cd scapy
sudo python3 setup.py install
```

4. Da für das Kompilieren des ProfiNet-Feldgeräts mit der rt-labs Bibliothek zur Anbindung an MiniCPS 2.0 eine SQLite Tabelle benötigt wird, muss man dieser Bibliothek die notwendigen Header-Dateien zur Verfügung stellen. Das geht mit: 
```
sudo apt-get install sqlite3 libsqlite3-dev
```

5. Zum Schluss wird noch der OVSTestcontroller für Mininet benötigt. Dieser lässt sich mit folgender Zeile installieren: 
```
sudo apt-get install openvswitch-testcontroller bridge-utils
```

## Installation von MiniCPS 2.0
 1. Klonen des Git-Repos zu MiniCPS 2.0
 2. Installieren der Python-Pakete: 
 ```
 cd python3.7
 pip3 install -r requirements.txt
 cd ../python2.7
 pip install -r requirements.txt
 ```

## Ausführen von MiniCPS Beispielprojekt Swat-S2

Vor der ersten Ausführung muss das System initialisiert werden: 
```
make swat-s2-init
```
Vor/Nach jeder Ausführung sollte das System bereinigt werden mit: 
```
make swat-s2-clean
```

Das Standardsystem lässt sich ausführen mit; sollte nicht das gwünschte Verhalten entstehen, dann in den Logs nach möglichen Fehlern suchen (für jedes Gerät/Prozess wird ein eigener Log unter /logs angelegt): 
```
make swat-s2
```

Verschiedene Angriffe mit: 
```
make swat-s2-{dcp-tamp / rpc-tamp / dos}
```

Weitere Angriffe müssen zur Laufzeit gestartet werden. Dafür muss das System normal gestartet werden und im Anschluss die Angreiferhost-Shell über Xterm geöffnet werden mit: 
```
mininet > xterm attacker
```
Im Ordner ```attacks``` finden sich noch die Angriffe: 
- ```replay.py``` (Replay-Attacke)
- ```pnio-tampering.py``` (Tampering with Data und PNIO-Protocol)
- ```forge.py``` (Forging-Attacke durch Einschleusen einer Alarmnachricht)

## Angriffe
Im MiniCPS 2.0 Beispielprojekt können zwei Arten von Angriffen ausgeführt werden, die sich unter anderem durch ihre Initialisierung in MiniCPS 2.0 unterscheiden. Der Benutzer sieht vorerst nur durch die Scada-Anwendung, dass das System eine Fehlfunktion besitzt. Angegriffen werden standardmäßig die Verbindung zwischen PLC1 und Dev3/LIT101 durch den Angreiferhost. Möchte man die Angriffe genauer analysieren und verstehen, sollte man sich zu Beginn eine Wireshark-Session pro Host öffnen. Dies kann man entweder direkt über die MiniNet-CLI machen oder über das Linux-System.
### Während Verbindungsaufbau
Angriffe, die den Verbindungsaufbau einer ProfiNet-Verbindung zwischen Feldgerät und Steuerung angreifen, werden im Startkommando spezifiziert und der Angriff findet ohne weitere Aktionen des Benutzers statt. Der Angriff wird zu Beginn gestartet. Vorerst exisitieren zwei Angriffe:
- <b>DCP-Tampering / DoS</b>: Bei diesem Angriff, wird das Gerät falsch konfiguriert, sodass ein weiterer Verbindungsaufbau nicht möglich ist. Die Gerätefunktionalität kann also in dieser Zeit nicht genutzt werden (DoS). Der Angriff geschieht über das Verändern einer DCP-Konfigurationsnachricht. Dabei wird dem Gerät eine andere IP Adresse zugewiesen. 
```
    make swat-s2-dcp-tamp
```
- <b>RPC-Tampering</b>: Beim RPC-Tampering wird der Verbindungsaufbau leicht verändert. Dabei ist der Verbindungsaufbau zwar erfolgreich, allerdings ändert der Angreifer den WatchDog-Factor ab, sodass der Watchdog-Timer eines IO-Devices länger als definiert ist. Dadurch könnten zukünfig einfach MitM-Angriffe während des Datenaustauschs stattfinden. 
```
    make swat-s2-rpc-tamp
```
### Während Datenaustausch
Angriffe, die während des Verbindungsaustauschs sind, müssen vom Anwender manuell gestartet werden. Hierfür öffnet über die MiniNet-Shell ein Xterm-Shellfenster auf dem Angreiferhost. Über dieses kann er die folgenden Angriffe ausführen: 
- <b>Forging</b>: Beim Forging wird an die Steuerung eine PNIO-Alarmnachricht versendet, dass der Watchdog-Timer des IO-Devices abgelaufen ist und dieses nun in den IDLE-Zustand übergegangen ist. Es wird also eine Nachricht zum scheinbaren Verbindungsabbruch versendet. 
```
# Starten der Attacker shell
mininet > xterm attacker
# Attacker-Shell
sudo python ./attacks/forging/alarm_injection.py
```
- <b>Replay</b>: Beim Replay wird eine bekannte Angriffsmethode verwendet, die oft bei ICS eingesetzt wird: Einschleusen von bereits aufgenommenen Datennachrichten, um einen alten Zustand im System zu propagieren. Hierzu wurde zuvor eine Kommunikation zwischen PLC1 und DEV3 aufgezeichnet und nach PNIO-RT-Nachrichten gefiltert (```./attacks/replay/sniff```). Wird Angriff gestartet, werden den beiden Verbindungspartnern die zuvor aufgezeichneten Nachrichten zugestellt. 
```
# Starten der Attacker shell
mininet > xterm attacker
# Attacker-Shell
sudo python ./attacks/replay/replay.py
```
- <b>PNIO-Tampering</b>: Beim PNIO-Tampering wird eine PNIO-Nachricht abgefangen und alle Datenwerte auf 0 gesetzt. Dieser Angriff lässt sich relativ schwer in der Scada-Anwendung nachvollziehen (aus dem Grund wie ProfiNet-Simulation und MiniCPS verbunden sind -> Updaterate der PN-Simulation viel höher als die der MiniCPS-Anwendung). 
```
# Starten der Attacker shell
mininet > xterm attacker
# Attacker-Shell
sudo python ./attacks/data_tampering/pnio_tampering.py
```