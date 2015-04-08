//
//  ConnectServerHTTP.swift
//  Studienarbeit
//
//  Created by Timo Höting on 20.02.15.
//  Copyright (c) 2015 Timo Höting. All rights reserved.
//

import Foundation
import Security
import UIKit

enum ProtocolType {
    case CLEAR
    case ONELED
    case LEDRANGE
    case ALLLED
    case EFFECT
    case MODUS
    case SYSTEMSTATUS
    case LEDSTATUS
    case CONFIG
    case AUTH
}

class ConnectServerHTTP : NSObject, NSStreamDelegate, NSURLSessionDelegate, NSURLSessionTaskDelegate   {
    
    var connection_avaible : Bool = false
    var connection_established : Bool = false
    var loggedin = false
    var server = ""
    
    // MARK: Initialisation
    
    func initServerConnection(){
        let host = globalDataManager.loadValue("Config", key: "host")
        let port = globalDataManager.loadValue("Config", key: "port")
        server = "https://" + host + ":" + port + "/serv"
    }
    
    // MARK: Protocol implementation
    
    func clearLED(){
        let message = createMessageStringWith(ProtocolType.CLEAR,"", "", "", "", "", "", "", "", "")
        globalConnection.sendMessageViaHttpPost(false, message: message)
    }
    
    func lightOneLEDinRangeWith(colourIdent : Int, number : Int) {
        var red = colourIdent & 0b111111110000000000000000
        var green = colourIdent & 0b0000000111111100000000
        var blue = colourIdent & 0b000000000000000011111111
        red = red >> 16
        green = green >> 8
        var message = createMessageStringWith(ProtocolType.ONELED, "", String(number), "", "", "", "", "", "", "")
        globalConnection.sendMessageViaHttpPost(false, message: message)
    }
    
    
    func lightLEDinRangeWith(colourIdent : Int, start : Int, end: Int) {
        var red = colourIdent & 0b111111110000000000000000
        var green = colourIdent & 0b0000000111111100000000
        var blue = colourIdent & 0b000000000000000011111111
        red = red >> 16
        green = green >> 8
        var message = createMessageStringWith(ProtocolType.LEDRANGE, "", String(start), String(end), String(red), String(green), String(blue), "", "", "")
        globalConnection.sendMessageViaHttpPost(false, message: message)
    }
    
    func lightAllLEDWith(colourIdent : Int) {
        var red = colourIdent & 0b111111110000000000000000
        var green = colourIdent & 0b0000000111111100000000
        var blue = colourIdent & 0b000000000000000011111111
        red = red >> 16
        green = green >> 8
        var message = createMessageStringWith(ProtocolType.ALLLED, "", "", "", String(red), String(green), String(blue), "", "", "")
        globalConnection.sendMessageViaHttpPost(false, message: message)
    }
    
    func getSystemStatusFromServer() {
        var message = createMessageStringWith(ProtocolType.SYSTEMSTATUS, "", "", "", "", "", "", "", "", "")
        self.sendMessageViaHttpPostWithCompletion(message) { (answer : NSString) in
            if answer.containsString("STATUS:") {
                NSOperationQueue.mainQueue().addOperationWithBlock() { () in
                    var s = answer.stringByReplacingOccurrencesOfString("STATUS:", withString: "")
                    self.manageRecvdConfigData(s)
                }
            }
        }
        
    }
    
    func getLEDStatusFromServer() {
        var message = createMessageStringWith(ProtocolType.LEDSTATUS, "", "", "", "", "", "", "", "", "")
        self.sendMessageViaHttpPostWithCompletion(message) { (answer : NSString) in
            if answer.containsString("LED:") {
                NSOperationQueue.mainQueue().addOperationWithBlock() { () in
                    var s = answer.stringByReplacingOccurrencesOfString("LED:{", withString: "{")
                    self.manageRecvdLEDData(s)
                }
            }
        }
    }
    
    func lightEffect(effectIdent : Int) {
        var message = createMessageStringWith(ProtocolType.EFFECT, "", "", "", "", "", "", "", String(effectIdent), "")
        globalConnection.sendMessageViaHttpPost(false, message: message)
    }
    
    func setNewModus(modus : Int) {
        var message = createMessageStringWith(ProtocolType.MODUS,"", "", "", "", "", "", String(modus), "", "")
        globalConnection.sendMessageViaHttpPost(false, message: message)
        globalDataManager.changeValueWithEntityName("Config", key: "modus", value: String(modus))
    }
    
    func changeConfigOnServerWith(key : String, value: NSString) {
        var message = createMessageStringWith(ProtocolType.CONFIG,"", "", "", "", "", "", "", "", key + "--" + value)
        globalConnection.sendMessageViaHttpPost(false, message: message)
    }
    
    func sendDeviceToken(){
        changeConfigOnServerWith("TOKEN", value: globalToken)
    }
    
    func checkIfInternetConnectionIsAvaible() -> Bool {
        if IJReachability.isConnectedToNetwork() {
            return true
        }
        return false
    }
    
    func checkIfAuthIsCorrect() {
        var message = createMessageStringWith(ProtocolType.AUTH,"", "", "", "", "", "", "", "", "")
        self.sendMessageViaHttpPostWithCompletion(message) { (answer : NSString) in
            if answer.containsString("LOGIN:TRUE") {
                NSOperationQueue.mainQueue().addOperationWithBlock() { () in
                    self.connection_established = true
                }
            }
        }
    }
    
    
    // MARK: Message generation
    
    func createMessageStringWith(protocolType : ProtocolType, _ ledNo : String, _ rangeStart : String, _ rangeEnd : String, _ red : String, _ green : String, _ blue : String, _ modus : String, _ effectcode : String, _ config : String) -> String {
        var c = ""
        switch protocolType {
        case .CLEAR: c = "X00"; break
        case .ONELED: c = "X01"; break
        case .LEDRANGE: c = "X02"; break
        case .ALLLED: c = "X03"; break
        case .EFFECT: c = "X04"; break
        case .MODUS: c = "X05"; break
        case .SYSTEMSTATUS: c = "X06"; break
        case .LEDSTATUS: c = "X07"; break
        case .CONFIG: c = "X08"; break
        case .AUTH: c = "X09"; break
        }
        let user = globalDataManager.getUserName()
        let pw = globalDataManager.getPasswordHash()
        var s = ":"
        var data =  user + s + pw + s + c + s +  ledNo + s + rangeStart + s + rangeEnd + s + red + s + green + s + blue + s + modus + s + effectcode + s + config + s
        var checksum = globalDataManager.hashStringWithSHA224(data)
        var message = data + checksum
        return message
    }
    
    func createMessageStringWithCredentials(protocolType : ProtocolType, _ user : String, _ pw : String, _ ledNo : String, _ rangeStart : String, _ rangeEnd : String, _ red : String, _ green : String, _ blue : String, _ modus : String, _ effectcode : String, _ config : String) -> String {
        var c = ""
        switch protocolType {
        case .CLEAR: c = "X00"; break
        case .ONELED: c = "X01"; break
        case .LEDRANGE: c = "X02"; break
        case .ALLLED: c = "X03"; break
        case .EFFECT: c = "X04"; break
        case .MODUS: c = "X05"; break
        case .SYSTEMSTATUS: c = "X06"; break
        case .LEDSTATUS: c = "X07"; break
        case .CONFIG: c = "X08"; break
        case .AUTH: c = "X09"; break
        }
        var s = ":"
        var data =  user + s + pw + s + c + s +  ledNo + s + rangeStart + s + rangeEnd + s + red + s + green + s + blue + s + modus + s + effectcode + s + config + s
        var checksum = globalDataManager.hashStringWithSHA224(data)
        var message = data + checksum
        return message
    }
    
    func disconnect() {
       globalConnection.connection_established = false
    }
    
    // MARK: Data Management
    
    private func manageRecvdConfigData(data : NSString) {
        var err : NSError? = nil
        var jsonData = data.dataUsingEncoding(NSUTF8StringEncoding, allowLossyConversion: true)
        NSLog("%@", data)
        var jsonResult : NSDictionary = NSJSONSerialization.JSONObjectWithData(jsonData!, options: NSJSONReadingOptions.AllowFragments, error: &err) as NSDictionary
        
        if ( err == nil ) {
            globalDataManager.changeValueWithEntityName("Config", key: "ledcount", value: jsonResult["ledcount"] as String)
            globalDataManager.changeValueWithEntityName("Config", key: "motionport1", value: jsonResult["motionport1"] as String)
            globalDataManager.changeValueWithEntityName("Config", key: "motionport2", value: jsonResult["motionport2"] as String)
            globalDataManager.changeValueWithEntityName("Config", key: "camavaible", value: jsonResult["camavaible"] as String)
            globalDataManager.changeValueWithEntityName("Config", key: "timeperiod", value: jsonResult["timeperiod"] as String)
        }
    }
    
    private func manageRecvdLEDData(data : NSString){
        var err : NSError? = nil
        var jsonData = data.dataUsingEncoding(NSUTF8StringEncoding, allowLossyConversion: true)
        var jsonResult : NSDictionary = NSJSONSerialization.JSONObjectWithData(jsonData!, options: NSJSONReadingOptions.AllowFragments, error: &err) as NSDictionary
        var jsonResultValues = jsonResult["led"] as [[String:String]]
        globalDataManager.LedColours.removeAll(keepCapacity: false)
        for led in jsonResultValues{
                var value_temp = led["l"]?.toInt()
                globalDataManager.LedColours.append(value_temp!)
            }
    }
    
    // MARK: Server Connection
    
    func sendMessageViaHttpPost(expectResponse: Bool, message : String) {
        self.initServerConnection()
        var result : NSString = ""
        if !IJReachability.isConnectedToNetwork() {
            return
        }
        let request = NSMutableURLRequest(URL: NSURL(string: server)!)
        request.HTTPMethod = "POST"
        let postString = "data=" + message
        request.HTTPBody = postString.dataUsingEncoding(NSUTF8StringEncoding)
        
        var configuration = NSURLSessionConfiguration.defaultSessionConfiguration()
        var session = NSURLSession(configuration: configuration, delegate: self, delegateQueue: NSOperationQueue.mainQueue())
        var task = session.dataTaskWithRequest(request) {
            data, response, error in
        }
        task.resume()
    }
    
    func sendMessageViaHttpPostWithCompletion(message : NSString, completionClosure : (s : NSString) -> ()) {
        self.initServerConnection()
        var result : NSString = ""
        if !IJReachability.isConnectedToNetwork() {
            
        }
        let request = NSMutableURLRequest(URL: NSURL(string: server)!)
        request.HTTPMethod = "POST"
        let postString = "data=" + message
        request.HTTPBody = postString.dataUsingEncoding(NSUTF8StringEncoding)
        
        var configuration = NSURLSessionConfiguration.defaultSessionConfiguration()
        var session = NSURLSession(configuration: configuration, delegate: self, delegateQueue: NSOperationQueue.mainQueue())
        var task = session.dataTaskWithRequest(request) {
            data, response, error in
            
            if error != nil {
                println("error=\(error)")
                return
            }
            result = NSString(data: data, encoding: NSUTF8StringEncoding)!
            completionClosure(s: result)
        }
        task.resume()
    }
    
    // MARK: Session Context
    
    func URLSession(session: NSURLSession,
        didReceiveChallenge challenge:
        NSURLAuthenticationChallenge,
        completionHandler:
        (NSURLSessionAuthChallengeDisposition,
        NSURLCredential!) -> Void) {
            completionHandler(
                NSURLSessionAuthChallengeDisposition.UseCredential,
                NSURLCredential(forTrust:
                    challenge.protectionSpace.serverTrust))
    }
    
    func URLSession(session: NSURLSession,
        task: NSURLSessionTask,
        willPerformHTTPRedirection response:
        NSHTTPURLResponse,
        newRequest request: NSURLRequest,
        completionHandler: (NSURLRequest!) -> Void) {
            var newRequest : NSURLRequest? = request
            completionHandler(newRequest)
    }

}




