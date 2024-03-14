from production import IF, AND, THEN, FAIL, OR  # for zookeeper rules


# data sets for transitive_rule

poker_data = [ 'two-pair beats pair',
               'three-of-a-kind beats two-pair',
               'straight beats three-of-a-kind',
               'flush beats straight',
               'full-house beats flush',
               'straight-flush beats full-house' ]

abc_data = [ 'a beats b', 'b beats c' ]

minecraft_data = [ 'diamond-sword beats diamond-axe',
                   'stone-pick beats stone-shovel',
                   'diamond-axe beats iron-axe',
                   'iron-axe beats stone-shovel',
                   'iron-pick beats stone-pick',
                   'iron-axe beats iron-pick',
                   'stone-shovel beats fist' ]


# data sets for family_rules

simpsons_data = ("person bart",
                 "person lisa",
                 "person maggie",
                 "person marge",
                 "person homer",
                 "person abe",
                 "parent marge bart",
                 "parent marge lisa",
                 "parent marge maggie",
                 "parent homer bart",
                 "parent homer lisa",
                 "parent homer maggie",
                 "parent abe homer")

black_data = ("person sirius",
              "person regulus",
              "person walburga",
              "person alphard",
              "person cygnus",
              "person pollux",
              "person bellatrix",
              "person andromeda",
              "person narcissa",
              "person nymphadora",
              "person draco",
              "parent walburga sirius",
              "parent walburga regulus",
              "parent pollux walburga",
              "parent pollux alphard",
              "parent pollux cygnus",
              "parent cygnus bellatrix",
              "parent cygnus andromeda",
              "parent cygnus narcissa",
              "parent andromeda nymphadora",
              "parent narcissa draco")

sibling_test_data = [ 'person mario',
                      'person luigi',
                      'person papa',
                      'parent papa mario',
                      'parent papa luigi' ]

grandparent_test_data = [ 'person jay',
                          'person claire',
                          'person alex',
                          'parent jay claire',
                          'parent claire alex' ]

anonymous_family_test_data = [ 'person a1', 'person b1', 'person b2',
                               'person c1', 'person c2', 'person c3',
                               'person c4', 'person d1', 'person d2',
                               'person d3', 'person d4',
                               'parent a1 b1',
                               'parent a1 b2',
                               'parent b1 c1',
                               'parent b1 c2',
                               'parent b2 c3',
                               'parent b2 c4',
                               'parent c1 d1',
                               'parent c2 d2',
                               'parent c3 d3',
                               'parent c4 d4' ]

# rules and data for zookeeper

zookeeper_rules = (

    IF( AND( '(?x) has hair' ),         # Z1
        THEN( '(?x) is a mammal' )),

    IF( AND( '(?x) gives milk' ),       # Z2
        THEN( '(?x) is a mammal' )),

    IF( AND( '(?x) has feathers' ),     # Z3
        THEN( '(?x) is a bird' )),

    IF( AND( '(?x) flies',              # Z4
             '(?x) lays eggs' ),
        THEN( '(?x) is a bird' )),

    IF( AND( '(?x) is a mammal',        # Z5
             '(?x) eats meat' ),
        THEN( '(?x) is a carnivore' )),

    IF( AND( '(?x) is a mammal',        # Z6
             '(?x) has pointed teeth',
             '(?x) has claws',
             '(?x) has forward-pointing eyes' ),
        THEN( '(?x) is a carnivore' )),

    IF( AND( '(?x) is a mammal',        # Z7
             '(?x) has hoofs' ),
        THEN( '(?x) is an ungulate' )),

    IF( AND( '(?x) is a mammal',        # Z8
             '(?x) chews cud' ),
        THEN( '(?x) is an ungulate' )),

    IF( AND( '(?x) is a carnivore',     # Z9
             '(?x) has tawny color',
             '(?x) has dark spots' ),
        THEN( '(?x) is a cheetah' )),

    IF( AND( '(?x) is a carnivore',     # Z10
             '(?x) has tawny color',
             '(?x) has black stripes' ),
        THEN( '(?x) is a tiger' )),

    IF( AND( '(?x) is an ungulate',     # Z11
             '(?x) has long legs',
             '(?x) has long neck',
             '(?x) has tawny color',
             '(?x) has dark spots' ),
        THEN( '(?x) is a giraffe' )),

    IF( AND( '(?x) is an ungulate',     # Z12
             '(?x) has white color',
             '(?x) has black stripes' ),
        THEN( '(?x) is a zebra' )),

    IF( AND( '(?x) is a bird',          # Z13
             '(?x) does not fly',
             '(?x) has long legs',
             '(?x) has long neck',
             '(?x) has black and white color' ),
        THEN( '(?x) is an ostrich' )),

    IF( AND( '(?x) is a bird',          # Z14
             '(?x) does not fly',
             '(?x) swims',
             '(?x) has black and white color' ),
        THEN( '(?x) is a penguin' )),

    IF( AND( '(?x) is a bird',        # Z15
             '(?x) is a good flyer' ),
        THEN( '(?x) is an albatross' )),

    )

zoo_data = [ 'tim has feathers',
             'tim is a good flyer',
             'mark flies',
             'mark does not fly',
             'mark lays eggs',
             'mark swims',
             'mark has black and white color' ]
