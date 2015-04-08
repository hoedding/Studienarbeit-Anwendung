//
//  ViewController.swift
//  Studienarbeit
//
//  Created by Timo Höting on 03.01.15.
//  Copyright (c) 2015 Timo Höting. All rights reserved.
//

import UIKit

var globalConnection : ConnectServerHTTP = ConnectServerHTTP()
var globalDataManager : CoreDataManager = CoreDataManager()
var globalFtp = ConnectFTP()
var globalToken = NSString()

class SlideViewController: ENSideMenuNavigationController, ENSideMenuDelegate {

    override func viewDidLoad() {
        super.viewDidLoad()
        
        sideMenu = ENSideMenu(sourceView: self.view, menuTableViewController: SlideViewTableController(), menuPosition:.Left)
        sideMenu?.delegate = self
        sideMenu?.menuWidth = 180.0
        sideMenu?.bouncingEnabled = false

        view.bringSubviewToFront(navigationBar)
        
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()

    }
    
    // MARK: - ENSideMenu Delegate
    func sideMenuWillOpen() {
        println("sideMenuWillOpen")
    }
    
    func sideMenuWillClose() {
        println("sideMenuWillClose")
    }
    
    /*
    // MARK: - Navigation
    
    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepareForSegue(segue: UIStoryboardSegue!, sender: AnyObject!) {
    // Get the new view controller using segue.destinationViewController.
    // Pass the selected object to the new view controller.
    }
    */


}

