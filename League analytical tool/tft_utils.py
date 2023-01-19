import re
import json

class TraitNotFound(Exception):
    def __init__(self,trait):
        super().__init__("trait "+trait+" doesnt exist")
def create_tft_dictionaries():
    '''
    returns 3 dictionaries from the json files for the information on tft champions, traits and items
    '''
    with open("./Data/tftchampions.json") as tftc:
        tftchampionslist = json.loads(tftc.read())
    tftchampions = {}
    for champion in tftchampionslist:
        champname = champion['character_id']
        tftchampions[champname] = champion
    with open("./Data/tftitems.json") as tfti:
        tftitemslist = json.loads(tfti.read())
    tftitems = {}
    for item in tftitemslist:
        itemname = item['nameId']
        tftitems[itemname] = item
    with open("./Data/tfttraits.json") as tftt:
        tfttraitslist = json.loads(tftt.read())
    tfttraits = {}
    for trait in tfttraitslist:
        traitname = trait['trait_id']
        tfttraits[traitname] = trait
    return tftchampions,tftitems,tfttraits
def get_trait_from_traitstem(traitstem,traitdict):
    '''
    will return the full proper trait name from stems
    ex: underground will return TFT8_
    '''
    for trait in traitdict.keys():
        if traitstem.lower() in trait.lower():
            return trait
        elif traitstem.lower() == 'InterPolaris'.lower():
            return('Set8_SpaceCorps')
    raise(TraitNotFound(traitstem))
    
        
    
    
def get_traits_from_unit(unitname,championdict,itemdict,traitdict):
    '''
    '''
    unit_trait = [trait['id'] for trait in championdict[unitname]['traits']]
    return unit_trait

def get_traits_from_items(itemlist,championdict,itemdict,traitdict):
    '''
    '''
    traits_from_items = []
    for item in itemlist:
        item_trait_benefit = re.sub("Item|TFT8_Augment_|TFT8_Item_|TFT_Item","",item)
        if re.match("Emblem\d?",item_trait_benefit)!=None:
            print("NOOO")
            item_trait_benefit = re.sub("|Emblem\d?","",item_trait_benefit)
            traits_from_items.append(item_trait_benefit)
    return traits_from_items

def calculate_comp_traits(unitlist,itemlist,championdict,itemdict,fulltraitdict):
    '''
    '''
    traitdict = {}
    for unit in unitlist:
        unit_traits = get_traits_from_unit(unit,championdict,itemdict,fulltraitdict)
        for trait in unit_traits:
            if trait in traitdict.keys():
                traitdict[trait] +=1
            else:
                traitdict[trait] = 1
    
    itemtraitstems = get_traits_from_items(itemlist,championdict,itemdict,fulltraitdict)
    print(itemtraitstems)
    itemtraits = []
    for itemstem in itemtraitstems:
        print(itemstem)
        propertraits = get_trait_from_traitstem(itemstem,fulltraitdict)
        itemtraits.append(propertraits)
   
    for trait in itemtraits:
        if trait in traitdict.keys():
            traitdict[trait]+=1
        else:
            traitdict[trait] = 1
    return traitdict
def calculate_trait_tier(numunits,trait,traitdict):
    '''
    '''
    trait_data = traitdict[trait]
    conditions = trait_data['conditional_trait_sets']
    for tier in conditions:
        if 'max_units' in tier.keys():
            min_units = tier['min_units']
            max_units = tier['max_units']
            tiercolor = tier['style_name']
            if numunits>= min_units and numunits<=tier['max_units']:
                return([min_units,tiercolor])
        else:
            min_units = tier['min_units']
            tiercolor = tier['style_name']
            if numunits>= min_units:
                return([min_units,tiercolor])
    return([0,"Grey"])
