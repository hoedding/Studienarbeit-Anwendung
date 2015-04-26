//
//  LiveViewController.swift
//  Studienarbeit
//
//  Created by Timo Höting on 23.04.15.
//  Copyright (c) 2015 Timo Höting. All rights reserved.
//

import UIKit

class LiveViewController : UIViewController {
    
    var imageview = UIImageView()
    var camurl = "http://"
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        if ( globalDataManager.loadValue("Config", key: "camavaible") == "0"  ){
            self.view.backgroundColor = UIColor.lightGrayColor()
            AlertWindow().alert(self, title: "Verbindungsfehler", message: "Es konnte keine Verbindung zur Kamera hergestellt werden.")
            return
        }
        
        buildCamURL()
        buildImageview()
        loadImageView()
        startReloadTimer()
    }
    
    func startReloadTimer(){
        var timer = NSTimer.scheduledTimerWithTimeInterval(0.3, target: self, selector: Selector("loadImageView"), userInfo: nil, repeats: true)
    }
    
    func buildImageview(){
        imageview = UIImageView(frame: CGRect(x: 0, y: 200, width: self.view.frame.width, height: 300))
        imageview.backgroundColor = UIColor.greenColor()
        self.view.addSubview(imageview)
        self.view.bringSubviewToFront(imageview)
    }
    
    func buildCamURL(){
        var user = globalDataManager.loadValue("Config", key: "camuser")
        var pw = globalDataManager.loadValue("Config", key: "campassword")
        var url = globalDataManager.loadValue("Config", key: "camurl")
        var dir = globalDataManager.loadValue("Config", key: "camdir")
        camurl = camurl + user + ":" + pw + "@" + url + dir
        
        println("url:" +  camurl)
    }
    
    func loadImageView(){
        dispatch_async(dispatch_get_main_queue(), {
            let url = NSURL(string: self.camurl)
            let data = NSData(contentsOfURL: url!)
            var _image : UIImage! = UIImage(data: data!)
            if _image != nil{
                self.imageview.image = _image
            }
        })
    }
}
