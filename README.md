# Studienarbeit Timo Höting an der DHBW-Karlsruhe
=======================

## Entwicklung eines Komplettsystems zur Überwachung und Beleuchtung von Innen- und Außenbereichen mit Raspberry Pi und iOS App
--------------

In einem beliebigen Raum (oder Außenbereicht) werden einzeln ansteuerbare LED-Pixel angebracht. Zusätzlich befinden sich dort Bewegungsmelder und eine Überwachungskamera. Die Steuerung findet über einen Raspberry Pi statt. Dieser kann über eine Weboberfläche (opt.: iOS App) kontrolliert werden.
Es gibt drei Modi:

- Beleuchtung wird durch Bewegungsmelder ausgelöst (Reaktion darauf
kann vom User definiert werden)
- Beleuchtung wird manuell vom Benutzer über App gesteuert (Color
Chooser, Bereichsauswahl, Leuchteffekte)
- Bewegungsmelder als Alarmanlage, beim Auslösen wird der Benutzer
benachrichtigt und Bild der Kamera als Notifcation auf dem
Smartphone angezeigt

Sprachen:

- Raspberry Pi: Shell, Python

- App: Swift / Objective-C

Kontakt
--------------
mail@timohoeting.de

Installation
--------------
>git clone https://github.com/timohoeting/Studienarbeit-Anwendung.git
>sudo python Center.py yourUser

Standarduser: admin / password
