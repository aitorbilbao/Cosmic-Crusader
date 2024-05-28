from map_info import *

#This is the dictionary of levels. It works for:
# - position of nodes
# - images for each level map
# - map info
# - level to be unlocked if finished


level_0 = {'node_pos': (110,400),
            'unlock': 1,
            'map': level0,
            'map_bc': level0_bc,
            'image': level_image,
            'graphics': "../backgrounds/Terran.png" 
            }

level_1 = {'node_pos': (290,500),
            'unlock': 2,
            'map': level1,
            'map_bc': level1_bc,
            'image': level_image,
            'graphics': "../backgrounds/Baren.png" 
            }

level_2 = {'node_pos': (490,220),
            'unlock': 3,
            'map': level2,
            'map_bc': level2_bc,
            'image': level_image,
            'graphics': "../backgrounds/Ice.png" 
            }

level_3 = {'node_pos': (580,610),
            'unlock': 4,
            'map': level3,
            'map_bc': level3_bc,
            'image': level_image,
            'graphics': "../backgrounds/Lava.png" 
            }

level_4 = {'node_pos': (730,350),
            'unlock': 5,
            'map': level4,
            'map_bc': level4_bc,
            'image': level_image,
            'graphics': "../backgrounds/ship0.png" 
            }

level_5 = {'node_pos': (930,210),
            'unlock': 6,
            'map': level5,
            'map_bc': level5_bc,
            'image': level_image,
            'graphics': "../backgrounds/ship.png" 
            }

level_6 = {'node_pos': (1090,400),
            'unlock': 6,
            'map': level6,
            'map_bc': level6_bc,
            'image': level_image,
            'graphics': "../backgrounds/Black_hole.png" 
            }


levels = {
    0: level_0,
    1: level_1,
    2: level_2,
    3: level_3,
    4: level_4,
    5: level_5,
    6: level_6 }