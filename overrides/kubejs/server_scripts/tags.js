//Tags

ServerEvents.tags('item', event => {
    // Get the #forge:cobblestone tag collection and add Diamond Ore to it
    event.add('cosmopolis:space_suit_helmet', ['jetboots:guardian_helmet', 'mekanism:mekasuit_helmet'])
    event.add('cosmopolis:space_suit_chestplate', ['jetboots:guardian_jacket', 'mekanism:mekasuit_bodyarmor'])
    event.add('cosmopolis:space_suit_leggings', ['jetboots:guardian_pants', 'mekanism:mekasuit_pants'])
    event.add('cosmopolis:space_suit_boots', ['jetboots:rocket_boots', 'mekanism:mekasuit_boots'])
    event.add('cosmopolis:space_suit_boots', 'jetboots:jetboots')
    event.add('itemfilters:check_nbt', 'ceramicbucket:ceramic_bucket')
    event.add('itemfilters:check_nbt', 'minecraft:water_bucket')
    event.add('itemfilters:check_nbt', 'immersiveengineering:blueprint')
    event.add('itemfilters:check_nbt', 'compactmachines:tunnel')
    event.add('forge:storage_blocks/aluminium', 'immersiveengineering:storage_aluminum')
    event.add('forge:raw_materials/aluminum', 'neverenderore:raw_never_ender_aluminium')
    event.add('forge:gems/ruby', 'astropolis:ruby')
    event.add('forge:gems/sapphire', 'astropolis:sapphire')
    event.add('forge:gems', ['astropolis:ruby', 'astropolis:sapphire'])
    event.add('opolisutilities:resource_generator_blocks', ['cosmopolis:asteroid_block'])

})

ServerEvents.tags('block', event => {
    event.add('opolisutilities:resource_generator_blocks', ['cosmopolis:asteroid_block'])
})

/*

//Forge Tag Fixed For Mods

e.add('forge:nuggets/copper', ['exlinecopperequipment:copper_nugget'])


})

onEvent('tags.blocks', e => {

//e.add('caveopolis:level_1_blocks', ['minecraft:stone'])


onEvent('tags.fluids', e => {

//e.add('skyopolis:molten_fungus', 'skyopolis:molten_fungus')

})

*/



//})

