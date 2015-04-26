import UIKit
import XCPlayground


let url = NSURL(string: "http://192.168.2.5/tmpfs/auto.jpg")
let data = NSData(contentsOfURL: url!)
var image = UIImage(data: data!)
var i = image?.description
var view = UIImageView(image: image)

