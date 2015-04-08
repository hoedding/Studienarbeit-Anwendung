//
//  ImageObject.swift
//  Studienarbeit
//
//  Created by Timo Höting on 10.03.15.
//  Copyright (c) 2015 Timo Höting. All rights reserved.
//

import Foundation
import UIKit

class ImageObject {
    var _filename : NSString
    var _title : NSString
    var _image : UIImage
    
    init (filename : NSString, title : NSString, image : UIImage?) {
        _filename = filename
        _title = title
        _image = image!
    }
    
    func getImage() -> UIImage {
        return _image
    }
    
}