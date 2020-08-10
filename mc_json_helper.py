import os
import json


class SerialHelper:
    path = 'input.json'
    langs_dictionairy = {}

    @staticmethod
    def read():
        if os.path.isfile(SerialHelper.path):
            with open(SerialHelper.path, 'r') as json_file:
                return json.load(json_file)
        else:
            raise FileNotFoundError('Missing input.json')

    @staticmethod
    def write(dir, name, json_data):
        if not os.path.isdir(dir):
            os.makedirs(dir)
        path = '{dir}/{name}'.format(dir=dir, name=name) + '.json'
        with open(path, 'w') as json_file:
            json.dump(json_data, json_file, sort_keys=False, indent=2)

    @staticmethod
    def write_lang_file():
        if not os.path.isdir('lang'):
            os.mkdir('lang')

        for key in SerialHelper.langs_dictionairy.keys():
            path = 'lang/' + key + '.json'
            with open(path, 'w') as json_file:
                json.dump(SerialHelper.langs_dictionairy.get(
                    key), json_file, sort_keys=True, indent=2)

    @staticmethod
    def add_to_langs_dict(lang, lang_dict):
        if SerialHelper.langs_dictionairy.get(lang):
            SerialHelper.langs_dictionairy.get(lang).update(lang_dict)
        else:
            SerialHelper.langs_dictionairy.update({lang: lang_dict})


class Item(SerialHelper):
    def __init__(self, modid, name, langs_dict):
        self.modid = modid
        self.name = name
        self.langs_dict = langs_dict

        self.write_item_model()
        self.add_lang()

    def write_item_model(self):
        identifier = self.modid + ':items/' + self.name
        json_data = {
            'parent': 'item/generated',
            'textures': {
                'layer0': identifier
            }
        }
        SerialHelper.write('models/item', self.name, json_data)

    def add_lang(self):
        identifier = 'item.' + self.modid + '.' + self.name
        for lang in langs_dict:
            lang_dict = {identifier: langs_dict[lang]}
            self.add_to_langs_dict(lang, lang_dict)


class Block(SerialHelper):
    def __init__(self, modid, name, langs_dict):
        self.modid = modid
        self.name = name
        self.langs_dict = langs_dict

        self.write_block_model()
        self.write_blockstate()
        self.write_blockitem()
        self.write_loot_table()
        self.add_lang()

    def write_block_model(self):
        identifier = self.modid + ':blocks/' + self.name
        json_data = {
            'parent': 'block/cube_all',
            'textures': {
                'all': identifier
            }
        }
        self.write('models/block', self.name, json_data)

    def write_blockstate(self):
        identifier = self.modid + ':block/' + self.name
        json_data = {
            'variants': {
                '': {'model': identifier}
            }
        }
        SerialHelper.write('blockstates', self.name, json_data)

    def write_blockitem(self):
        identifier = self.modid + ':block/' + self.name
        json_data = {
            'parent': identifier
        }
        self.write('models/item', self.name, json_data)

    def write_loot_table(self):
        identifier = self.modid + ':' + self.name
        json_data = {
            'type': 'minecraft:block',
            'pools': [
                {
                    'rolls': 1,
                    'entries': [
                        {
                            'type': 'minecraft:item',
                            'name': identifier
                        }
                    ],
                    'conditions': [
                        {
                            'condition': 'minecraft:survives_explosion'
                        }
                    ]
                }
            ]
        }
        self.write('loot_tables', self.name, json_data)

    def add_lang(self):
        identifier = 'block.' + self.modid + '.' + self.name
        for lang in langs_dict:
            lang_dict = {identifier: langs_dict[lang]}
            self.add_to_langs_dict(lang, lang_dict)


class OrientableBlock(Block):
    def write_block_model(self):
        identifier = self.modid + ':blocks/' + self.name
        json_data = {
            'parent': 'block/orientable',
            'textures': {
                'front': identifier + '_front',
                'side': identifier + '_side',
                'top': identifier + '_top'
            }
        }
        self.write('models/block', self.name, json_data)

    def write_blockstate(self):
        identifier = self.modid + ':block/' + self.name
        json_data = {
            'variants': {
                'facing=north': {'model': identifier},
                'facing=east': {'model': identifier, 'y': 90},
                'facing=south': {'model': identifier, 'y': 180},
                'facing=west': {'model': identifier, 'y': 270}
            }
        }
        self.write('blockstates', self.name, json_data)


class StairsBlock(Block):
    def __init__(self, modid, name, lang_dict, origin_block):
        self.modid = modid
        self.name = name
        self.lang_dict = lang_dict
        self.origin_block = origin_block

        self.write_block_model()
        self.write_blockstate()
        self.write_blockitem()
        self.write_loot_table()
        self.add_lang()

    def write_block_model(self):
        identifier = self.modid + ':blocks/' + self.origin_block
        json_data = {
            'parent': 'minecraft:block/stairs',
            'textures': {
                'bottom': identifier,
                'top': identifier,
                'side': identifier
            }
        }
        self.write('models/block', self.name, json_data)

        json_data = {
            'parent': 'minecraft:block/inner_stairs',
            'textures': {
                'bottom': identifier,
                'top': identifier,
                'side': identifier
            }
        }
        self.write('models/block', self.name + '_inner', json_data)

        json_data = {
            'parent': 'minecraft:block/outer_stairs',
            'textures': {
                'bottom': identifier,
                'top': identifier,
                'side': identifier
            }
        }
        self.write('models/block', self.name + '_outer', json_data)

    def write_blockstate(self):
        identifier = modid + ':block/' + self.name
        identifier_inner = identifier + '_inner'
        identifier_outer = identifier + '_outer'
        json_data = {
            'variants': {
                'facing=east,half=bottom,shape=inner_left': {
                    'model': identifier_inner,
                    'y': 270,
                    'uvlock': True
                },
                'facing=east,half=bottom,shape=inner_right': {
                    'model': identifier_inner
                },
                'facing=east,half=bottom,shape=outer_left': {
                    'model': identifier_outer,
                    'y': 270,
                    'uvlock': True
                },
                'facing=east,half=bottom,shape=outer_right': {
                    'model': identifier_outer
                },
                'facing=east,half=bottom,shape=straight': {
                    'model': identifier
                },
                'facing=east,half=top,shape=inner_left': {
                    'model': identifier_inner,
                    'x': 180,
                    'uvlock': True
                },
                'facing=east,half=top,shape=inner_right': {
                    'model': identifier_inner,
                    'x': 180,
                    'y': 90,
                    'uvlock': True
                },
                'facing=east,half=top,shape=outer_left': {
                    'model': identifier_outer,
                    'x': 180,
                    'uvlock': True
                },
                'facing=east,half=top,shape=outer_right': {
                    'model': identifier_outer,
                    'x': 180,
                    'y': 90,
                    'uvlock': True
                },
                'facing=east,half=top,shape=straight': {
                    'model': identifier,
                    'x': 180,
                    'uvlock': True
                },
                'facing=north,half=bottom,shape=inner_left': {
                    'model': identifier_inner,
                    'y': 180,
                    'uvlock': True
                },
                'facing=north,half=bottom,shape=inner_right': {
                    'model': identifier_inner,
                    'y': 270,
                    'uvlock': True
                },
                'facing=north,half=bottom,shape=outer_left': {
                    'model': identifier_outer,
                    'y': 180,
                    'uvlock': True
                },
                'facing=north,half=bottom,shape=outer_right': {
                    'model': identifier_outer,
                    'y': 270,
                    'uvlock': True
                },
                'facing=north,half=bottom,shape=straight': {
                    'model': identifier,
                    'y': 270,
                    'uvlock': True
                },
                'facing=north,half=top,shape=inner_left': {
                    'model': identifier_inner,
                    'x': 180,
                    'y': 270,
                    'uvlock': True
                },
                'facing=north,half=top,shape=inner_right': {
                    'model': identifier_inner,
                    'x': 180,
                    'uvlock': True
                },
                'facing=north,half=top,shape=outer_left': {
                    'model': identifier_outer,
                    'x': 180,
                    'y': 270,
                    'uvlock': True
                },
                'facing=north,half=top,shape=outer_right': {
                    'model': identifier_outer,
                    'x': 180,
                    'uvlock': True
                },
                'facing=north,half=top,shape=straight': {
                    'model': identifier,
                    'x': 180,
                    'y': 270,
                    'uvlock': True
                },
                'facing=south,half=bottom,shape=inner_left': {
                    'model': identifier_inner
                },
                'facing=south,half=bottom,shape=inner_right': {
                    'model': identifier_inner,
                    'y': 90,
                    'uvlock': True
                },
                'facing=south,half=bottom,shape=outer_left': {
                    'model': identifier_outer
                },
                'facing=south,half=bottom,shape=outer_right': {
                    'model': identifier_outer,
                    'y': 90,
                    'uvlock': True
                },
                'facing=south,half=bottom,shape=straight': {
                    'model': identifier,
                    'y': 90,
                    'uvlock': True
                },
                'facing=south,half=top,shape=inner_left': {
                    'model': identifier_inner,
                    'x': 180,
                    'y': 90,
                    'uvlock': True
                },
                'facing=south,half=top,shape=inner_right': {
                    'model': identifier_inner,
                    'x': 180,
                    'y': 180,
                    'uvlock': True
                },
                'facing=south,half=top,shape=outer_left': {
                    'model': identifier_outer,
                    'x': 180,
                    'y': 90,
                    'uvlock': True
                },
                'facing=south,half=top,shape=outer_right': {
                    'model': identifier_outer,
                    'x': 180,
                    'y': 180,
                    'uvlock': True
                },
                'facing=south,half=top,shape=straight': {
                    'model': identifier,
                    'x': 180,
                    'y': 90,
                    'uvlock': True
                },
                'facing=west,half=bottom,shape=inner_left': {
                    'model': identifier_inner,
                    'y': 90,
                    'uvlock': True
                },
                'facing=west,half=bottom,shape=inner_right': {
                    'model': identifier_inner,
                    'y': 180,
                    'uvlock': True
                },
                'facing=west,half=bottom,shape=outer_left': {
                    'model': identifier_outer,
                    'y': 90,
                    'uvlock': True
                },
                'facing=west,half=bottom,shape=outer_right': {
                    'model': identifier_outer,
                    'y': 180,
                    'uvlock': True
                },
                'facing=west,half=bottom,shape=straight': {
                    'model': identifier,
                    'y': 180,
                    'uvlock': True
                },
                'facing=west,half=top,shape=inner_left': {
                    'model': identifier_inner,
                    'x': 180,
                    'y': 180,
                    'uvlock': True
                },
                'facing=west,half=top,shape=inner_right': {
                    'model': identifier_inner,
                    'x': 180,
                    'y': 270,
                    'uvlock': True
                },
                'facing=west,half=top,shape=outer_left': {
                    'model': identifier_outer,
                    'x': 180,
                    'y': 180,
                    'uvlock': True
                },
                'facing=west,half=top,shape=outer_right': {
                    'model': identifier_outer,
                    'x': 180,
                    'y': 270,
                    'uvlock': True
                },
                'facing=west,half=top,shape=straight': {
                    'model': identifier,
                    'x': 180,
                    'y': 180,
                    'uvlock': True
                }
            }
        }
        self.write('blockstates', self.name, json_data)


class SlabBlock(Block):
    def __init__(self, modid, name, lang_dict, origin_block):
        self.modid = modid
        self.name = name
        self.lang_dict = lang_dict
        self.origin_block = origin_block

        self.write_block_model()
        self.write_blockstate()
        self.write_blockitem()
        self.write_loot_table()
        self.add_lang()

    def write_block_model(self):
        identifier = self.modid + ':blocks/' + self.origin_block
        json_data = {
            'parent': 'minecraft:block/slab',
            'textures': {
                'bottom': identifier,
                'top': identifier,
                'side': identifier
            }
        }
        self.write('models/block', self.name, json_data)

        json_data = {
            'parent': 'minecraft:block/slab_top',
            'textures': {
                'bottom': identifier,
                'top': identifier,
                'side': identifier
            }
        }
        self.write('models/block', self.name + '_top', json_data)

    def write_blockstate(self):
        identifier = self.modid + ':block/' + self.name
        identifier_top = identifier + '_top'
        identifier_origin_block = self.modid + ':block/' + self.origin_block
        json_data = {
            'variants': {
                'type=bottom': {
                    'model': identifier
                },
                'type=double': {
                    'model': identifier_origin_block
                },
                'type=top': {
                    'model': identifier_top
                }
            }
        }
        self.write('blockstates', self.name, json_data)


class WallBlock(Block):
    def __init__(self, modid, name, lang_dict, origin_block):
        self.modid = modid
        self.name = name
        self.lang_dict = lang_dict
        self.origin_block = origin_block

        self.write_block_model()
        self.write_blockstate()
        self.write_blockitem()
        self.write_loot_table()
        self.add_lang()

    def write_block_model(self):
        identifier = self.modid + ':blocks/' + self.origin_block
        json_data = {
            'parent': 'minecraft:block/template_inventory',
            'textures': {
                'wall': identifier
            }
        }
        self.write('models/block', self.name + '_inventory', json_data)

        json_data = {
            'parent': 'minecraft:block/template_wall_post',
            'textures': {
                'wall': identifier
            }
        }
        self.write('models/block', self.name + '_post', json_data)

        json_data = {
            'parent': 'minecraft:block/wall_side',
            'textures': {
                'wall': identifier
            }
        }
        self.write('models/block', self.name + '_side', json_data)

        json_data = {
            'parent': 'minecraft:block/template_wall_side_tall',
            'textures': {
                'wall': identifier
            }
        }
        self.write('models/block', self.name + '_side_tall', json_data)

    def write_blockstate(self):
        identifier = self.modid + ':block/' + self.name
        identifier_post = identifier + '_post'
        identifier_side = identifier + '_side'
        identifier_side_tall = identifier_side + '_tall'
        json_data = {
            "multipart": [
                {
                    "when": {
                        "up": "true"
                    },
                    "apply": {
                        "model": identifier_post
                    }
                },
                {
                    "when": {
                        "north": "low"
                    },
                    "apply": {
                        "model": identifier_side,
                        "uvlock": True
                    }
                },
                {
                    "when": {
                        "east": "low"
                    },
                    "apply": {
                        "model": identifier_side,
                        "y": 90,
                        "uvlock": True
                    }
                },
                {
                    "when": {
                        "south": "low"
                    },
                    "apply": {
                        "model": identifier_side,
                        "y": 180,
                        "uvlock": True
                    }
                },
                {
                    "when": {
                        "west": "low"
                    },
                    "apply": {
                        "model": identifier_side,
                        "y": 270,
                        "uvlock": True
                    }
                },
                {
                    "when": {
                        "north": "tall"
                    },
                    "apply": {
                        "model": identifier_side_tall,
                        "uvlock": True
                    }
                },
                {
                    "when": {
                        "east": "tall"
                    },
                    "apply": {
                        "model": identifier_side_tall,
                        "y": 90,
                        "uvlock": True
                    }
                },
                {
                    "when": {
                        "south": "tall"
                    },
                    "apply": {
                        "model": identifier_side_tall,
                        "y": 180,
                        "uvlock": True
                    }
                },
                {
                    "when": {
                        "west": "tall"
                    },
                    "apply": {
                        "model": identifier_side_tall,
                        "y": 270,
                        "uvlock": True
                    }
                }
            ]
        }
        self.write('blockstates', self.name, json_data)

    def write_blockitem(self):
        identifier = self.modid + ':block/' + self.name + '_inventory'
        json_data = {
            'parent': identifier
        }
        self.write('models/item', self.name, json_data)


json_input = SerialHelper.read()
modid = json_input.get('modid')
types = {'block/cube_all': Block, 'item/generated': Item,
         'block/orientable': OrientableBlock, 'block/stairs': StairsBlock, 'block/wall': WallBlock}

for entry in json_input.get('entries'):
    parent = entry.get('parent')
    name = entry.get('name')
    langs_dict = entry.get('lang')
    if entry.get('origin_block'):
        types.get(parent)(modid, name, langs_dict, entry.get('origin_block'))
    else:
        types.get(parent)(modid, name, langs_dict)
    print(langs_dict)

SerialHelper.write_lang_file()
