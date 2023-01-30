import re
import json
import dash.html.Img as img
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
        if "set8".lower() in trait.lower():
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

def get_traits_from_items(itemlist,itemdict):
    '''
    '''
    traits_from_items = []
    for item in itemlist:
        if item != None:
            item_trait_benefit = re.sub("Item|TFT8_Augment_|TFT8_Item_|TFT_Item","",item)
            if re.match("Emblem\d?",item_trait_benefit)!=None:
                item_trait_benefit = re.sub("Emblem\d?","",item_trait_benefit)
                traits_from_items.append(item_trait_benefit)
    return traits_from_items
def get_traits_from_augments(augments,traitdict):
    augment_traits = []
    for augment in augments:
        is_augmentstem = re.match("TFT8_Augment_\D*Trait",augment)
       
        if is_augmentstem!=None:
            
            traitstem = re.sub("TFT8_Augment_|Trait\d?","",augment)
            trait = get_trait_from_traitstem(traitstem,traitdict)
            augment_traits.append(trait)
    return augment_traits
def calculate_comp_traits(unitlist,itemlist,augmentlist,championdict,itemdict,fulltraitdict):
    '''
    '''
    traitdict = {}
    unitlist = list(dict.fromkeys(unitlist))
    for unit in unitlist:
        unit_traits = get_traits_from_unit(unit,championdict,itemdict,fulltraitdict)
        for trait in unit_traits:
            if trait in traitdict.keys():
                traitdict[trait] +=1
            else:
                traitdict[trait] = 1
    
    itemtraitstems = get_traits_from_items(itemlist,itemdict)
   
    itemtraits = []
    for itemstem in itemtraitstems:
       
        propertraits = get_trait_from_traitstem(itemstem,fulltraitdict)
        
        itemtraits.append(propertraits)
   
    for trait in itemtraits:
        if trait in traitdict.keys():
            traitdict[trait]+=1
        else:
            traitdict[trait] = 1
    augment_traits = get_traits_from_augments(augmentlist,fulltraitdict)
    for augment in augment_traits:
        if augment in fulltraitdict.keys():
            try:
                traitdict[augment]+=1
            except:
                TraitNotFound(augment)
        else:
            traitdict[augment]=1
    
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

def get_img_for_champ(champname):
    url = "https://raw.communitydragon.org/latest/game/assets/characters/"+champname.lower()+"/hud/"+champname.lower()+".tft_set8.png"
    champ_img =img(src = url)
    return champ_img
def get_img_for_item(itemname):
    c,i,t = create_tft_dictionaries()
    
    if re.match("Emblem\d?",itemname)!=None:
        item = re.sub("TFT8_Item_.+EmblemItem",itemname)
        url = "https://raw.communitydragon.org/latest/game/assets/maps/particles/tft/item_icons/traits/spatula/set8/"
    else:
        url = "https://raw.communitydragon.org/latest/game/assets/maps/particles/tft/"+itemname.lower()+".png"
    item_img = img(src=url)
    return item_img
def get_img_for_trait(traitname):
    pass
def get_img_for_augment(augmentname):
    pass

    
