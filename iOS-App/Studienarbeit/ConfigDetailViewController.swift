//
//  ConfigDetailViewController.swift
//  Studienarbeit
//
//  Created by Timo Höting on 14.01.15.
//  Copyright (c) 2015 Timo Höting. All rights reserved.
//
import UIKit

class  ConfigDetailViewController: UIViewController, UITextFieldDelegate  {
    
    @IBOutlet var bt_safe: UIBarButtonItem!
    @IBOutlet var tf_ledcount: UITextField!
    @IBOutlet var tf_motionport1: UITextField!
    @IBOutlet var tf_motionport2: UITextField!

    @IBOutlet var tf_ftpdir: UITextField!
    @IBOutlet var tf_ftp: UITextField!
    @IBOutlet var timeperiod: UITextField!
    @IBOutlet var sw_safePW: UISwitch!
    @IBOutlet var sw_changeCam: UISwitch!
    
    @IBOutlet var tf_ftpuser: UITextField!
    @IBOutlet var tf_ftppassword: UITextField!
    @IBOutlet var tf_camurl: UITextField!
    @IBOutlet var tf_camuser: UITextField!
    @IBOutlet var tf_campassword: UITextField!
    @IBOutlet var tf_camdir: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        bt_safe.enabled = false
        textFieldDelegates()
        loadData()
    }
    
    @IBAction func btn_safe_PW(sender: AnyObject) {
        var switch_current = sw_safePW.on
        if (switch_current && !switch_PW_previous){
            globalDataManager.changeValueWithEntityName("Config", key: "authWithoutPW", value: "1")
            switch_PW_previous = true
        }
        if (!switch_current && switch_PW_previous){
            globalDataManager.changeValueWithEntityName("Config", key: "authWithoutPW", value: "0")
            switch_PW_previous = false
        }
    }

    @IBAction func btn_change_Cam(sender: UISwitch) {
        var switch_current = sw_changeCam.on
        if (switch_current && !switch_Cam_previous){
            if globalConnection.connection_established {
                globalConnection.changeConfigOnServerWith("camavaible", value: "1")
                globalDataManager.changeValueWithEntityName("Config", key: "camavaible", value: "1")
                switch_Cam_previous = true
                tf_ftpdir.enabled = true
                tf_ftp.enabled = true
                tf_ftpuser.enabled = true
                tf_ftppassword.enabled = true
                tf_camurl.enabled = true
                tf_camuser.enabled = true
                tf_campassword.enabled = true
                tf_camdir.enabled = true
            }
        }
        if (!switch_current && switch_Cam_previous){
            if globalConnection.connection_established {
                globalConnection.changeConfigOnServerWith("camavaible", value: "0")
                globalDataManager.changeValueWithEntityName("Config", key: "camavaible", value: "0")
                switch_Cam_previous = false
                tf_ftpdir.enabled = false
                tf_ftp.enabled = false
                tf_ftpuser.enabled = false
                tf_ftppassword.enabled = false
                tf_camurl.enabled = false
                tf_camuser.enabled = false
                tf_campassword.enabled = false
                tf_camdir.enabled = false
            }
        }
    }
  
     var temp_tf_ledcount = ""
     var temp_tf_motionport1 = ""
     var temp_tf_motionport2 = ""
     var temp_camavaible = ""
     var temp_ftp_dir = ""
     var temp_ftp = ""
     var temp_timeperiod = ""
     var switch_PW_previous = false
     var switch_Cam_previous = false
     var temp_safePW = ""
     var temp_ftpuser = ""
     var temp_ftppassword = ""
     var temp_camurl = ""
     var temp_camuser = ""
     var temp_campassword = ""
     var temp_camdir = ""
    
    private func textFieldDelegates() {
        tf_ledcount.delegate = self
        tf_motionport1.delegate = self
        tf_motionport2.delegate = self
        tf_ftpdir.delegate = self
        tf_ftp.delegate = self
        timeperiod.delegate = self
        tf_ftpuser.delegate = self
        tf_ftppassword.delegate = self
        tf_camurl.delegate = self
        tf_camuser.delegate = self
        tf_campassword.delegate = self
        tf_camdir.delegate = self
    }
    
    func textFieldShouldReturn(textField: UITextField) -> Bool {
        textField.resignFirstResponder()
        return true
    }
    
    func textFieldDidBeginEditing(textField: UITextField) {
        bt_safe.enabled = true
    }
    
    func textFieldDidEndEditing(textField: UITextField) {
        // nothing
    }
    
    func loadData() {
        if !globalConnection.connection_established || !IJReachability.isConnectedToNetwork() {
            tf_ledcount.enabled = false
            tf_motionport1.enabled = false
            tf_motionport2.enabled = false
            sw_changeCam.enabled = false
            tf_ftpdir.enabled = false
            tf_ftp.enabled = false
            timeperiod.enabled = false
            tf_ftpuser.enabled = false
            tf_ftppassword.enabled = false
            tf_camurl.enabled = false
            tf_camuser.enabled = false
            tf_campassword.enabled = false
            tf_camdir.enabled = false
            
            temp_safePW = globalDataManager.loadValue("Config", key: "authWithoutPW")
            if (temp_safePW == "1") {
                sw_safePW.setOn(true, animated: true)
                switch_PW_previous = true
            } else {
                sw_safePW.setOn(false, animated: true)
                switch_PW_previous = false
            }
            return
        }
        
        temp_tf_ledcount = globalDataManager.loadValue("Config", key: "ledcount")
        temp_tf_motionport1 = globalDataManager.loadValue("Config", key: "motionport1")
        temp_tf_motionport2 = globalDataManager.loadValue("Config", key: "motionport2")
        temp_camavaible = globalDataManager.loadValue("Config", key: "camavaible")
        temp_ftp_dir = globalDataManager.loadValue("Config", key: "ftpdir")
        temp_ftp = globalDataManager.loadValue("Config", key: "ftp")
        temp_timeperiod = globalDataManager.loadValue("Config", key: "timeperiod")
        temp_safePW = globalDataManager.loadValue("Config", key: "authWithoutPW")
        temp_ftpuser = globalDataManager.loadValue("Config", key: "ftpuser")
        temp_ftppassword = globalDataManager.loadValue("Config", key: "ftppassword")
        temp_camurl = globalDataManager.loadValue("Config", key: "camurl")
        temp_camuser = globalDataManager.loadValue("Config", key: "camuser")
        temp_campassword = globalDataManager.loadValue("Config", key: "campassword")
        temp_camdir = globalDataManager.loadValue("Config", key: "camdir")

        tf_ledcount.text = temp_tf_ledcount
        tf_motionport1.text = temp_tf_motionport1
        tf_motionport2.text = temp_tf_motionport2
        tf_ftpdir.text = temp_ftp_dir
        tf_ftp.text = temp_ftp
        timeperiod.text = temp_timeperiod
        tf_ftpuser.text = temp_ftpuser
        tf_ftppassword.text = temp_ftppassword
        tf_camurl.text = temp_camurl
        tf_camuser.text = temp_camuser
        tf_campassword.text = temp_campassword
        tf_camdir.text = temp_camdir
        
        if (temp_safePW == "1") {
            sw_safePW.setOn(true, animated: true)
            switch_PW_previous = true
        } else {
            sw_safePW.setOn(false, animated: true)
            switch_PW_previous = false
        }
        
        if (temp_camavaible == "" || temp_camavaible == "0") {
            tf_ftp.enabled = false
            tf_ftpdir.enabled = false
            tf_ftpuser.enabled = false
            tf_ftppassword.enabled = false
            tf_camurl.enabled = false
            tf_camuser.enabled = false
            tf_campassword.enabled = false
            tf_camdir.enabled = false
            sw_changeCam.setOn(false, animated: true)
        } else {
            tf_ftp.enabled = true
            tf_ftpdir.enabled = true
            tf_ftpuser.enabled = true
            tf_ftppassword.enabled = true
            tf_camurl.enabled = true
            tf_camuser.enabled = true
            tf_campassword.enabled = true
            tf_camdir.enabled = true
            sw_changeCam.setOn(true, animated: true)
        }
    }
    
    @IBAction func safeData(sender: AnyObject) {
        self.safeChangedData()
    }
    
    func safeChangedData(){
        if (!globalConnection.connection_established){
            return
        }
        if (temp_tf_ledcount != tf_ledcount.text) {
            globalConnection.changeConfigOnServerWith("ledcount", value: tf_ledcount.text)
            globalDataManager.changeValueWithEntityName("Config", key: "ledcount", value: tf_ledcount.text)
        }
        if (temp_tf_motionport1 != tf_motionport1.text) {
            globalConnection.changeConfigOnServerWith("motionport1", value: tf_motionport1.text)
            globalDataManager.changeValueWithEntityName("Config", key: "motionport1", value: tf_motionport1.text)
        }
        if (temp_tf_motionport2 != tf_motionport2.text) {
            globalConnection.changeConfigOnServerWith("motionport2", value: tf_motionport2.text)
            globalDataManager.changeValueWithEntityName("Config", key: "motionport2", value: tf_motionport2.text)
        }
        if (temp_ftp_dir != tf_ftpdir.text) {
            globalConnection.changeConfigOnServerWith("ftp_directory", value: tf_ftpdir.text)
            globalDataManager.changeValueWithEntityName("Config", key: "ftpdir", value: tf_ftpdir.text)
        }
        if (temp_ftp != tf_ftp.text) {
            globalConnection.changeConfigOnServerWith("ftp_host", value: tf_ftp.text)
            globalDataManager.changeValueWithEntityName("Config", key: "ftp", value: tf_ftp.text)
        }
        if (temp_timeperiod != timeperiod.text) {
            globalConnection.changeConfigOnServerWith("timeperiod", value: timeperiod.text)
            globalDataManager.changeValueWithEntityName("Config", key: "timeperiod", value: timeperiod.text)
        }
        if (temp_ftpuser != tf_ftpuser.text) {
            globalConnection.changeConfigOnServerWith("ftp_user", value: tf_ftpuser.text)
            globalDataManager.changeValueWithEntityName("Config", key: "ftpuser", value: tf_ftpuser.text)
        }
        if (temp_ftppassword != tf_ftppassword.text) {
            globalConnection.changeConfigOnServerWith("ftp_pw", value: tf_ftppassword.text)
            globalDataManager.changeValueWithEntityName("Config", key: "ftppassword", value: tf_ftppassword.text)
        }
        if (temp_camurl != tf_camurl.text) {
            globalConnection.changeConfigOnServerWith("cam_host", value: tf_camurl.text)
            globalDataManager.changeValueWithEntityName("Config", key: "camurl", value: tf_ftppassword.text)
        }
        if (temp_camuser != tf_camuser.text) {
            globalConnection.changeConfigOnServerWith("cam_user", value: tf_camuser.text)
            globalDataManager.changeValueWithEntityName("Config", key: "camuser", value: tf_ftppassword.text)
        }
        if (temp_campassword != tf_campassword.text) {
            globalConnection.changeConfigOnServerWith("cam_pw", value: tf_campassword.text)
            globalDataManager.changeValueWithEntityName("Config", key: "campassword", value: tf_campassword.text)
        }
        if (temp_camdir != tf_camdir.text) {
            globalConnection.changeConfigOnServerWith("cam_dir", value: tf_camdir.text)
            globalDataManager.changeValueWithEntityName("Config", key: "camdir", value: tf_camdir.text)
        }
        self.loadData()
        bt_safe.enabled = false
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    
}
