//
//  CoreDataManager.swift
//  Studienarbeit
//
//  Created by Timo Höting on 10.01.15.
//  Copyright (c) 2015 Timo Höting. All rights reserved.
//

import Foundation
import CoreData
import UIKit
import CryptoSwift

class CoreDataManager : NSObject {
    
    var LedColours : [Int] = []
    
    func insertNilConfig() {
        var err : NSError? = nil
        var appDel : AppDelegate = (UIApplication.sharedApplication().delegate as AppDelegate)
        var context : NSManagedObjectContext = appDel.managedObjectContext!
        
        var manObject = NSEntityDescription.insertNewObjectForEntityForName("Config", inManagedObjectContext: context) as NSManagedObject

        // Default Password ist admin/password
        manObject.setPrimitiveValue("admin", forKey: "user")
        manObject.setPrimitiveValue("password", forKey: "pw")
        manObject.setPrimitiveValue("", forKey: "host")
        manObject.setPrimitiveValue("", forKey: "port")
        manObject.setPrimitiveValue("", forKey: "ledcount")
        manObject.setPrimitiveValue("", forKey: "motionport1")
        manObject.setPrimitiveValue("", forKey: "motionport2")
       // manObject.setPrimitiveValue("", forKey: "ftp_url")
        manObject.setPrimitiveValue("", forKey: "camavaible")
        //manObject.setPrimitiveValue("", forKey: "cam_url")
        //manObject.setPrimitiveValue("", forKey: "cam_url_short")
        manObject.setPrimitiveValue("", forKey: "timeperiod")
        manObject.setPrimitiveValue("0", forKey: "modus")
        
        context.save(&err)
        if (err != nil) {
            println(err)
        }
    }
    
    func insertNilUserSettings() {
        var err : NSError? = nil
        var appDel : AppDelegate = (UIApplication.sharedApplication().delegate as AppDelegate)
        var context : NSManagedObjectContext = appDel.managedObjectContext!
        var manObject = NSEntityDescription.insertNewObjectForEntityForName("UserSettings", inManagedObjectContext: context) as NSManagedObject
        manObject.setPrimitiveValue("0", forKey: "authWithoutPW")
        manObject.setPrimitiveValue("", forKey: "ftp")
        manObject.setPrimitiveValue("", forKey: "ftpdir")
        manObject.setPrimitiveValue("", forKey: "ftpuser")
        manObject.setPrimitiveValue("", forKey: "ftppassword")
        context.save(&err)
        if (err != nil) {
            println(err)
        }
    }
    
    func loadValue(entityName : String, key : String) -> String {
        var err : NSError? = nil
        var appDel : AppDelegate = (UIApplication.sharedApplication().delegate as AppDelegate)
        var context : NSManagedObjectContext = appDel.managedObjectContext!
        var request = NSFetchRequest(entityName: entityName)
        request.returnsObjectsAsFaults = false
        
        var result : Array = context.executeFetchRequest(request, error: &err)! as Array
        var value: String = ""

        if (result.count > 0 ){
            for res in result{
                if ( res.valueForKey(key) == nil ){
                    return ""
                }
                value = res.valueForKey(key)! as String
            }
        }
        return value
    }
    
    func changeValueWithEntityName(entityName : String, key : String, value : AnyObject) {
        var err : NSError? = nil
        var appDel : AppDelegate = (UIApplication.sharedApplication().delegate as AppDelegate)
        var context : NSManagedObjectContext = appDel.managedObjectContext!
        var request = NSFetchRequest(entityName: entityName)
        request.returnsObjectsAsFaults = false
        
        var result : Array = context.executeFetchRequest(request, error: nil)! as Array
        
        if (result.count == 1){
            for res in result {
                res.setValue(value, forKey: key)
            }
        }
        
        context.save(&err)

        if (err != nil) {
            println(err)
        }
    }
    
    func safeNewPassword(p : String) {
        let hash = hashStringWithSHA224(p)
        changeValueWithEntityName("Config", key: "pw", value: hash)
    }
    
    func hashStringWithSHA224(value : NSString) -> String {

        let data = value.dataUsingEncoding(NSUTF8StringEncoding)

        let hash = CryptoSwift.Hash.sha224(data!).calculate()?.hexString

        return hash!
    }
    
    func deleteConfig( entityName : String ) {
        var appDel : AppDelegate = (UIApplication.sharedApplication().delegate as AppDelegate)
        var context : NSManagedObjectContext = appDel.managedObjectContext!
        var request = NSFetchRequest(entityName: entityName)
        request.returnsObjectsAsFaults = false
        var result : Array = context.executeFetchRequest(request, error: nil)! as Array
        if (result.count > 0){
            for res in result {
                context.deleteObject(res as NSManagedObject)
            }
        }
        context.save(nil)
    }
    
    func countElementsInEntity( entityName : String ) -> Int {
        var appDel : AppDelegate = (UIApplication.sharedApplication().delegate as AppDelegate)
        var context : NSManagedObjectContext = appDel.managedObjectContext!
        var request = NSFetchRequest(entityName: entityName)
        request.returnsObjectsAsFaults = false
        var result : Array = context.executeFetchRequest(request, error: nil)! as Array
        var count = 0
        if (result.count > 0){
            for res in result {
                count++
            }
        }
        return count
    }
    
    func getServerHost() -> String {
        return loadValue("Config", key: "host")
    }
    
    func getServerPort() -> UInt32 {
        var port = loadValue("Config", key: "port").toInt()
        return UInt32(port!)
    }
    
    func getUserName() -> String {
        return self.loadValue("Config", key: "user")
    }
    
    func getPasswordHash() -> String {
        return self.loadValue("Config", key: "pw")
    }
    
    func checkLocalCredetials(user : NSString, pw : NSString) -> Bool {
        if (self.loadValue("Config", key: "user") != user || self.loadValue("Config", key: "pw") != pw){
            return false
        }
        return true
    }
}


