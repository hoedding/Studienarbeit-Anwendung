//
//  MyMenuTableViewController.swift
//  Studienarbeit
//
//  Created by Timo Höting on 03.01.15.
//  Copyright (c) 2015 Timo Höting. All rights reserved.
//

import UIKit

class SlideViewTableController : UITableViewController {
    var selectedMenuItem : Int = 0
    var pages : [String] = ["Start", "Farben", "Konfiguration", "Bilder", "Info"]
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Customize apperance of table view
        tableView.contentInset = UIEdgeInsetsMake(64.0, 0, 0, 0) //
        tableView.separatorStyle = .None
        tableView.backgroundColor = UIColor.clearColor()
        tableView.scrollsToTop = false
        
        // Preserve selection between presentations
        self.clearsSelectionOnViewWillAppear = false
        
        tableView.selectRowAtIndexPath(NSIndexPath(forRow: selectedMenuItem, inSection: 0), animated: false, scrollPosition: .Middle)
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    // MARK: - Table view data source

    override func numberOfSectionsInTableView(tableView: UITableView) -> Int {
        // Return the number of sections.
        return 1
    }

    override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // Return the number of rows in the section.
        return 5
    }

    override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        
        var cell = tableView.dequeueReusableCellWithIdentifier("CELL") as? UITableViewCell
        
        if (cell == nil) {
            cell = UITableViewCell(style: UITableViewCellStyle.Default, reuseIdentifier: "CELL")
            cell!.backgroundColor = UIColor.clearColor()
            cell!.textLabel?.textColor = UIColor.darkGrayColor()
            let selectedBackgroundView = UIView(frame: CGRectMake(0, 0, cell!.frame.size.width, cell!.frame.size.height))
            selectedBackgroundView.backgroundColor = UIColor.grayColor().colorWithAlphaComponent(0.2)
            cell!.selectedBackgroundView = selectedBackgroundView
        }
        
        cell!.textLabel?.text = pages[indexPath.row]
        //cell!.textLabel?.text = "Menüpunkt #\(indexPath.row+1)"
        return cell!
    }
    
    override func tableView(tableView: UITableView, heightForRowAtIndexPath indexPath: NSIndexPath) -> CGFloat {
        return 50.0
    }
    
    override func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
        
        if (indexPath.row == selectedMenuItem) {
            return
        }
        selectedMenuItem = indexPath.row
        
        //Present new view controller
        let mainStoryboard: UIStoryboard = UIStoryboard(name: "Main",bundle: nil)
        var destViewController : UIViewController
        
        //var pages : [String] = ["Kamera", "Farben", "Konfiguration", "Info", "Start"]
        switch (indexPath.row) {
        case 0:
            destViewController = mainStoryboard.instantiateViewControllerWithIdentifier("main") as UIViewController
            break
        case 1:
            destViewController = mainStoryboard.instantiateViewControllerWithIdentifier("colour") as UIViewController
            break
        case 2:
            destViewController = mainStoryboard.instantiateViewControllerWithIdentifier("config") as UIViewController
            break
        case 3:
            destViewController = mainStoryboard.instantiateViewControllerWithIdentifier("cam") as UIViewController
            break
        default:
            destViewController = mainStoryboard.instantiateViewControllerWithIdentifier("info") as UIViewController
            break
        }
        sideMenuController()?.setContentViewController(destViewController)
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepareForSegue(segue: UIStoryboardSegue!, sender: AnyObject!) {
        // Get the new view controller using [segue destinationViewController].
        // Pass the selected object to the new view controller.
    }
    */

}
