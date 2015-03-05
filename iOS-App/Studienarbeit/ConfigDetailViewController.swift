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
    @IBOutlet var camavaible: UITextField!
    @IBOutlet var url: UITextField!
    @IBOutlet var shorturl: UITextField!
    @IBOutlet var ftp: UITextField!
    @IBOutlet var timeperiod: UITextField!
    @IBOutlet weak var sw_safePW: UISwitch!
    @IBAction func btn_safePW(sender: AnyObject) {
        var switch_current = sw_safePW.on
        if (switch_current && !switch_previous){
            globalDataManager.changeValueWithEntityName("UserSettings", key: "authWithoutPW", value: "1")
            switch_previous = true
        }
        if (!switch_current && switch_previous){
            globalDataManager.changeValueWithEntityName("UserSettings", key: "authWithoutPW", value: "0")
            switch_previous = false
        }
    }

     var temp_tf_ledcount = ""
     var temp_tf_motionport1 = ""
     var temp_tf_motionport2 = ""
     var temp_camavaible = ""
     var temp_url = ""
     var temp_shorturl = ""
     var temp_ftp = ""
     var temp_timeperiod = ""
     var switch_previous = false
    
    override func viewDidLoad() {
        super.viewDidLoad()
        bt_safe.enabled = false
        textFieldDelegates()
        loadData()
    }
    
    private func textFieldDelegates() {
        tf_ledcount.delegate = self
        tf_motionport1.delegate = self
        tf_motionport2.delegate = self
        camavaible.delegate = self
        url.delegate = self
        shorturl.delegate = self
        ftp.delegate = self
        timeperiod.delegate = self
    }
    
    func textFieldShouldReturn(textField: UITextField!) -> Bool {
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
        if !globalConnection.connection_established {
            tf_ledcount.enabled = false
            tf_motionport1.enabled = false
            tf_motionport2.enabled = false
            camavaible.enabled = false
            url.enabled = false
            shorturl.enabled = false
            ftp.enabled = false
            timeperiod.enabled = false
            sw_safePW.enabled = false
            return
        }
        temp_tf_ledcount = globalDataManager.loadValue("Config", key: "ledcount")
        temp_tf_motionport1 = globalDataManager.loadValue("Config", key: "motionport1")
        temp_tf_motionport2 = globalDataManager.loadValue("Config", key: "motionport2")
        temp_camavaible = globalDataManager.loadValue("Config", key: "camavaible")
        temp_url = globalDataManager.loadValue("Config", key: "cam_url")
        temp_shorturl = globalDataManager.loadValue("Config", key: "cam_url_short")
        temp_ftp = globalDataManager.loadValue("Config", key: "ftp_url")
        temp_timeperiod = globalDataManager.loadValue("Config", key: "timeperiod")
        var switch_value = globalDataManager.loadValue("UserSettings", key: "authWithoutPW")

        tf_ledcount.text = temp_tf_ledcount
        tf_motionport1.text = temp_tf_motionport1
        tf_motionport2.text = temp_tf_motionport2
        camavaible.text = temp_camavaible
        url.text = temp_url
        shorturl.text = temp_shorturl
        ftp.text = temp_ftp
        timeperiod.text = temp_timeperiod
        
        if (switch_value == "1") {
            sw_safePW.setOn(true, animated: true)
            switch_previous = true
        } else {
            sw_safePW.setOn(false, animated: true)
            switch_previous = false
        }
        
        if (temp_camavaible == "" || temp_camavaible == "0") {
            url.enabled = false
            shorturl.enabled = false
        } else {
            url.enabled = true
            shorturl.enabled = true

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
        if (temp_camavaible != camavaible.text) {
            globalConnection.changeConfigOnServerWith("camavaible", value: camavaible.text)
            globalDataManager.changeValueWithEntityName("Config", key: "camavaible", value: camavaible.text)
        }
        if (temp_url != url.text) {
            globalConnection.changeConfigOnServerWith("cam_url", value: url.text)
            globalDataManager.changeValueWithEntityName("Config", key: "cam_url", value: url.text)
        }
        if (temp_shorturl != shorturl.text) {
            globalConnection.changeConfigOnServerWith("cam_url_short", value: shorturl.text)
            globalDataManager.changeValueWithEntityName("Config", key: "cam_url_short", value: shorturl.text)
        }
        if (temp_ftp != ftp.text) {
            globalConnection.changeConfigOnServerWith("ftp_url", value: ftp.text)
            globalDataManager.changeValueWithEntityName("Config", key: "ftp_url", value: ftp.text)
        }
        if (temp_timeperiod != timeperiod.text) {
            globalConnection.changeConfigOnServerWith("timeperiod", value: timeperiod.text)
            globalDataManager.changeValueWithEntityName("Config", key: "timeperiod", value: timeperiod.text)
        }
        self.loadData()
        bt_safe.enabled = false
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    
}
