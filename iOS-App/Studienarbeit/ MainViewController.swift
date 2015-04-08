 //
//  MainViewController.swift
//  Studienarbeit
//
//  Created by Timo Höting on 03.01.15.
//  Copyright (c) 2015 Timo Höting. All rights reserved.
//

import UIKit
import CoreData
import CFNetwork
import CoreFoundation
 


class  MainViewController: UIViewController, WRRequestDelegate {
    
    @IBOutlet var btn_modus: UIButton!
    @IBOutlet var lbl_connected: UILabel!
    @IBOutlet var lbl_modus: UILabel!
    @IBOutlet var btn_connect: UIButton!
    @IBAction func btn_connect(sender: AnyObject) {
        if (!globalConnection.connection_established){
            self.initLoginView()
            return
        }
        globalConnection.connection_established = false
        self.reloadView()
    }
    
    func printKeys (key : AnyObject, value : AnyObject, context : AnyObject) {
        CFShow(key)
    }
    

    func requestCompleted (request : WRRequest) {
        println("success")
        var image = UIImage(data: downloadFile.receivedData)
    }
    
    func requestFailed (request : WRRequest) {
        println("failed")
    }
    
    var downloadFile = WRRequestDownload()
    
    override func viewDidLoad() {
        super.viewDidLoad()

        if !globalConnection.connection_established {
            firstLaunchOfApplication()
            initLoginView()
        }
        reloadView()
        
        globalFtp.loadFTPFirectory()
    }
    
    func reloadView(){
        setModus()
        setButtonConnection()
        return
    }
    
    @IBAction func btn_modus(sender: UIButton) {
        if ( globalConnection.connection_established ) {
            var modus = globalDataManager.loadValue("Config", key: "modus")
            if ( modus.toInt() == 0) {
                globalConnection.setNewModus(1)
                globalDataManager.changeValueWithEntityName("Config", key: "modus", value: "1")
            }
            if ( modus.toInt() == 1) {
                globalConnection.setNewModus(2)
                globalDataManager.changeValueWithEntityName("Config", key: "modus", value: "2")
            }
            if ( modus.toInt() == 2) {
                globalConnection.setNewModus(0)
                globalDataManager.changeValueWithEntityName("Config", key: "modus", value: "0")
            }
            setModus()
        }
    }
    
    func firstLaunchOfApplication() {
        if ( globalDataManager.countElementsInEntity("Config") == 0 ) {
            globalDataManager.insertNilConfig()
        }
        if ( globalDataManager.countElementsInEntity("UserSettings") == 0 ) {
            globalDataManager.insertNilUserSettings()
        }
        
    }
    
    func validConfigurationAvaible() -> Bool {
        if (globalDataManager.loadValue("Config", key: "host") == "" || globalDataManager.loadValue("Config", key: "port") == "") {
            return false
        }
        return true
    }

    func connectWithoutAuthentication() -> Bool {
        if ( globalDataManager.loadValue("UserSettings", key: "authWithoutPW") == "1") {
            return true
        }
        return false
    }
    
    func syncWithServer () {
        globalConnection.getSystemStatusFromServer()
        globalConnection.getLEDStatusFromServer()
        globalConnection.sendDeviceToken()
    }
    
    func setButtonConnection() {
        if ( globalConnection.connection_established ) {
            btn_connect.setTitle("Trennen", forState: UIControlState.Normal)
            return
        }
            btn_connect.setTitle("Verbinden", forState: UIControlState.Normal)
    }
   
    func setModus() {
        if ( !globalConnection.connection_established ) {
            lbl_modus.text = "offline"
            btn_modus.enabled = false
            return
        }
        var modus = globalDataManager.loadValue("Config", key: "modus")
        if ( modus.toInt() == 0) {
            lbl_modus.text = "Bewegungsmelder"
            btn_modus.enabled = true
            return
        }
        if ( modus.toInt() == 1) {
            lbl_modus.text = "Manuelle Steuerung"
            btn_modus.enabled = true
            return
        }
        if ( modus.toInt() == 2) {
            lbl_modus.text = "Alarmgesichert"
            btn_modus.enabled = true
            return
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    /*@IBAction func toggleSideMenu(sender: AnyObject) {
        toggleSideMenuView()
    }*/

    var alertField_User: UITextField?
    var alertField_PW: UITextField?
    
    func initLoginView() {
        if !validConfigurationAvaible() {
            AlertWindow().alert(self, title: "Konfiguration", message: "Bitte geben sie gültige Verbindungsdaten ein.")
            return
        }
        if connectWithoutAuthentication() == false {
            let connectAlert = UIAlertController(title: "Authentifizierung notwendig", message: "Sie können die Authentifizierung unter Einstellungen deaktivieren.", preferredStyle: UIAlertControllerStyle.Alert)
            connectAlert.addAction(UIAlertAction(title: "Abbrechen", style: UIAlertActionStyle.Default, handler: nil))
            connectAlert.addAction(UIAlertAction(title: "Verbinden", style: UIAlertActionStyle.Default, handler: userPressedConnectInLoginView))
            connectAlert.addTextFieldWithConfigurationHandler({(textField: UITextField!) in
                textField.placeholder = "Benutzer:"
                textField.secureTextEntry = false
                self.alertField_User = textField
            })
            connectAlert.addTextFieldWithConfigurationHandler({(textField: UITextField!) in
                textField.placeholder = "Passwort:"
                textField.secureTextEntry = true
                self.alertField_PW = textField
            })
            self.parentViewController?.presentViewController(connectAlert, animated: true, completion: nil)
            return
        } else {
            self.connectServer(nil, pw: nil)
        }
    }
    
    func userPressedConnectInLoginView(alert: UIAlertAction!){
        var user = alertField_User?.text
        var pw = alertField_PW?.text
        
        if ( user == "" || pw == "" ){
            initLoginView()
            return
        }
        if ( user != globalDataManager.loadValue("Config", key: "user") || pw != globalDataManager.loadValue("Config", key: "pw")){
            self.connectServer(user, pw: pw)
            //initLoginView()
            return
        }
        self.connectServer(nil, pw: nil)
    }
    
    func connectServer(user : NSString?, pw : NSString?){
        if (user != nil && pw != nil){
            var message = globalConnection.createMessageStringWithCredentials(ProtocolType.AUTH, user!,pw!, "", "", "", "", "", "", "", "", "")
            globalConnection.sendMessageViaHttpPostWithCompletion(message) { (answer : NSString) in
                if answer.containsString("LOGIN:TRUE") {
                    NSOperationQueue.mainQueue().addOperationWithBlock() { () in
                        globalDataManager.changeValueWithEntityName("Config", key: "user", value: user!)
                        globalDataManager.changeValueWithEntityName("Config", key: "pw", value: pw!)
                        globalConnection.connection_established = true
                        self.syncWithServer()
                        self.reloadView()
                    }
                } else {
                    self.initLoginView()
                }
            }
        } else {
            var message = globalConnection.createMessageStringWith(ProtocolType.AUTH, "", "", "", "", "", "", "", "", "")
            globalConnection.sendMessageViaHttpPostWithCompletion(message) { (answer : NSString) in
                println(answer)
                if answer.containsString("LOGIN:TRUE") {
                    NSOperationQueue.mainQueue().addOperationWithBlock() { () in
                        globalConnection.connection_established = true
                        self.syncWithServer()
                        self.reloadView()
                    }
                } else {
                    self.initLoginView()
                }
            }

        }
            }
    
}

