//
//  CamViewController.swift
//  Studienarbeit
//
//  Created by Timo Höting on 09.01.15.
//  Copyright (c) 2015 Timo Höting. All rights reserved.
//

import UIKit

class  CamViewController: UIViewController, WRRequestDelegate  {
    
    @IBOutlet var tableView: UITableView!
    var refreshControl : UIRefreshControl!

    var imageList : [ImageObject?] = []
    var linkList = [NSString]()
    var dateList = [CFDateRef]()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        initRefreshControl()
        loadImageList()
    }
    
    func initRefreshControl(){
      // self.refreshControl = UIRefreshControl()
       // self.refreshControl?.addTarget(self, action: "loadImageList", forControlEvents: UIControlEvents.ValueChanged)
//        refreshControl?.tintColor = UIColor.grayColor()
        //refreshControl?.attributedTitle = "Pull to refresh."
        
    }
    
    func requestCompleted (request : WRRequest) {

        var downloadFile = request as WRRequestDownload
        var image = UIImage(data: downloadFile.receivedData)
        let dateFormatter = NSDateFormatter()
        dateFormatter.dateFormat = "dd-MM-yyyy HH:mm"
        //var date = dateFormatter.stringFromDate(dateList[counter])
        
        imageList.append(ImageObject(filename: /*linkList[counter]*/ "", title: /*date*/ "", image: image!))
        tableView.reloadData()
    }
    
    func requestFailed (request : WRRequest) {
        println("failed")
    }

    var counter = 0
    func loadImageList(){
        
        linkList = globalFtp.getFileNameList()
        dateList = globalFtp.getDateList()
        
        if (linkList.count == 0 || dateList.count == 0 ){
            AlertWindow().alert(self, title: "FTP-Verbindung nicht verfügbar.", message: "Bitte überprüfen Sie ihre FTP-Konfiguration!")
            return
        }
        
        counter = 0
        for i in 0...linkList.count-1 {
                var downloadFile = WRRequestDownload()
                downloadFile.delegate = self
                downloadFile.hostname = "192.168.2.200"
                downloadFile.username = "admin"
                downloadFile.password = "Mareike2"
                downloadFile.path = "/Home/Cam/" + linkList[i]
                downloadFile.start()
                counter++
        }
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return imageList.count
    }
    
    func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {

        let identifier = "CamCustomCell"
        var cell: CamCustomCell! = tableView.dequeueReusableCellWithIdentifier(identifier) as? CamCustomCell
        if cell == nil {
            tableView.registerNib(UINib(nibName: "CamCustomCell", bundle: nil), forCellReuseIdentifier: identifier)
            cell = tableView.dequeueReusableCellWithIdentifier(identifier) as? CamCustomCell
        }
        let height = cell.bounds.size.height
        let width = cell.bounds.size.width
        let border = (height * 0.1) / 2
        
        if imageList.count == 0 {
            return cell
        }
        if let imageobject = imageList[indexPath.row] {
            var imageview = UIImageView(frame: CGRect(x: border, y: border, width: width / 3, height: height * 0.9))
            imageview.image = imageobject.getImage()
            imageview.backgroundColor = UIColor.greenColor()
            cell.addSubview(imageview)
            cell.cell_lable.text = "" // imageobject._title
            cell.cell_date.text = "" //imageobject._filename
        }
        
        return cell
        
    }
    
    func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
        
        initPhotoView(indexPath.row)
        
    }
    
    var photoview : VIPhotoView!
    func initPhotoView(row : Int){
        var image = imageList[row]?._image
        photoview = VIPhotoView(frame: self.view.bounds, andImage: image)
        
        var btn = UIButton(frame: CGRect(x: 10, y: 10, width: 100, height: 30))
        btn.backgroundColor = UIColor.grayColor()
        btn.addTarget(self, action: "closePhotoView", forControlEvents: UIControlEvents.AllTouchEvents)
        photoview.addSubview(btn)
        
        self.view.addSubview(photoview)
        
    }
    
    func closePhotoView(){
        photoview.removeFromSuperview()
    }
    


}
