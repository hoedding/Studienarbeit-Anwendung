//
//  AlertWindow.swift
//  Studienarbeit
//
//  Created by Timo Höting on 25.01.15.
//  Copyright (c) 2015 Timo Höting. All rights reserved.
//

import Foundation
import UIKit

class AlertWindow {

    func alert(view : UIViewController, title : String, message : String) {
        let connectAlert = UIAlertController(title: title, message: message, preferredStyle: UIAlertControllerStyle.Alert)
        connectAlert.addAction(UIAlertAction(title: "OK", style: UIAlertActionStyle.Default,
            handler: nil))
        
        view.parentViewController?.presentViewController(connectAlert, animated: true, completion: nil)
    }
    
    func showConnectionError (view : UIViewController) {
        let connectAlert = UIAlertController(title: "Verbindung fehlgeschlagen", message: "Verbindung zum Server konnte nicht hergestellt werden. Bitte Einstellungen überprüfen.", preferredStyle: UIAlertControllerStyle.Alert)
        connectAlert.addAction(UIAlertAction(title: "OK", style: UIAlertActionStyle.Default,
            handler: nil))
        view.parentViewController?.presentViewController(connectAlert, animated: true, completion: nil)
    }

}