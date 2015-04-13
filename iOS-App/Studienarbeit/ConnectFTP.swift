//
//  ConnectFTP.swift
//  Studienarbeit
//
//  Created by Timo Höting on 12.02.15.
//  Copyright (c) 2015 Timo Höting. All rights reserved.
//

import Foundation

class ConnectFTP : NSObject, WRRequestDelegate{
    
    var linkList = [NSString]()
    var dateList = [CFDateRef]()
    
//    func OpenAndTestFTPConn(user:NSString, pass:NSString) {
//        var ftpstring = "ftp://\(user):\(pass)@192.168.2.200/"
//        var ftpNSURL = NSURL(string: ftpstring)
//        var FTPStream = CFReadStreamCreateWithFTPURL(nil, ftpNSURL).takeRetainedValue()
//        CFReadStreamOpen(FTPStream)
//        
//        var buffer = [Byte](count: 4096, repeatedValue: 0)
//        CFReadStreamRead(FTPStream, &buffer, buffer.count)
//        var listing : Unmanaged<CFDictionary>?
//        var test2 = CFFTPCreateParsedResourceListing(kCFAllocatorDefault, &buffer, buffer.count, &listing)
//        var test3 = listing?.takeRetainedValue()
//        var count = CFDictionaryGetCount(test3)
//        
//        var keys  = UnsafeMutablePointer<UnsafePointer<Void>>.alloc(10)
//        keys.initialize(nil)
//        var t : CFTypeRef
//        var values : UnsafeMutablePointer<UnsafePointer<Void>> = UnsafeMutablePointer()
//        var context : UnsafeMutablePointer<UnsafePointer<Void>> = UnsafeMutablePointer()
//        
//        CFDictionaryGetKeysAndValues(test3, keys, values)
//        
//    }
    
    func getFileNameList() -> [NSString]{
        return linkList
    }
    
    func getDateList() -> [CFDateRef]{
        return dateList
    }
    
    func reset(){
        linkList.removeAll(keepCapacity: false)
        dateList.removeAll(keepCapacity: false)
    }
    
    func requestCompleted (request : WRRequest) {
        println("list complete")
        var listDirectory = request as WRRequestListDirectory
        for file in listDirectory.filesInfo {
            println(file.objectForKey(kCFFTPResourceName))
            
            var objectName = file.objectForKey(kCFFTPResourceName) as NSString
            var objectDate = file.objectForKey(kCFFTPResourceModDate) as CFDateRef
            println(objectDate)
            linkList.append(objectName)
            dateList.append(objectDate)
        }
    }
    
    func requestFailed (request : WRRequest) {
        println("failed")
    }
    
    func loadFTPFirectory(){
        reset()
        var hostname = globalDataManager.loadValue("UserSettings", key: "ftp")
        var dir = globalDataManager.loadValue("UserSettings", key: "ftpdir")
        var user = globalDataManager.loadValue("UserSettings", key: "ftpuser")
        var password = globalDataManager.loadValue("UserSettings", key: "ftppassword")
        println(dir + "/safe/")
        
        var listDirectory = WRRequestListDirectory()
        listDirectory.delegate = self
        listDirectory.hostname = hostname
        listDirectory.username = user
        listDirectory.password = password
        listDirectory.path = dir + "/safe/"
        listDirectory.start()
    }
}