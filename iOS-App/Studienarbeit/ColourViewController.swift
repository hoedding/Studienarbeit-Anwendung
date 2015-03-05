//
//  ColourViewController.swift
//  Studienarbeit
//
//  Created by Timo Höting on 09.01.15.
//  Copyright (c) 2015 Timo Höting. All rights reserved.
//

import UIKit

class  ColourViewController: UIViewController  {
    
    override func viewDidLoad() {
        super.viewDidLoad()
        createColourButtons()
        createBlackoutButton()
        createWhiteButton()
        createLEDStripe()
        createEffectButtons()
        createEffectButtons()
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    @IBAction func reloadView(sender: UIButton) {
        createLEDStripe()
    }
    
    // MARK: Create UI Elements

    func createColourButtons() {
        // Mit diesen Buttons werden alle LEDs in einer Farbe angeschaltet
        let colourList : [UIColor] = [UIColor.redColor(), UIColor.greenColor(), UIColor.blueColor(), UIColor.yellowColor(), UIColor.orangeColor(), UIColor.brownColor(),  UIColor(red: 255.0, green: 255.0, blue: 255.0, alpha: 1.0)]

        let positionList : [CGPoint] = [CGPoint(x: 10, y: 70), CGPoint(x: 70, y: 70), CGPoint(x: 130, y: 70), CGPoint(x: 190, y: 70), CGPoint(x: 250, y: 70), CGPoint(x: 310, y: 70), CGPoint(x: 200, y: 150), CGPoint(x: 250, y: 150)]
        
        // Buttons für Farben hinzufügen
        for e in 0..<colourList.count {
            let imageSize = CGSize(width: 52, height: 52)
            let imageView = UIImageView(frame: CGRect(origin: positionList[e], size: imageSize))
            imageView.userInteractionEnabled = true
            
            let singleTap = UITapGestureRecognizer(target: self, action: "gesture:")
            singleTap.numberOfTapsRequired = 1
            
            imageView.addGestureRecognizer(singleTap)
            
            self.view.addSubview(imageView)
            var colours = CGColorGetComponents(colourList[e].CGColor)
            let image = drawCircle(size: imageSize, colours: colours, Scale: nil)
            
            var r : Int = Int(colours[0]*255.0) << 16
            var g : Int = Int(colours[1]*255.0) << 8
            var b : Int = Int(colours[2]*255.0)
            var rgb : Int = r | g | b
            imageView.tag = rgb

            imageView.image = image
        }
    }
    
    func createWhiteButton(){
        // Dieses Button setzt alle LEDs auf die Farbe weis
        let imageSize = CGSize(width: 170, height: 52)
        let imageView = UIImageView(frame: CGRect(origin: CGPoint(x: 10, y: 130), size: imageSize))
        imageView.userInteractionEnabled = true
        
        let singleTap = UITapGestureRecognizer(target: self, action: "gesture:")
        singleTap.numberOfTapsRequired = 1
        
        imageView.addGestureRecognizer(singleTap)
        self.view.addSubview(imageView)
        
        let image = drawRectangle(size: imageSize, colour: UIColor.whiteColor(), Scale: nil)
        
        imageView.tag = 16777215
        imageView.image = image
    }
    
    func createBlackoutButton(){
        // Dieses Button schaltet alle LEDs aus
        let imageSize = CGSize(width: 170, height: 52)
        let imageView = UIImageView(frame: CGRect(origin: CGPoint(x: 190, y: 130), size: imageSize))
        imageView.userInteractionEnabled = true
        
        let singleTap = UITapGestureRecognizer(target: self, action: "gesture:")
        singleTap.numberOfTapsRequired = 1
        
        imageView.addGestureRecognizer(singleTap)
        
        self.view.addSubview(imageView)
        //let image = drawCustomImage(imageSize)

        let image = drawRectangle(size: imageSize, colour: UIColor.blackColor(), Scale: nil)
        
        imageView.tag = 0
        
        imageView.image = image
    }
    
    func createEffectButtons(){
        // Hier werden die einzelnen Effekte definiert
        /*
        1: Strobo
        2: Bunte Farben
        */
        let effects = [1,2]
        for i in 0...effects.count-1{
            let imageSize = CGSize(width: 170, height: 52)
            let imageView = UIImageView(frame: CGRect(origin: CGPoint(x: 10 + (i*180), y: 190), size: imageSize))
            imageView.userInteractionEnabled = true
            let singleTap = UITapGestureRecognizer(target: self, action: "gestureeffect:")
            singleTap.numberOfTapsRequired = 1
            imageView.addGestureRecognizer(singleTap)
            self.view.addSubview(imageView)
            let image = drawRectangle(size: imageSize, colour: UIColor.grayColor(), Scale: nil)
            imageView.tag = effects[i]
            imageView.image = image
        }
    }
    
    func createLEDStripe() {
        // An dieser Stelle werden die aktuellen Farben der LEDs angezeigt
        var ledValues = globalDataManager.LedColours
        if (ledValues.count == 0) {
            //TODO Fehler ausgeben
            return
        }
        var colourList : [UIColor] = []
        let valueCount = ledValues.count
        for n in 0...valueCount - 1 {
            var temp_value = ledValues[n]
            var red = temp_value & 0b111111110000000000000000
            var green = temp_value & 0b0000000111111100000000
            var blue = temp_value & 0b000000000000000011111111
            red = red >> 16
            green = green >> 8
            var _red = CGFloat(red)
            var _blue = CGFloat(blue)
            var _green = CGFloat(green)
            colourList.append(UIColor(red: _red, green: _green, blue: _blue, alpha: 1.0))
        }
        var width = UIScreen.mainScreen().bounds.width
        var maxElements_float = ( width * 0.9 ) / 15
        var maxElements_int = Int(maxElements_float)
        var border = ( width - maxElements_float ) / 2
        var rows = valueCount / maxElements_int
        var rest = valueCount - (rows * maxElements_int)
        var count = 30
        
        for i in 0..<rows {
            // Es fehlen noch die Elemente "rest"
            for e in 0..<maxElements_int {
                // array[e+(i*maxElements_int)]
                var colour_temp = colourList[ e + ( i * maxElements_int ) ]
                let imageSize = CGSize(width: 15, height: 15)
                let imageView = UIImageView(frame: CGRect(origin: CGPoint(x: 15 + ( e * 15), y: 300 + (i * 15)), size: imageSize))
                imageView.userInteractionEnabled = false
                
                self.view.addSubview(imageView)
                var colours = CGColorGetComponents(colour_temp.CGColor)
                let image = drawCircle(size: imageSize, colours: colours, Scale: nil)
                imageView.image = image
            }
        }
    }
    
    // MARK: Drawing UIImages
    
    func drawCircle(#size: CGSize, colours : UnsafePointer<CGFloat>,Scale sca : CGFloat?) -> UIImage {
        // Setup our context
        let bounds = CGRect(origin: CGPoint.zeroPoint, size: size)
        let opaque = false
        var scale: CGFloat = 0
        if (sca != nil) { scale = sca! }
        
        UIGraphicsBeginImageContextWithOptions(size, opaque, scale)
        let context = UIGraphicsGetCurrentContext()
        
        CGContextBeginPath(context)
        CGContextSetRGBFillColor(context, colours[0], colours[1], colours[2], 1.0)
        CGContextFillEllipseInRect(context, CGRect(x: 1, y: 1, width: size.width-2, height: size.height-2))
        CGContextStrokePath(context)

        CGContextBeginPath(context)
        CGContextSetRGBFillColor(context, 1, 1, 1, 1)
        CGContextAddEllipseInRect(context, CGRect(x: 1, y: 1, width: size.width-2, height: size.height-2))
        CGContextStrokePath(context)
        
        let image = UIGraphicsGetImageFromCurrentImageContext()
        UIGraphicsEndImageContext()
        return image
        
    }
    
    func drawRectangle(#size: CGSize, colour : UIColor,Scale sca : CGFloat?) -> UIImage{
        let bounds = CGRect(origin: CGPoint.zeroPoint, size: size)
        let opaque = false
        var scale: CGFloat = 0
        if (sca != nil) { scale = sca! }
        
        UIGraphicsBeginImageContextWithOptions(size, opaque, scale)
        let context = UIGraphicsGetCurrentContext()
        
        CGContextBeginPath(context)

        CGContextSetFillColorWithColor(context, colour.CGColor)
        CGContextSetStrokeColorWithColor(context, UIColor.blackColor().CGColor)
        CGContextSetLineWidth(context, 2.0)
        
        CGContextFillRect(context, bounds)
        CGContextStrokeRect(context, bounds)
        
        let image = UIGraphicsGetImageFromCurrentImageContext()
        UIGraphicsEndImageContext()
        return image
    }
    
    // MARK: Gesture Recognizer
    
    func gesture(gestureRecognizer : UIGestureRecognizer){
        var m = gestureRecognizer.view?.tag
        globalConnection.lightAllLEDWith(m!)
        NSLog("gesture detected: %i", m!)
        globalConnection.getLEDStatusFromServer()
    }
    
    func gestureeffect(gestureRecognizer : UIGestureRecognizer){
        var m = gestureRecognizer.view?.tag
        NSLog("gesture detected: %i", m!)
        globalConnection.lightEffect(m!)
    }
    
}
