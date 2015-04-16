//
//  ConfigViewController.swift
//  Studienarbeit
//
//  Created by Timo Höting on 09.01.15.
//  Copyright (c) 2015 Timo Höting. All rights reserved.
//

import UIKit

class  ConfigViewController: UIViewController, UITextFieldDelegate  {
    
    @IBOutlet var tf_host: UITextField!
    @IBOutlet var tf_port: UITextField!
    @IBOutlet var tf_user: UITextField!
    @IBOutlet var tf_pw: UITextField!
    
    var temp_tf_host = ""
    var temp_tf_port = ""
    var temp_tf_user = ""
    var temp_tf_pw = ""

    @IBOutlet var btn_safe: UIBarButtonItem!
    @IBAction func btn_safe(sender: AnyObject) {
        safeData()
    }
    override func viewDidLoad() {
        super.viewDidLoad()
        textFieldDelegates()
        btn_safe.enabled = false
        loadData()
    }
    
    func textFieldShouldReturn(textField: UITextField) -> Bool {
        textField.resignFirstResponder()
        return true
    }
    
    func textFieldDidBeginEditing(textField: UITextField) {
        btn_safe.enabled = true
    }
    
    func textFieldDidEndEditing(textField: UITextField) {
        //nothing
    }
    
    private func textFieldDelegates() {
        tf_host.delegate = self
         tf_port.delegate = self
         tf_user.delegate = self
         tf_pw.delegate = self
    }

    func safeData() {
        if (!globalConnection.connection_established){
            if (temp_tf_host != tf_host.text) {
                globalDataManager.changeValueWithEntityName("Config", key: "host", value: tf_host.text)
            }
            if (temp_tf_host != tf_port.text) {
                globalDataManager.changeValueWithEntityName("Config", key: "port", value: tf_port.text)
            }
            return
        }
        if (temp_tf_host != tf_host.text) {
            globalDataManager.changeValueWithEntityName("Config", key: "host", value: tf_host.text)
            //globalConnection.connection_established = false
        }
        if (temp_tf_host != tf_port.text) {
            globalDataManager.changeValueWithEntityName("Config", key: "port", value: tf_port.text)
            //globalConnection.connection_established = false
        }
        if (temp_tf_user != tf_user.text || temp_tf_pw != tf_pw.text) {
            loginAlert()
        }
    }
    
    var alertField_User: UITextField?
    var alertField_PW: UITextField?
    
    func loginAlert(){
        let connectAlert = UIAlertController(title: "Authentifizierung notwendig", message: "Für die Änderung von Passwort oder Benutzername ist die Eingabe eines Bestehenden Nutzers erforderlich.", preferredStyle: UIAlertControllerStyle.Alert)
        connectAlert.addAction(UIAlertAction(title: "Abbrechen", style: UIAlertActionStyle.Default, handler: nil))
        connectAlert.addAction(UIAlertAction(title: "Bestätigen", style: UIAlertActionStyle.Default, handler: userPressedConnect))
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
    }
    
    func userPressedConnect(alert: UIAlertAction!){
        var user = alertField_User?.text
        var pw = alertField_PW?.text
        

        
        if ( globalConnection.connection_established && globalDataManager.checkLocalCredetials(user!, pw: pw!) ){
            
            globalConnection.changeConfigOnServerWith("user", value: tf_user.text)
            globalConnection.changeConfigOnServerWith("pw", value: tf_pw.text)
            globalDataManager.changeValueWithEntityName("Config", key: "user", value: tf_user.text)
            globalDataManager.changeValueWithEntityName("Config", key: "pw", value: tf_pw.text)
            return
        }
        loginAlert()
    }
    
    func loadData() {
        if !globalConnection.connection_established {
            tf_user.enabled = false
            tf_pw.enabled = false
            btn_safe.enabled = false
            
            temp_tf_host = globalDataManager.loadValue("Config", key: "host")
            temp_tf_port = globalDataManager.loadValue("Config", key: "port")
            tf_host.text = temp_tf_host
            tf_port.text = temp_tf_port
            
            return
        }
        
        temp_tf_user = globalDataManager.loadValue("Config", key: "user")
        temp_tf_pw = globalDataManager.loadValue("Config", key: "pw")
        temp_tf_host = globalDataManager.loadValue("Config", key: "host")
        temp_tf_port = globalDataManager.loadValue("Config", key: "port")
        
        tf_host.text = temp_tf_host
        tf_port.text = temp_tf_port
        tf_user.text = temp_tf_user
        tf_pw.text = temp_tf_pw
        
        btn_safe.enabled = false
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }

}
