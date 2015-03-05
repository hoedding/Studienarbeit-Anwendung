//
//  ConnectServer.swift
//  Studienarbeit
//
//  Created by Timo Höting on 03.01.15.
//  Copyright (c) 2015 Timo Höting. All rights reserved.
//

import Foundation
import Security
import UIKit

class ConnectServerTCP : NSObject, NSStreamDelegate, NSURLSessionDelegate, NSURLSessionTaskDelegate  {

 /*   private var inputstream : NSInputStream!
    private var outputstream : NSOutputStream!
    private var host : String = ""
    private var port : UInt32 = 0
    var connected : Bool = false
    var errorOccured : Bool = false

    func initWithData(_host : NSString, _port : UInt32) {
        host = _host
        port = _port
    }
    
    func connect() {
        errorOccured = false
        
        var readstream : Unmanaged<CFReadStream>?
        var writestream : Unmanaged<CFWriteStream>?
        CFStreamCreatePairWithSocketToHost(kCFAllocatorDefault, host, port, &readstream, &writestream)
        
        inputstream = readstream!.takeRetainedValue()
        outputstream = writestream!.takeRetainedValue()
        
        inputstream.delegate = self
        outputstream.delegate = self
        
        inputstream.scheduleInRunLoop(NSRunLoop.currentRunLoop(), forMode: NSDefaultRunLoopMode)
        outputstream.scheduleInRunLoop(NSRunLoop.currentRunLoop(), forMode: NSDefaultRunLoopMode)
        
        inputstream.open()
        outputstream.open()
        if ( !errorOccured ) {
            connected = true
        }
    }
    
    func clearLED(){
        var message = createMessageStringWith(globalDataManager.getUserName(), globalDataManager.getPasswordHash(), "X00","", "", "", "", "", "", "", "", "")
        globalConnection.sendMessageViaHttpPost(false, message: message)
    }
    
    func allLEDoneColour(ident : Int) {
        var red = ident & 0b111111110000000000000000
        var green = ident & 0b0000000111111100000000
        var blue = ident & 0b000000000000000011111111
        red = red >> 16
        green = green >> 8
        var message = createMessageStringWith(globalDataManager.getUserName(), globalDataManager.getPasswordHash(), "X03", "", "", "", String(red), String(green), String(blue), "", "", "")
        globalConnection.sendMessageViaHttpPost(false, message: message)
    }
    
    func recvConfigFromServer() {
        var message = createMessageStringWith(globalDataManager.getUserName(), globalDataManager.getPasswordHash(), "X06", "", "", "", "", "", "", "", "", "")
        var response = globalConnection.sendMessageViaHttpPost(true, message: message)
        if response.containsString("STATUS:") {
            response = response.stringByReplacingOccurrencesOfString("STATUS:", withString: "")
            self.manageRecvdConfigData(response)
        }
    }
    
    func setModus ( mod : Int ) {
        var message = createMessageStringWith(globalDataManager.getUserName(), globalDataManager.getPasswordHash(), "X05","", "", "", "", "", "", String(mod), "", "")
        globalConnection.sendMessageViaHttpPost(false, message: message)
        globalDataManager.changeValueWithEntityName("Config", key: "modus", value: String(mod))
    }
    
    func setNewPw ( pw : String ) {
        var message = createMessageStringWith(globalDataManager.getUserName(), globalDataManager.getPasswordHash(), "X08","", "", "", "", "", "", "", "", "pw--"+pw)
        globalConnection.sendMessageViaHttpPost(false, message: message)
    }
    
    func changeConfigOnServerWith(key : String, value: String) {
        var message = createMessageStringWith(globalDataManager.getUserName(), globalDataManager.getPasswordHash(), "X08","", "", "", "", "", "", "", "", key + "--" + value)
        globalConnection.sendMessageViaHttpPost(false, message: message)
    }
    
    func checkIfAuthIsCorrect() -> Bool {
        var message = createMessageStringWith(globalDataManager.getUserName(), globalDataManager.getPasswordHash(), "X09","", "", "", "", "", "", "", "", "")
        var response = globalConnection.sendMessageViaHttpPost(true, message: message)
        if response.containsString("TRUE") {
            return true
        }
        return false
    }
    
    func createMessageStringWith(user : String, _ pass : String,_ control : String, _ ledNo : String, _ rangeStart : String, _ rangeEnd : String, _ red : String, _ green : String, _ blue : String, _ modus : String, _ effectcode : String, _ config : String) -> String {
        var s = ":"
        var data =  user + s + pass + s + control + s +  ledNo + s + rangeStart + s + rangeEnd + s + red + s + green + s + blue + s + modus + s + effectcode + s + config + s
        var checksum = globalDataManager.hashStringWithSHA224(data)
        var message = data + checksum 
        return message
    }
    
    internal func stream(aStream: NSStream, handleEvent eventCode: NSStreamEvent) {
        switch (eventCode){
        case NSStreamEvent.ErrorOccurred:
            errorOccured = true
            NSLog("ErrorOccurred")
            break
        case NSStreamEvent.EndEncountered:
            NSLog("EndEncountered")
            break
        case NSStreamEvent.None:
            NSLog("None")
            break
        case NSStreamEvent.HasBytesAvailable:
            NSLog("HasBytesAvaible")
            var buffer = [Byte](count: 1024, repeatedValue: 0)
            if ( aStream == inputstream ){

                while (inputstream.hasBytesAvailable){
                    var len = inputstream.read(&buffer, maxLength: buffer.count)

                    if(len > 0){

                        var output = NSString(bytes: &buffer, length: buffer.count, encoding: NSUTF8StringEncoding)

                        if (output != ""){
                            NSLog("server said: %@", output!)
                            output = output?.stringByReplacingOccurrencesOfString("\n", withString: "")
                            output = output?.stringByReplacingOccurrencesOfString("\r", withString: "")
                            manageRecvdConfigData(output!)
                        }
                    }
                }
            }
            break
        case NSStreamEvent.allZeros:
            NSLog("allZeros")
            break
        case NSStreamEvent.OpenCompleted:
            NSLog("OpenCompleted")
            break
        case NSStreamEvent.HasSpaceAvailable:
            NSLog("HasSpaceAvailable")
            break
        default:
            NSLog("unknown.")
        }
    }
    
    func disconnect() {
        inputstream.close()
        outputstream.close()
        connected = false
    }
    
    private func manageRecvdConfigData(data : NSString) {
        var err : NSError? = nil
        var jsonData = data.dataUsingEncoding(NSUTF8StringEncoding, allowLossyConversion: true)
        NSLog("%@", data)
        var jsonResult : NSDictionary = NSJSONSerialization.JSONObjectWithData(jsonData!, options: NSJSONReadingOptions.AllowFragments, error: &err) as NSDictionary
 
        if ( err == nil ) {
            globalDataManager.changeValueWithEntityName("Config", key: "ledcount", value: jsonResult["ledcount"] as String)
            globalDataManager.changeValueWithEntityName("Config", key: "motionport1", value: jsonResult["motionport1"] as String)
            globalDataManager.changeValueWithEntityName("Config", key: "motionport2", value: jsonResult["motionport2"] as String)
            globalDataManager.changeValueWithEntityName("Config", key: "ftp_url", value: jsonResult["ftp_url"] as String)
            globalDataManager.changeValueWithEntityName("Config", key: "camavaible", value: jsonResult["camavaible"] as String)
            globalDataManager.changeValueWithEntityName("Config", key: "cam_url", value: jsonResult["cam_url"] as String)
            globalDataManager.changeValueWithEntityName("Config", key: "cam_url_short", value: jsonResult["cam_url_short"] as String)
            globalDataManager.changeValueWithEntityName("Config", key: "timeperiod", value: jsonResult["timeperiod"] as String)
        }
    }
    
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
    
    
    func sendMessageViaHttpPost(expectResponse: Bool, message : String) -> NSString {
        var result : NSString = ""
        let server = "https://" + globalDataManager.loadValue("Config", key: "host") + ":" + globalDataManager.loadValue("Config", key: "port") + "/serv"
        let request = NSMutableURLRequest(URL: NSURL(string: server)!)
        request.HTTPMethod = "POST"
        let postString = "data=" + message
        request.HTTPBody = postString.dataUsingEncoding(NSUTF8StringEncoding)

        var configuration = NSURLSessionConfiguration.defaultSessionConfiguration()
        var session = NSURLSession(configuration: configuration, delegate: self, delegateQueue: NSOperationQueue.mainQueue())
        var task = session.dataTaskWithRequest(request) {
                 data, response, error in
            if !expectResponse {
                return
            }
            if error != nil {
                println("error=\(error)")
                return
            }
            result = NSString(data: data, encoding: NSUTF8StringEncoding)!
        }
        task.resume()
        return result
    }*/
}