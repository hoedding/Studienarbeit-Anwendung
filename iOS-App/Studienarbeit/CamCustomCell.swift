//
//  CamCustomCell.swift
//  Studienarbeit
//
//  Created by Timo Höting on 26.01.15.
//  Copyright (c) 2015 Timo Höting. All rights reserved.
//

import Foundation
import UIKit

class CamCustomCell : UITableViewCell {
    
    @IBOutlet var cell_imageview: UIImageView!
    @IBOutlet var cell_lable: UILabel!
    @IBOutlet weak var cell_date: UILabel!
    
    
    required init(coder aDecoder: NSCoder) {
        super.init(coder: aDecoder)
        cell_imageview = UIImageView()
    }
    
    override init(style: UITableViewCellStyle, reuseIdentifier: String!) {
        super.init(style: style, reuseIdentifier: reuseIdentifier)
    }
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }
    
    override func setSelected(selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)
        // Configure the view for the selected state
    }
    

    
}