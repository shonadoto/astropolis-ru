// priority: 100

ServerEvents.recipes (event => {

//Slabs To Blocks
    
//e.forEachRecipe({ type: 'minecraft:crafting_shaped', output: '#minecraft:slabs' }, r => {
//    e.shaped(r.inputItems[a], ["A", "A"], { A: r.outputItems[a].withCount(1) })})
//    
//Smelting

// e.smelting(black_iron_ingot, compressed_iron_ingot).id('extendedcrafting:black_iron_ingot')

//Crafting (Stone Chests)

//RFTools 

event.shaped('1x rftoolsbase:machine_frame', ['OIO','IMI','OIO'], {I:'minecraft:iron_ingot', O: 'engineersdecor:old_industrial_wood_planks', M: 'astropolis:machinist_research_pack'}).id('rftoolsbase:machine_frame')
event.shapeless('3x rftoolsbase:machine_base', ['rftoolsbase:machine_frame']).id('rftoolsbase:machine_base')
event.shapeless('1x rftoolsbase:machine_frame', ['rftoolsbase:machine_base', 'rftoolsbase:machine_base', 'rftoolsbase:machine_base']).id('astropolis:machine_frame')


//Extended Crafting

event.shaped('2x extendedcrafting:frame', ['PPP','PMP','PPP'], {P: 'extendedcrafting:black_iron_slate', M: 'astropolis:machinist_research_pack'}).id('extendedcrafting:frame')
event.shaped('6x extendedcrafting:black_iron_ingot', ['III','CCC','III'], {I: 'minecraft:iron_ingot', C: 'neverenderore:raw_never_ender_coal'}).id('extendedcrafting:black_iron_ingot')
event.custom({type:"immersiveengineering:metal_press", energy:2400, input:{item:"extendedcrafting:black_iron_ingot"}, mold:"immersiveengineering:mold_plate", result:{item:"extendedcrafting:black_iron_slate"}}).id('extendedcrafting:black_iron_slate')

event.shaped('1x extendedcrafting:compressor', ['III','IMI','III'], {M: 'extendedcrafting:frame', I: 'astropolis:ingot_of_ingots'}).id('extendedcrafting:compressor')

event.shaped('1x extendedcrafting:basic_table', ['ICI','IMI','ICI'], {M: 'extendedcrafting:frame', I: 'minecraft:iron_block', C: 'minecraft:crafting_table'}).id('extendedcrafting:basic_table')
event.shaped('1x extendedcrafting:advanced_table', ['ICI','IMI','ICI'], {M: 'extendedcrafting:frame', I: 'minecraft:gold_block', C: 'extendedcrafting:basic_table'}).id('extendedcrafting:advanced_table')
event.shaped('1x extendedcrafting:elite_table', ['ICI','IMI','ICI'], {M: 'extendedcrafting:frame', I: 'astropolis:gem_of_gems', C: 'extendedcrafting:advanced_table'}).id('extendedcrafting:elite_table')
event.shaped('1x extendedcrafting:ultimate_table', ['ICI','IMI','ICI'], {M: 'extendedcrafting:frame', I: 'astropolis:shard_of_shards', C: 'extendedcrafting:elite_table'}).id('extendedcrafting:ultimate_table')


//Custom Compressor Recipes

function quantumCompressor(input, output, catalyst, power, inputCount){
  event.custom({ "type": "extendedcrafting:compressor", "powerCost": power, "inputCount": inputCount, "ingredient": { "item": input }, "catalyst": { "item": catalyst }, "result": { "item": output } })
}

quantumCompressor('cosmopolis:moon_portal_frame', 'cosmopolis:mars_portal_frame', 'astropolis:ingot_of_ingots', 100000, 1)

//Extended Crafting (TABLES)

event.custom({
  "type": "extendedcrafting:shaped_table",
  "pattern": [
    "AAAAA",
    " AAA ",
    " AAA ",
    "AAAAA",
    "AAAAA"
  ],
  "key": {
    "A": {
      "item": "extendedcrafting:black_iron_slate"
    }
  },
  "result": {
    "item": "extendedcrafting:pedestal"
  }
}).id('extendedcrafting:pedestal')

event.custom({
  "type": "extendedcrafting:shaped_table",
  "pattern": [
    "AAAAA",
    "AAAAA",
    "BBBBB",
    "AAAAA",
    "AAAAA"
  ],
  "key": {
    "A": {
      "item": "extendedcrafting:black_iron_slate"
    },
    "B": {
      "item": "minecraft:diamond_block"
    }
  },
  "result": {
    "item": "extendedcrafting:crafting_core"
  }
}).id('extendedcrafting:crafting_core')

event.custom({
  "type": "extendedcrafting:combination",
  "powerCost": 100000,
  "input":  {"item": "extendedcrafting:black_iron_ingot"},
  "ingredients": [
    {
      "item": "immersiveengineering:ingot_electrum"
    },
    {
      "item": "immersiveengineering:ingot_nickel"
    },
    {
      "item": "immersiveengineering:ingot_constantan"
    },
    {
      "item": "mekanism:ingot_refined_glowstone"
    },
    {
      "item": "mekanism:ingot_refined_obsidian"
    },
    {
      "item": "immersiveengineering:ingot_aluminum"
    },
    {
      "item": "immersiveengineering:ingot_silver"
    },
    {
      "item": "minecraft:copper_ingot"
    },
    {
      "item": "mekanism:ingot_uranium"
    },
    {
      "item": "minecraft:iron_ingot"
    },
    {
      "item": "mekanism:ingot_bronze"
    },
    {
      "item": "minecraft:netherite_ingot"
    },
    {
      "item": "mekanism:ingot_osmium"
    },
    {
      "item": "minecraft:gold_ingot"
    },
    {
      "item": "mekanism:ingot_tin"
    },
    {
      "item": "mekanism:ingot_steel"
    }
  ],
  "result": {
    "item": "astropolis:ingot_of_ingots"
  }
}).id('astropolis:ingot_of_ingots')

event.custom({
  "type": "extendedcrafting:shaped_table",
  "pattern": [
    " AAA ",
    "A   A",
    "A B A",
    "A   A",
    " AAA "
  ],
  "key": {
    "A": {
      "item": "extendedcrafting:black_iron_slate"
    },
    "B": {
      "item": "astropolis:ingot_of_ingots"
    }
  },
  "result": {
    "item": "cosmopolis:alien_artifact"
  }
}).id('cosmopolis:alien_artifact')

event.custom({
  "type": "extendedcrafting:combination",
  "powerCost": 100000,
  "input":  {"item": "minecraft:quartz"},
  "ingredients": [
    {
      "item": "ae2:charged_certus_quartz_crystal"
    },
    {
      "item": "minecraft:emerald"
    },
    {
      "item": "mekanism:fluorite_gem"
    },
    {
      "item": "minecraft:lapis_lazuli"
    },
    {
      "item": "minecraft:prismarine_crystals"
    },
    {
      "item": "ae2:fluix_crystal"
    },
    {
      "item": "minecraft:diamond"
    },
    {
      "item": "astropolis:sapphire"
    },
    {
      "item": "astropolis:ruby"
    }
  ],
  "result": {
    "item": "astropolis:gem_of_gems"
  }
})

event.custom({
  "type": "extendedcrafting:shaped_table",
  "pattern": [
    "AAAAAAAAA",
    "BBBBBBBBB",
    "CDDEEEDDC",
    "CDDEEEDDC",
    "CDDEEEDDC",
    "CDDEEEDDC",
    "FFFFFFFFF",
    "FGGGGGGGF",
    "FFFFFFFFF"
  ],
  "key": {
    "A": {
      "item": "minecraft:grass_block"
    },
    "B": {
      "item": "minecraft:dirt"
    },
    "C": {
      "item": "minecraft:stone"
    },
    "D": {
      "item": "astropolis:ingot_of_ingots"
    },
    "E": {
      "item": "astropolis:gem_of_gems"
    },
    "F": {
      "item": "minecraft:deepslate"
    },
    "G": {
      "item": "astropolis:shard_of_shards"
    }
  },
  "result": {
    "item": "astropolis:overworld_core"
  }
})

event.custom({
  "type": "extendedcrafting:shaped_table",
  "pattern": [
    "AABBBBBAA",
    "ABBBBBBBA",
    "BBBBBBBBB",
    "BBBCCCBBB",
    "BBBCBCBBB",
    "BBBCCCBBB",
    "BBBBBBBBB",
    "ABBBBBBBA",
    "AABBBBBAA"
  ],
  "key": {
    "A": {
      "item": "cosmopolis:mars_portal_frame"
    },
    "B": {
      "item": "astropolis:overworld_core"
    },
    "C": {
      "item": "minecraft:obsidian"
    }
  },
  "result": {
    "item": "cosmopolis:space_portal_frame",
    "count": 2
  }
})

event.custom({
  "type": "extendedcrafting:combination",
  "powerCost": 100000,
  "input": {"item": "cosmopolis:ice_shard"},
  "ingredients": [
    {
      "item": "geodeopolis:emerald_shard"
    },
    {
      "item": "geodeopolis:diamond_shard"
    },
    {
      "item": "geodeopolis:quartz_shard"
    },
    {
      "item": "caveopolis:bright_shard"
    },
    {
      "item": "geodeopolis:glowstone_shard"
    },
    {
      "item": "geodeopolis:coal_shard"
    },
    {
      "item": "geodeopolis:redstone_shard"
    },
    {
      "item": "geodeopolis:lead_shard"
    },
    {
      "item": "geodeopolis:tin_shard"
    },
    {
      "item": "geodeopolis:lapis_shard"
    },
    {
      "item": "geodeopolis:aluminum_shard"
    },
    {
      "item": "geodeopolis:iron_shard"
    },
    {
      "item": "geodeopolis:debris_shard"
    },
    {
      "item": "minecraft:amethyst_shard"
    },
    {
      "item": "geodeopolis:copper_shard"
    },
    {
      "item": "geodeopolis:nickel_shard"
    },
    {
      "item": "geodeopolis:osmium_shard"
    },
    {
      "item": "geodeopolis:silver_shard"
    },
    {
      "item": "geodeopolis:gold_shard"
    },
    {
      "item": "geodeopolis:uranium_shard"
    }
  ],
  "result": {
    "item": "astropolis:shard_of_shards"
  }
})

//Compact Machines

event.replaceInput({id: 'compactmachines:wall'}, 'minecraft:polished_deepslate', 'immersiveengineering:sheetmetal_iron')
event.shaped('1x compactmachines:personal_shrinking_device', [' W ','WIW',' W '], {W: 'compactmachines:wall', I: 'minecraft:iron_ingot'}).id('compactmachines:personal_shrinking_device')
event.shaped(Item.of('compactmachines:chunkloader_upgrade', '{upgrade_info:{key:"compactmachines:chunkloader"}}'), ['WWW','QRE','WWW'], {E:Item.of('compactmachines:tunnel', '{definition:{id:"compactmachines:item"}}').strongNBT(),  W: 'compactmachines:wall', R: Item.of('compactmachines:tunnel', '{definition:{id:"compactmachines:fluid"}}').strongNBT(),  Q: Item.of('compactmachines:tunnel', '{definition:{id:"compactmachines:energy"}}').strongNBT()}).id('astropolis:chunkloader')
event.shaped(Item.of('compactmachines:tunnel', '{definition:{id:"compactmachines:energy"}}'), [' W ','WIW',' W '], {W: 'compactmachines:wall', I: 'pipez:energy_pipe'}).id('compactmachines:tunnels/energy')
event.shaped(Item.of('compactmachines:tunnel', '{definition:{id:"compactmachines:fluid"}}'), [' W ','WIW',' W '], {W: 'compactmachines:wall', I: 'pipez:fluid_pipe'}).id('compactmachines:tunnels/fluid')
event.shaped(Item.of('compactmachines:tunnel', '{definition:{id:"compactmachines:item"}}'), [' W ','WIW',' W '], {W: 'compactmachines:wall', I: 'pipez:item_pipe'}).id('compactmachines:tunnels/item')

event.shaped('1x pipez:basic_upgrade' , ['INI','NMN','INI'], {I: '#forge:ingots/iron', N: '#forge:nuggets/iron', M: 'astropolis:machinist_research_pack'}).id('pipez:basic_upgrade')
event.shaped('1x pipez:improved_upgrade' , ['INI','NMN','INI'], {I: '#forge:ingots/bronze', N: '#forge:nuggets/bronze', M: 'astropolis:machinist_research_pack'}).id('pipez:improved_upgrade')


//Cosmopolis

event.shaped('1x cosmopolis:venus_portal_frame', ['FRF','C A','FRF'], {F: 'cosmopolis:mining_belt_portal_frame', R: 'minecraft:red_sandstone', C: 'ae2:formation_core', A: 'ae2:annihilation_core'}).id('astropolis:venus_portal_frame')
event.shaped('10x cosmopolis:moon_portal_frame', ['FRF','C C','FRF'], {F: 'cosmopolis:venus_portal_frame', R: 'cosmopolis:mining_belt_portal_frame', C: 'mekanism:quantum_entangloporter'}).id('astropolis:moon_portal_frame')
//event.shaped('5x cosmopolis:mars_portal_frame', [' I ','IFI',' I '], {F: 'cosmopolis:moon_portal_frame', I: 'astropolis:ingot_of_ingots'}).id('astropolis:mars_portal_frame')

//Caveopolis

event.shaped('1x caveopolis:stone_crafting_table', ['AA','AA'], {A: 'cosmopolis:asteroid_block'}).id('astropolis:stone_crafting_table')
event.shaped('4x caveopolis:stone_stick', ['A','A'], {A: 'cosmopolis:asteroid_block'}).id('astropolis:stone_stick')
event.shaped('5x caveopolis:bright_stone', ['SSS','SMS','SSS'], {S: 'minecraft:stone', M:'astropolis:miners_research_pack'}).id('astropolis:bright_stone')

event.shaped('1x cosmopolis:hammer', ['AAA','AAA',' S '], {S: 'caveopolis:stone_stick', A: 'cosmopolis:asteroid_block'}).id('astropolis:hammer')
event.shaped('1x cosmopolis:asteroid_pickaxe', ['AAA',' S ',' S '], {S: 'caveopolis:stone_stick', A: 'cosmopolis:asteroid_block'}).id('astropolis:asteroid_pickaxe')
event.shaped('1x cosmopolis:asteroid_hoe', ['AA ',' S ',' S '], {S: 'caveopolis:stone_stick', A: 'cosmopolis:asteroid_block'}).id('astropolis:asteroid_hoe')
event.shaped('1x cosmopolis:asteroid_shovel', [' A ',' S ',' S '], {S: 'caveopolis:stone_stick', A: 'cosmopolis:asteroid_block'}).id('astropolis:asteroid_shovel')
event.shaped('1x cosmopolis:asteroid_axe', ['AA ','AS ',' S '], {S: 'caveopolis:stone_stick', A: 'cosmopolis:asteroid_block'}).id('astropolis:asteroid_axe')
event.shaped('1x cosmopolis:asteroid_sword', [' A ',' A ',' S '], {S: 'caveopolis:stone_stick', A: 'cosmopolis:asteroid_block'}).id('astropolis:asteroid_sword')

//Minecraft

event.shaped('1x minecraft:grass_block', ['LLL','LDL','LLL'], {L: '#minecraft:leaves', D: 'minecraft:dirt'}).id('astropolis:grass_block')

event.shaped('1x minecraft:packed_ice', ['III','IBI','III'], {I: 'cosmopolis:ice_shard', B: 'minecraft:ice'}).id('minecraft:packed_ice')
event.shaped('1x minecraft:piston', ['PPP','CRC','CMC'], {P: '#minecraft:planks', C: '#forge:cobblestone/normal', R: 'engineersdecor:metal_bar', M: 'astropolis:machinist_research_pack'}).id('astropolis:piston')
event.shaped('1x minecraft:slime_ball', [' W ','WEW',' W '], {W: 'cosmopolis:water_drop', E: 'immersiveengineering:ersatz_leather'}).id('astropolis:slime_ball')
event.shaped('1x minecraft:red_sand', [' R ','RSR',' R '], {R: 'geodeopolis:redstone_shard', S: 'minecraft:sand'}).id('astropolis:red_sand')

event.shapeless('2x minecraft:snowball', ['cosmopolis:water_drop', 'cosmopolis:ice_shard']).id('astropolis:snowball')
event.shapeless('1x minecraft:flint', ['minecraft:gravel', 'minecraft:gravel', 'minecraft:gravel']).id('astropolis:flint')
event.shapeless('1x minecraft:glow_berries', ['minecraft:sweet_berries', 'minecraft:glowstone_dust']).id('astropolis:glow_berries')

event.shapeless('1x mekanism:dust_netherite', ['#forge:dusts/gold', '#forge:dusts/gold', '#forge:dusts/gold', '#forge:dusts/gold', 'minecraft:netherite_scrap', 'minecraft:netherite_scrap', 'minecraft:netherite_scrap', 'minecraft:netherite_scrap']).id('minecraft:netherite_ingot')

event.shapeless('1x minecraft:blue_dye', ['cosmopolis:water_drop', 'mekanism:dye_base']).id('astropolis:blue_dye')

event.custom({type: "minecraft:smoking", cookingtime: 100, experience: 0.05, ingredient: {tag: "minecraft:logs"}, result: "supplementaries:ash"}).id('astropolis:ash')

//Pipez

event.shaped('8x pipez:energy_pipe', ['BBB','FFF','BBB'], {B: 'minecraft:brick', F: 'minecraft:flint'}).id('pipez:energy_pipe')
event.shaped('8x pipez:item_pipe', ['BBB','FFF','BBB'], {B: 'minecraft:brick', F: '#forge:chests/wooden'}).id('pipez:item_pipe')
event.shaped('8x pipez:fluid_pipe', ['BBB','FFF','BBB'], {B: 'minecraft:iron_ingot', F: 'ceramicbucket:ceramic_bucket'}).id('pipez:fluid_pipe')
event.custom({type: "minecraft:crafting_shaped", pattern: [" F "," SF","S  "], key: {"F": {item: "minecraft:flint"},"S": {"item": "cosmopolis:artificial_stick"}}, result: {item: "pipez:wrench", count: 1}}).id('pipez:wrench')



//Misc

event.shaped(Item.of('ceramicbucket:ceramic_bucket', '{Fluid:{Amount:1000,FluidName:"minecraft:water"}}'), [' W ','WCW',' W '], {C: Item.of('ceramicbucket:ceramic_bucket').strongNBT(), W: 'cosmopolis:water_drop'}).id('astropolis:ceramic_water_bucket')
event.shaped('1x minecraft:water_bucket', [' W ','WCW',' W '], {C: 'minecraft:bucket', W: 'cosmopolis:water_drop'}).id('astropolis:iron_water_bucket')
event.shaped('1x minecraft:prismarine_crystals', [' A ','APA',' A '], {P: 'minecraft:prismarine_shard', A: 'minecraft:amethyst_shard'}).id('astropolis:prismarine_crystals')
event.shaped('1x minecraft:feather', ['  S',' S ','S  '], {S: 'minecraft:string'}).id('astropolis:feather')
event.shaped('1x rftoolsutility:regeneration_module', ['GGG','GMG','GGG'], {G: 'minecraft:golden_apple', M: 'rftoolsutility:module_template'}).id('rftoolsutility:regeneration_module')

event.shapeless('4x cosmopolis:water_drop', ['minecraft:water_bucket']).id('astropolis:water_drop_from_iron_water_bucket')
event.shapeless('4x cosmopolis:water_drop', [Item.of('ceramicbucket:ceramic_bucket', '{Fluid:{Amount:1000,FluidName:"minecraft:water"}}').strongNBT()]).id('astropolis:water_drop_from_clay_water_bucket')


event.shaped('1x flopper:flopper', ['BCB',' B '], {C: 'ceramicbucket:ceramic_bucket', B: 'minecraft:brick'}).id('flopper:recipes/flopper')
event.shaped('1x structurecompass:structure_compass', [' F ','FCF',' F '], {F: 'cosmopolis:mining_belt_portal_frame', C: 'cosmopolis:space_suit_upgrade'}).id('structurecompass:structure_compass')

event.shaped('1x minecraft:carrot', [' O ','OSO',' O '], {S: 'minecraft:pumpkin_seeds', O: 'cosmopolis:organic_powder'}).id('astropolis:carrot')
event.shaped('1x minecraft:potato', [' O ','OSO',' O '], {S: 'minecraft:melon_seeds', O: 'cosmopolis:organic_powder'}).id('astropolis:potato')
event.shaped('1x minecraft:sweet_berries', [' O ','OSO',' O '], {S: 'minecraft:wheat_seeds', O: 'cosmopolis:organic_powder'}).id('astropolis:berries')

//event.shaped(Item.of('minecraft:water_bucket', '{RepairCost:1}').enchant('minecraft:infinity', 1), ['WCW','CWC','WCW'], {W: 'cosmopolis:water_drop', C: 'minecraft:bucket'}).id('astropolis:infinity_water_bucket_iron')

//AE2

event.shaped('1x ae2:sky_stone_chest', ['AAA','ASA','AAA'], {A: 'cosmopolis:asteroid_block', S: 'cosmopolis:artificial_stick'}).id('astropolis:sky_stone_chest')
event.shaped('1x ae2:charger', ['EEE','SMS','EEE'], {E: '#forge:ingots/electrum', M: 'astropolis:machinist_research_pack', S:'#forge:ingots/steel'}).id('ae2:network/blocks/crystal_processing_charger')
event.shaped('1x ae2:inscriber', ['IFI','IPI','MPM'], {M: 'astropolis:machinist_research_pack', I: '#forge:ingots/iron', P: 'minecraft:sticky_piston', F:'ae2:fluix_block'}).id('ae2:network/blocks/inscribers')
event.shaped('8x ae2:quartz_fiber', ['GGG','DDD','GGG'], {G: 'ae2:quartz_glass', D: '#forge:dusts/certus_quartz'}).id('ae2:network/parts/quartz_fiber_part')
event.shaped('1x ae2:sky_stone_tank', ['AAA','AGA','AAA'], {A: 'cosmopolis:asteroid_block', G: '#forge:glass/colorless'}).id('ae2:misc/tank_sky_stone')

event.custom({type: "ae2:transform", circumstance: {type: "fluid", tag: "minecraft:water"}, ingredients: [{item: "ae2:charged_certus_quartz_crystal"},{item: "ae2:flawed_budding_quartz"}],result: {item: "ae2:flawless_budding_quartz"}}).id('astropolis:flawless_budding_quartz')

event.custom({type: "ae2:charger", ingredient: {item: "minecraft:redstone_block"}, result: {item: "minecraft:glowstone"}}).id('astropolis:charger_glowstone')
event.custom({type: "ae2:charger", ingredient: {item: "minecraft:glowstone_dust"}, result: {item: "ae2:certus_quartz_dust"}}).id('astropolis:charger_certus_quartz_dust')
event.custom({type: "ae2:charger", ingredient: {item: "ae2:fluix_block"}, result: {item: "ae2:mysterious_cube"}}).id('astropolis:mysterious_cube')
event.custom({type: "ae2:charger", ingredient: {tag: "forge:sand"}, result: {item: "ae2:silicon"}}).id('ae2:blasting/silicon_from_certus_quartz_dust')

event.custom({type: "ae2:inscriber", ingredients: {middle:{tag: "forge:ingots/silver"}, top:{item: "ae2:engineering_processor_press"}}, mode: "inscribe", result:{item: "ae2:printed_engineering_processor"}}).id('ae2:inscriber/engineering_processor_print')

event.custom({type: "ae2:inscriber", ingredients: {bottom:{tag: "forge:dusts/electrum"}, middle: {item: "ae2:charged_certus_quartz_crystal"}, top: {item: "minecraft:redstone"
    }},mode: "press",result: {item: "ae2:fluix_crystal"}}).id('astropolis:extra_fluix_crystal_recipe')

event.custom({type: "ae2:inscriber", ingredients: {middle:{item: "cosmopolis:asteroid_block"}}, mode: "inscribe", result: {item: "ae2:sky_dust"}}).id('ae2:inscriber/sky_stone_dust')
event.custom({type: "ae2:inscriber", ingredients: {middle:{item: "ae2:sky_dust"}}, mode: "inscribe", result: {item: "ae2:sky_stone_block"}}).id('astropolis:sky_stone_block')


//Essence 



//Mekanism

event.shaped('1x mekanism:steel_casing', ['NDN','MSM','NEN'], {M:'astropolis:machinist_research_pack', N:'#forge:ingots/netherite', E:'#forge:gems/emerald', D:'#forge:gems/diamond', S: '#forge:storage_blocks/steel'}).id('mekanism:steel_casing')
event.shaped('1x mekanism:metallurgic_infuser', ['IFI','OSO','IFI'], {I: '#forge:ingots/steel', F: 'minecraft:furnace', O:'#forge:ingots/osmium', S:'mekanism:steel_casing'}).id('mekanism:metallurgic_infuser')

event.shaped('1x mekanism:basic_energy_cube', ['III','BMB','III'], {I:'#forge:ingots/iron', B: 'mekanism:basic_universal_cable', M: 'astropolis:machinist_research_pack'}).id('mekanism:energy_cube/basic')
event.shaped('8x mekanism:basic_universal_cable', ['BMB',], {B:'#forge:ingots/steel', M: 'astropolis:machinist_research_pack'}).id('astropolis:basic_universal_cable')

event.shaped('3x mekanism:fluorite_gem', ['YQY','QYQ','YQY'], {Y:'mekanism:yellow_cake_uranium', Q: 'minecraft:quartz'}).id('astropolis:fluorite_gem')

event.shaped('1x mekanism:configurator', ['M','M','S'], {M:'astropolis:machinist_research_pack', S:'#forge:rods/wooden'}).id('mekanism:configurator')



//Astropolis

event.shaped('1x astropolis:miners_research_pack', ['ABA','BAB','ABA'], {A: 'cosmopolis:asteroid_block', B: 'mekanism:ingot_bronze'}).id('astropolis:miners_research_pack')
event.shaped('1x astropolis:machinist_research_pack', ['TST','STS','TST'], {T: '#forge:treated_wood', S: 'mekanism:ingot_steel'}).id('astropolis:machinist_research_pack')
event.shaped('1x astropolis:water_core', ['WBW','BCB','WBW'], {B: 'minecraft:water_bucket', C: 'astropolis:machinist_research_pack', W: 'cosmopolis:water_drop'}).id('astropolis:water_core')

event.shaped('1x geodeopolis:budding_copper', ['CBC','BMB','CBC'], {M:'astropolis:miners_research_pack', C: 'minecraft:copper_ingot', B: 'caveopolis:bright_shard'}).id('astropolis:budding_copper')
event.shaped('1x geodeopolis:budding_coal', ['CBC','BMB','CBC'], {M:'astropolis:miners_research_pack', C: 'minecraft:charcoal', B: 'caveopolis:bright_shard'}).id('astropolis:budding_coal')
event.shaped('1x geodeopolis:budding_tin', ['CBC','BMB','CBC'], {M:'astropolis:miners_research_pack', C: 'mekanism:ingot_tin', B: 'caveopolis:bright_shard'}).id('astropolis:budding_tin')
event.shaped('1x geodeopolis:budding_iron', ['CBC','BMB','CBC'], {M:'astropolis:miners_research_pack', C: 'minecraft:iron_ingot', B: 'caveopolis:bright_shard'}).id('astropolis:budding_iron')
event.shaped('1x minecraft:budding_amethyst', ['BBB','BMB','BBB'], {M:'astropolis:miners_research_pack', B: 'caveopolis:bright_shard'}).id('astropolis:budding_amethyst')

event.shaped('1x geodeopolis:budding_gold', ['CBC','BMB','CBC'], {M:'astropolis:miners_research_pack', C: 'minecraft:gold_ingot', B: 'caveopolis:bright_shard'}).id('astropolis:budding_gold')
event.shaped('1x geodeopolis:budding_redstone', ['CBC','BMB','CBC'], {M:'astropolis:miners_research_pack', C: 'minecraft:redstone', B: 'caveopolis:bright_shard'}).id('astropolis:budding_redstone')
event.shaped('1x geodeopolis:budding_silver', ['CBC','BMB','CBC'], {M:'astropolis:miners_research_pack', C: 'immersiveengineering:ingot_silver', B: 'caveopolis:bright_shard'}).id('astropolis:budding_silver')
event.shaped('1x geodeopolis:budding_quartz', ['CBC','BMB','CBC'], {M:'astropolis:miners_research_pack', C: 'minecraft:quartz', B: 'caveopolis:bright_shard'}).id('astropolis:budding_quartz')

event.shaped('1x geodeopolis:budding_diamond', ['CBC','BMB','CBC'], {M:'astropolis:miners_research_pack', C: 'minecraft:diamond', B: 'caveopolis:bright_shard'}).id('astropolis:budding_diamond')
event.shaped('1x geodeopolis:budding_emerald', ['CBC','BMB','CBC'], {M:'astropolis:miners_research_pack', C: 'minecraft:emerald', B: 'caveopolis:bright_shard'}).id('astropolis:budding_emerald')
event.shaped('1x geodeopolis:budding_debris', ['CBC','BMB','CBC'], {M:'astropolis:miners_research_pack', C: 'minecraft:ancient_debris', B: 'caveopolis:bright_shard'}).id('astropolis:budding_debris')
event.shaped('1x geodeopolis:budding_uranium', ['CBC','BMB','CBC'], {M:'astropolis:miners_research_pack', C: '#forge:ingots/uranium', B: 'caveopolis:bright_shard'}).id('astropolis:budding_uranium')
event.shaped('1x geodeopolis:budding_osmium', ['CBC','BMB','CBC'], {M:'astropolis:miners_research_pack', C: '#forge:ingots/osmium', B: 'caveopolis:bright_shard'}).id('astropolis:budding_osmium')

event.shaped('1x geodeopolis:budding_aluminum', ['CBC','BMB','CBC'], {M:'astropolis:miners_research_pack', C: '#forge:ingots/aluminum', B: 'caveopolis:bright_shard'}).id('astropolis:budding_aluminum')
event.shaped('1x geodeopolis:budding_glowstone', ['CBC','BMB','CBC'], {M:'astropolis:miners_research_pack', C: 'minecraft:glowstone', B: 'caveopolis:bright_shard'}).id('astropolis:budding_glowstone')
event.shaped('1x geodeopolis:budding_lead', ['CBC','BMB','CBC'], {M:'astropolis:miners_research_pack', C: '#forge:ingots/lead', B: 'caveopolis:bright_shard'}).id('astropolis:budding_lead')
event.shaped('1x geodeopolis:budding_lapis', ['CBC','BMB','CBC'], {M:'astropolis:miners_research_pack', C: '#forge:gems/lapis', B: 'caveopolis:bright_shard'}).id('astropolis:budding_lapis')
event.shaped('1x geodeopolis:budding_nickel', ['CBC','BMB','CBC'], {M:'astropolis:miners_research_pack', C: '#forge:ingots/nickel', B: 'caveopolis:bright_shard'}).id('astropolis:budding_nickel')

event.shaped('1x geodeopolis:cluster_template', ['SSS','S S','SSS'], {S:'caveopolis:bright_shard'}).id('astropolis:cluster_template')

//Never Ender Ores

event.shaped('1x astropolis:never_ender_ore_base', ['DCD','DAD','DCD'], {D:'minecraft:deepslate', C:'cosmopolis:cheese', A:'cosmopolis:alien_artifact'}).id('astropolis:never_ender_ore_base')
event.shaped('1x neverenderore:ore_remover', ['DAD',' S ',' S '], {S:'#forge:rods/wooden', D:'minecraft:diamond', A:'cosmopolis:alien_artifact'}).id('astropolis:ore_remover')
event.shaped('1x neverenderore:ore_extractor', ['SSS','OAO','SSS'], {S:'#forge:stone', O:'neverenderore:ore_remover', A:'cosmopolis:alien_artifact'}).id('astropolis:ore_extractor')


function neverenderoreOres(ore){
event.shaped(`1x neverenderore:never_ender_${ore}_ore`, ['OOO','EBE','OOO'], {O:`#forge:storage_blocks/${ore}`, B:'astropolis:never_ender_ore_base', E:'rftoolsbase:infused_enderpearl'}).id(`astropolis:never_ender_${ore}_ore`)
}

neverenderoreOres('coal')
neverenderoreOres('redstone')
neverenderoreOres('copper')
neverenderoreOres('diamond')
neverenderoreOres('emerald')
neverenderoreOres('gold')
neverenderoreOres('iron')
neverenderoreOres('lapis')
neverenderoreOres('lead')
neverenderoreOres('nickel')
neverenderoreOres('osmium')
neverenderoreOres('quartz')
neverenderoreOres('silver')
neverenderoreOres('tin')
neverenderoreOres('uranium')
neverenderoreOres('aluminium') 

event.shaped(`1x neverenderore:never_ender_ruby_ore`, ['OOO','EBE','OOO'], {O:`astropolis:ruby`, B:'astropolis:never_ender_ore_base', E:'rftoolsbase:infused_enderpearl'}).id(`astropolis:never_ender_ruby_ore`)
event.shaped(`1x neverenderore:never_ender_sapphire_ore`, ['OOO','EBE','OOO'], {O:`astropolis:sapphire`, B:'astropolis:never_ender_ore_base', E:'rftoolsbase:infused_enderpearl'}).id(`astropolis:never_ender_sapphire_ore`)
event.shaped(`1x neverenderore:never_ender_sulfur_ore`, ['OOO','EBE','OOO'], {O:`#forge:dusts/sulfur`, B:'astropolis:never_ender_ore_base', E:'rftoolsbase:infused_enderpearl'}).id(`astropolis:never_ender_sulfur_ore`)


event.shaped('3x mekanism:dust_sulfur', [' S ','SSS',' S '], {S:'neverenderore:raw_never_ender_sulfur'}).id('astropolis:sulfur')
event.shaped('3x minecraft:redstone', [' S ','SSS',' S '], {S:'neverenderore:raw_never_ender_redstone'}).id('astropolis:redstone')
event.shaped('3x minecraft:quartz', [' S ','SSS',' S '], {S:'neverenderore:raw_never_ender_quartz'}).id('astropolis:quartz')
event.shaped('3x minecraft:lapis_lazuli', [' S ','SSS',' S '], {S:'neverenderore:raw_never_ender_lapis'}).id('astropolis:lapis_lazuli')
event.shaped('3x minecraft:coal', [' S ','SSS',' S '], {S:'neverenderore:raw_never_ender_coal'}).id('astropolis:coal')
event.shaped('1x minecraft:emerald', [' S ','SSS',' S '], {S:'neverenderore:raw_never_ender_emerald'}).id('astropolis:emerald')
event.shaped('1x minecraft:diamond', [' S ','SSS',' S '], {S:'neverenderore:raw_never_ender_diamond'}).id('astropolis:diamond')
event.shaped('1x astropolis:sapphire', [' S ','SSS',' S '], {S:'neverenderore:raw_never_ender_sapphire'}).id('astropolis:sapphire')
event.shaped('1x astropolis:ruby', [' S ','SSS',' S '], {S:'neverenderore:raw_never_ender_ruby'}).id('astropolis:ruby')
event.shaped('1x mekanism:dust_sulfur', [' S ','SSS',' S '], {S:'neverenderore:raw_never_ender_sulfur'}).id('astropolis:sulfur')


//Opolis Utilities

event.shaped('1x opolisutilities:resource_generator', ['IPI','CCC','IPI'], {I: 'minecraft:ice', C: 'ae2:sky_stone_chest', P: 'cosmopolis:artificial_planks'}).id('opolisutilities:resource_generator/resource_generator')
event.shaped('1x opolisutilities:resource_generator_2', ['LPL', 'CCC', 'LPL'], {L: '#minecraft:logs', P: '#minecraft:planks', C: 'ae2:sky_stone_chest'}).id('opolisutilities:resource_generator_2')
event.custom({type: "opolisutilities:resource_generator", ingredients: [{item: "cosmopolis:asteroid_block"}], duration: 200, output: {item: "cosmopolis:asteroid_block"}}).id('astropolis:rg_asteroid_block')
event.custom({type: "opolisutilities:resource_generator", ingredients: [{item: "minecraft:cobbled_deepslate"}], duration: 200, output: {item: "minecraft:cobbled_deepslate"}}).id('astropolis:rg_cobbled_deepslate_block')

event.shaped('1x opolisutilities:drying_table', ['AAA','AAA','A A'], {A: 'cosmopolis:artificial_stick'}).id('astropolis:drying_table')
event.custom({type: "opolisutilities:drying_table", ingredients: [{tag: "forge:cobblestone"}], duration: 80, output: {item: "minecraft:gravel"}}).id('astropolis:dt_gravel')
event.custom({type: "opolisutilities:drying_table", ingredients: [{item: "minecraft:gravel"}], duration: 80, output: {item: "minecraft:sand"}}).id('astropolis:dt_sand')
event.custom({type: "opolisutilities:drying_table", ingredients: [{item: "cosmopolis:water_drop"}], duration: 80, output: {item: "minecraft:snowball"}}).id('astropolis:dt_snowball')
event.custom({type: "opolisutilities:drying_table", ingredients: [{item: "immersiveengineering:ersatz_leather"}], duration: 80, output: {item: "minecraft:leather"}}).id('astropolis:dt_leather')
event.custom({type: "opolisutilities:drying_table", ingredients: [{item: "cosmopolis:ice_shard"}], duration: 80, output: {item: "cosmopolis:water_drop"}}).id('astropolis:dt_more_string')

//Jet Boots

event.shaped('1x jetboots:armor_core', ['G G','GGG','GGG'], {G: 'jetboots:obsidian_infused_gold'}).id('jetboots:armor_core')
event.shaped('1x jetboots:rocket_boots', ['GCG','G G'], {G: 'jetboots:obsidian_infused_gold', C: 'jetboots:armor_core'}).id('jetboots:rocket_boots')
event.shaped('1x jetboots:guardian_helmet', ['GGG','GCG'], {G: 'jetboots:obsidian_infused_gold', C: 'jetboots:armor_core'}).id('jetboots:guardian_helmet')
event.shaped('1x jetboots:guardian_jacket', ['GCG','GGG', 'GGG'], {G: 'jetboots:obsidian_infused_gold', C: 'jetboots:armor_core'}).id('jetboots:guardian_jacket')
event.shaped('1x jetboots:guardian_pants', ['GGG','GCG', 'G G'], {G: 'jetboots:obsidian_infused_gold', C: 'jetboots:armor_core'}).id('jetboots:guardian_pants')

//Functional Storage

event.shaped('1x functionalstorage:framed_1', ['CCC','CDC','CCC'], {D: '#forge:chests/wooden', C: 'cosmopolis:mini_charcoal'}).id('functionalstorage:framed_1')
event.shaped('2x functionalstorage:framed_2', ['CDC','CCC','CDC'], {D: '#forge:chests/wooden', C: 'cosmopolis:mini_charcoal'}).id('functionalstorage:framed_2')
event.shaped('4x functionalstorage:framed_4', ['DCD','CCC','DCD'], {D: '#forge:chests/wooden', C: 'cosmopolis:mini_charcoal'}).id('functionalstorage:framed_4')
event.shaped('1x functionalstorage:compacting_framed_drawer', ['CCC','CDC','CCC'], {D: 'functionalstorage:compacting_drawer', C: 'cosmopolis:mini_charcoal'})
event.shaped('1x functionalstorage:configuration_tool', ['F F',' C ',' F '], {F: 'functionalstorage:framed_1', C: 'minecraft:charcoal'}).id('functionalstorage:configuration_tool')
event.shaped('1x functionalstorage:linking_tool', ['F F',' C ',' F '], {C: 'functionalstorage:configuration_tool', F: 'minecraft:charcoal'}).id('functionalstorage:linking_tool')
event.shaped('1x functionalstorage:storage_controller', ['AGA','GLG','AGA'], {G: '#forge:glass/colorless', A: 'cosmopolis:asteroid_block', L: 'functionalstorage:configuration_tool'}).id('functionalstorage:storage_controller')
event.shaped('1x functionalstorage:compacting_drawer', ['AAA','GHG','AAA'], {G: '#forge:glass/colorless', A: 'cosmopolis:asteroid_block', H: 'cosmopolis:hammer'}).id('functionalstorage:compacting_drawer')

event.shaped('1x functionalstorage:void_upgrade', ['MIM','IDI','MIM'], {I: 'trashcans:item_trash_can', D: '#functionalstorage:drawer', M: 'astropolis:machinist_research_pack'}).id('functionalstorage:void_upgrade')

//Immersive (Decor)

event.shaped('6x engineersdecor:metal_bar', [' CB','CBC','BC '], {B: 'mekanism:ingot_bronze', C: 'minecraft:coal'}).id('astropolis:metal_bar')
event.shaped('1x engineersdecor:small_freezer', ['MMM','MCM','MBM'], {B: 'engineersdecor:fluid_barrel', M: 'engineersdecor:metal_bar', C: 'astropolis:machinist_research_pack'}).id('engineersdecor:independent/small_freezer_recipe')


//Immersive (Crafting)

event.shaped('1x immersiveengineering:thermoelectric_generator', ['EEE','BFB','BBB'], {B: 'minecraft:bricks', F: 'supplementaries:flint_block', E: 'pipez:energy_pipe'}).id('immersiveengineering:crafting/thermoelectric_generator')
event.shaped('1x immersiveengineering:cloche', ['GGG','APA','AAA'], {G: '#forge:glass', A: 'cosmopolis:artificial_planks', P: 'cosmopolis:organic_powder'}).id('immersiveengineering:crafting/cloche')
event.shaped('9x immersiveengineering:blastbrick', ['BAB','AFA','BAB'], {B: 'minecraft:brick', A: 'supplementaries:ash_brick', F: 'supplementaries:flint_block'}).id('immersiveengineering:crafting/blastbrick')
event.shaped('3x immersiveengineering:cokebrick', ['BAB','AFA','BAB'], {B: 'minecraft:clay_ball', A: 'supplementaries:ash_brick', F: '#forge:sandstone'}).id('immersiveengineering:crafting/cokebrick')

event.shaped('2x immersiveengineering:rs_engineering', ['ICI', 'CMC', 'ICI'], {I: 'minecraft:iron_ingot', M:'astropolis:machinist_research_pack', C: 'minecraft:copper_ingot'}).id('immersiveengineering:crafting/rs_engineering')
event.shaped('1x immersiveengineering:component_steel', [' SC', 'SMS', 'CS '], {C:'minecraft:copper_ingot', M:'astropolis:machinist_research_pack', S: 'mekanism:ingot_steel'}).id('immersiveengineering:crafting/component_steel')
event.shaped('4x immersiveengineering:heavy_engineering', ['BSB', 'SMS', 'BSB'], {B:'mekanism:ingot_bronze', S:'immersiveengineering:component_steel', M:'astropolis:machinist_research_pack'}).id('immersiveengineering:crafting/heavy_engineering')
event.shaped('8x immersiveengineering:conveyor_basic', ['LLL', 'IMI'], {L:'#forge:leather', I: 'minecraft:iron_ingot', M:'astropolis:machinist_research_pack'}).id('immersiveengineering:crafting/conveyor_basic')
event.shaped('8x immersiveengineering:ersatz_leather', ['TT', 'TT'], {T:'immersiveengineering:hemp_fabric'}).id('immersiveengineering:crafting/ersatz_leather')
event.shaped('1x immersiveengineering:seed', ['LLL', 'LOL', 'LLL'], {L:'#minecraft:leaves', O:'cosmopolis:organic_powder'}).id('astropolis:hemp_seed')

event.shaped('1x immersiveengineering:component_iron', [' SC', 'SMS', 'CS '], {C:'minecraft:copper_ingot', M:'astropolis:machinist_research_pack', S: 'minecraft:iron_ingot'}).id('immersiveengineering:crafting/component_iron')
event.shaped('4x immersiveengineering:light_engineering', ['BSB', 'SMS', 'BSB'], {B:'mekanism:ingot_bronze', S:'immersiveengineering:component_iron', M:'astropolis:machinist_research_pack'}).id('immersiveengineering:crafting/light_engineering')

event.shaped('1x immersiveengineering:hammer', [' A ', ' SA', 'S  '], {S:'#forge:rods/wooden', A:'supplementaries:ash_brick'}).id('immersiveengineering:crafting/hammer')
event.shaped('8x immersiveengineering:treated_wood_horizontal', ['PPP', 'PBP', 'PPP'], {P:'#minecraft:planks', B: Item.of('ceramicbucket:ceramic_bucket', '{Fluid:{Amount:1000,FluidName:"immersiveengineering:creosote"}}').strongNBT()}).id('astropolis:treated_wood')

event.shaped('1x immersiveengineering:stick_steel', ['III'], {I: 'mekanism:ingot_steel'}).id('immersiveengineering:crafting/stick_steel')
event.shaped('1x immersiveengineering:stick_aluminum', ['III'], {I: 'immersiveengineering:ingot_aluminum'}).id('immersiveengineering:crafting/stick_aluminum')
event.shaped('1x immersiveengineering:stick_iron', ['III'], {I: 'minecraft:iron_ingot'}).id('immersiveengineering:crafting/stick_iron')

event.shaped('1x immersiveengineering:hemp_fiber', ['III'], {I: 'immersiveengineering:seed'}).id('astropolis:hemp')

event.shaped('1x immersiveengineering:mold_plate', ['SSS', 'S S', 'SSS'], {S: '#forge:ingots/steel'})
event.shaped(Item.of('immersiveengineering:blueprint', '{blueprint:"electrode"}'), [' D ', 'BBB', 'PPP'], {P: 'minecraft:paper', B:'minecraft:blue_dye', D:'immersiveengineering:dust_hop_graphite'}).id('astropolis:blueprint_electrode')
event.shaped(Item.of('immersiveengineering:blueprint', '{blueprint:"components"}'), [' D ', 'BBB', 'PPP'], {P: 'minecraft:paper', B:'minecraft:blue_dye', D:'astropolis:machinist_research_pack'}).id('immersiveengineering:crafting/blueprint_components')

event.custom({type: "immersiveengineering:thermoelectric_source", singleBlock:"supplementaries:flint_block", tempKelvin:1100})

event.custom({type: "immersiveengineering:blast_furnace", result :{"item":"opolisutilities:copper_nugget"}, input:{item:"cosmopolis:asteroid_block"}, slag:{item:"cosmopolis:asteroid_rock"}, time:120}).id('astropolis:bf_copper_nugget')
event.custom({type: "immersiveengineering:blast_furnace", result :{"item":"mekanism:nugget_tin"}, input:{item:"minecraft:andesite"}, slag:{item:"cosmopolis:rock"}, time:120}).id('astropolis:bf_tin_nugget')
event.custom({type: "immersiveengineering:blast_furnace", result :{"item":"minecraft:iron_nugget"}, input:{item:"engineersdecor:metal_bar"}, slag:{item:"cosmopolis:mini_coal"}, time:120}).id('astropolis:bf_iron_nugget')

event.custom({type:"immersiveengineering:sawmill",energy:1600,input:[{item:"minecraft:mangrove_log"},{item:"minecraft:mangrove_wood"}],result:{count:6,item:"minecraft:mangrove_planks"},secondaries:[{output:{item:"mekanism:sawdust"},"stripping":true},{output:{item:"mekanism:sawdust"},stripping:false}],stripped:{item:"minecraft:stripped_mangrove_log"}})
event.custom({type:"immersiveengineering:sawmill",energy:1600,input:[{item:"quark:azalea_log"},{item:"quark:azalea_wood"}],result:{count:6,item:"quark:azalea_planks"},secondaries:[{output:{item:"mekanism:sawdust"},"stripping":true},{output:{item:"mekanism:sawdust"},stripping:false}],stripped:{item:"quark:stripped_azalea_log"}})
event.custom({type:"immersiveengineering:sawmill",energy:1600,input:[{item:"quark:blossom_log"},{item:"quark:blossom_wood"}],result:{count:6,item:"quark:blossom_planks"},secondaries:[{output:{item:"mekanism:sawdust"},"stripping":true},{output:{item:"mekanism:sawdust"},stripping:false}],stripped:{item:"quark:stripped_blossom_log"}})

event.custom({type:"immersiveengineering:sawmill",energy:1600,input:[{item:"cosmopolis:asteroid_block"}],result:{count:1,item:"cosmopolis:asteroid_rock"},secondaries:[{output:{item:"cosmopolis:organic_powder"},"stripping":true},{output:{item:"cosmopolis:ice_shard"},stripping:false}, {output:{item:"cosmopolis:rock"},stripping:false}, {output:{item:"cosmopolis:water_drop"},stripping:false}],stripped:{item:"cosmopolis:asteroid_block"}})

/*

event.custom({type:"immersiveengineering:arc_furnace", additives:[], energy:51200, input :{tag:"forge:ingots/copper"}, results:[{item:"minecraft:redstone"}],time:100})
event.custom({type:"immersiveengineering:arc_furnace", additives:[], energy:51200, input :{tag:"forge:ingots/iron"}, results:[{item:"minecraft:gold_ingot"}],time:100})
event.custom({type:"immersiveengineering:arc_furnace", additives:[], energy:51200, input :{tag:"forge:ingots/iron"}, results:[{item:"minecraft:gold_ingot"}],time:100})

*/

//Immersive (Arc Furnace)

event.custom({type:"immersiveengineering:arc_furnace", additives:[{item:"immersiveengineering:dust_coke"}], energy:25600, 
  input:{tag:"forge:ingots/steel"}, 
  results:[{item:"cosmopolis:space_suit_upgrade"}],
  time:400}).id('cosmopolis:space_suit_upgrade')

event.custom({type:"immersiveengineering:arc_furnace", additives:[], energy:6400, 
  input:{item:"ae2:certus_quartz_dust"}, 
  results:[{item:"ae2:certus_quartz_crystal"}],
  time:100}).id('astropolis:certus_quartz_crystal')

event.custom({type:"immersiveengineering:arc_furnace", additives:[], energy:6400, 
  input:{item:"ae2:fluix_dust"}, 
  results:[{item:"ae2:fluix_crystal"}],
  time:100}).id('astropolis:fluix_crystal')

event.custom({type:"immersiveengineering:arc_furnace", additives:[{item:"ae2:certus_quartz_dust"}, {item: "minecraft:redstone"}, {item: "minecraft:glowstone_dust"}, {tag: "forge:dusts/electrum"}], energy:12800, 
  input:{item:"ae2:charged_certus_quartz_crystal"}, 
  results:[{base_ingredient:{"item":"ae2:fluix_dust"},"count":4}],
  time:100}).id('astropolis:fluix_dust')

event.custom({type:"immersiveengineering:arc_furnace", additives:[{item:"ae2:silicon"}, {item: "minecraft:quartz"}], energy:6400, 
  input:{item:"minecraft:glass"}, 
  results:[{base_ingredient:{"item":"ae2:quartz_glass"},"count":1}],
  time:100}).id('ae2:decorative/quartz_glass')

event.custom({type:"immersiveengineering:arc_furnace", additives:[], energy:6400, 
  input:{item:"ae2:fluix_block"}, 
  results:[{item:"minecraft:obsidian"}],
  time:100}).id('astropolis:obsidian')

event.custom({type:"immersiveengineering:arc_furnace", additives:[{item:"minecraft:obsidian"}], energy:6400, 
  input:{item:"minecraft:gold_ingot"}, 
  results:[{base_ingredient:{"item":"jetboots:obsidian_infused_gold"},"count":2}],
  time:100}).id('jetboots:obsidian_infused_gold')

event.custom({type:"immersiveengineering:arc_furnace", additives:[{item:"immersiveengineering:coal_coke"}], energy:3200,  
  input:{"base_ingredient":{item:"immersiveengineering:treated_wood_horizontal"},"count":8},
  results:[{"base_ingredient":{"item":"engineersdecor:old_industrial_wood_planks"},"count":8}],
  time:100}).id('astropolis:old_industrial_wood_planks')


//Immersive (Blueprints)

event.custom({type:"immersiveengineering:blueprint",category:"components",inputs:[{base_ingredient:{tag:"forge:plates/steel"},count:2},{item:"astropolis:machinist_research_pack"}],result:{item:"immersiveengineering:component_steel"}}).id('immersiveengineering:blueprint/component_steel')
event.custom({type:"immersiveengineering:blueprint",category:"components",inputs:[{base_ingredient:{tag:"forge:plates/iron"},count:2},{item:"astropolis:machinist_research_pack"}],result:{item:"immersiveengineering:component_iron"}}).id('immersiveengineering:blueprint/component_iron')


//Immersive (Squeezer)

event.custom({type:"immersiveengineering:squeezer", energy:400, fluid:{amount:250, fluid:"minecraft:water"},input:{item:"cosmopolis:water_drop"}}).id('astropolis:water_drop')
event.custom({type:"immersiveengineering:squeezer", energy:400, fluid:{amount:100, fluid:"minecraft:water"},input:{tag:"minecraft:leaves"}}).id('astropolis:water_leaves')
event.custom({type:"immersiveengineering:squeezer", energy:400, fluid:{amount:100, fluid:"minecraft:water"},input:{tag:"minecraft:saplings"}}).id('astropolis:water_sapling')

//Immersive (Cloche/Saplings)

function saplingsCloche(log, leaves, sapling){
  event.custom({type:"immersiveengineering:cloche", input:{item: sapling}, render:{type: "generic", block: sapling},
  results:[{"count":2, item:log},{item: leaves}], soil :{item: "minecraft:dirt"},"time":640}).id(`${sapling}_in_cloche`)}

  saplingsCloche('minecraft:oak_log', 'minecraft:oak_leaves', 'minecraft:oak_sapling')
  saplingsCloche('minecraft:dark_oak_log', 'minecraft:dark_oak_leaves', 'minecraft:dark_oak_sapling')
  saplingsCloche('minecraft:birch_log', 'minecraft:birch_leaves', 'minecraft:birch_sapling')
  saplingsCloche('minecraft:spruce_log', 'minecraft:spruce_leaves', 'minecraft:spruce_sapling')
  saplingsCloche('minecraft:jungle_log', 'minecraft:jungle_leaves', 'minecraft:jungle_sapling')
  saplingsCloche('minecraft:acacia_log', 'minecraft:acacia_leaves', 'minecraft:acacia_sapling')
  saplingsCloche('quark:azalea_log', 'minecraft:azalea_leaves', 'minecraft:azalea')
  saplingsCloche('quark:azalea_log', 'minecraft:flowering_azalea_leaves', 'minecraft:flowering_azalea')
  saplingsCloche('minecraft:mangrove_log', 'minecraft:mangrove_leaves', 'minecraft:mangrove_propagule')

  saplingsCloche('quark:blossom_log', 'quark:yellow_blossom_leaves', 'quark:yellow_blossom_sapling')
  saplingsCloche('quark:blossom_log', 'quark:pink_blossom_leaves', 'quark:pink_blossom_sapling')
  saplingsCloche('quark:blossom_log', 'quark:blue_blossom_leaves', 'quark:blue_blossom_sapling')
  saplingsCloche('quark:blossom_log', 'quark:lavender_blossom_leaves', 'quark:lavender_blossom_sapling')
  saplingsCloche('quark:blossom_log', 'quark:orange_blossom_leaves', 'quark:orange_blossom_sapling')
  saplingsCloche('quark:blossom_log', 'quark:red_blossom_leaves', 'quark:red_blossom_sapling')

//Non Geodeopolis Geodes

function geodeCloche(geode, outCrystal, inCrystal){
  event.custom({type:"immersiveengineering:cloche", input:{item: inCrystal}, render:{type: "generic", block: outCrystal},
  results:[{item: outCrystal}], soil :{item: geode},"time":1000})}

  geodeCloche('ae2:flawless_budding_quartz', 'ae2:quartz_cluster', 'geodeopolis:cluster_template')
  geodeCloche('minecraft:dirt', 'supplementaries:flax', 'supplementaries:flax_seeds')

event.custom({
  "type":"immersiveengineering:crusher",
  "energy":3000,
  "input":{"item":"ae2:quartz_cluster"},
  "result":{"base_ingredient":{"item":"ae2:certus_quartz_crystal"},
  "count":6},
  "secondaries":[]
}).id('astropolis:certus_in_a_crusher')

//Engineers Decor

event.shaped('1x engineersdecor:small_lab_furnace', ['MHM','MAM','OFO'], {O:'engineersdecor:old_industrial_wood_planks', A: 'minecraft:furnace', M: 'engineersdecor:metal_bar', F: 'astropolis:machinist_research_pack', H: 'minecraft:hopper'}).id('engineersdecor:independent/small_lab_furnace_recipe')
event.shaped('1x engineersdecor:small_block_breaker', ['OMO','MFP','OMO'], {O:'engineersdecor:old_industrial_wood_planks', M: 'engineersdecor:metal_bar', F: 'astropolis:machinist_research_pack', P: 'cosmopolis:asteroid_pickaxe'}).id('engineersdecor:independent/small_block_breaker_recipe')

//Flux Networks

event.shaped('8x fluxnetworks:flux_dust', ['RDR','CEC','RDR'], {C:'#forge:dusts/coal', E: '#forge:dusts/emerald', R: 'minecraft:redstone', D: 'mekanism:dust_refined_obsidian'}).id('astropolis:flux_dust_emerald')
event.shaped('8x fluxnetworks:flux_dust', ['RDR','CEC','RDR'], {C:'#forge:dusts/coal', E: '#forge:dusts/diamond', R: 'minecraft:redstone', D: 'mekanism:dust_refined_obsidian'}).id('astropolis:flux_dust_diamond')

event.shaped('1x fluxnetworks:flux_block', [' F ','FCF',' F '], {C:'fluxnetworks:flux_core', F: 'fluxnetworks:flux_dust'}).id('fluxnetworks:fluxblock')
event.shaped('1x fluxnetworks:flux_controller', ['FCF','1M2','FFF'], {1:'fluxnetworks:flux_plug', 2:'fluxnetworks:flux_point', C:'fluxnetworks:flux_core', F: 'fluxnetworks:flux_block', M: 'astropolis:machinist_research_pack'}).id('fluxnetworks:fluxcontroller')


/*


//Placing Strucutres

ItemEvents.rightClicked(event => {
  const {player, server} = event
  if(player.mainHandItem === 'astropolis:fission_reactor' ) {
    
          if (event.hand != "MAIN_HAND") return; {
              server.runCommandSilent(`particle minecraft:lava ~ ~1 ~ 0.5 0 0.5 1 20 normal`)
              server.runCommandSilent(`loot give @p loot cryptopolis:lava_loot`)
              event.item.setCount(event.item.getCount() - 1)
              event.player.give('cryptopolis:non_flammable_bowl')
              event.player.swingArm(event.hand);
          }
      
  }
})
*/



//Remove

event.remove({id:'ae2:smelting/silicon_from_certus_quartz_dust'})
event.remove({id:'caveopolis:charcoal_fragment'})
event.remove({id:'caveopolis:coal_fragment'})
event.remove({id:'cosmopolis:armor/space_portal_frame'})
event.remove({id:'engineersdecor:dependent/old_industrial_planks_recipe'})
event.remove({id:'engineersdecor:dependent/old_industrial_planks_recipe_vmirrored'})
event.remove({id:'tiab:time_in_a_bottle'})
event.remove({id:'ae2:transform/fluix_crystals'})
event.remove({id:'ae2:transform/fluix_crystal'})
event.remove({id:'immersiveengineering:crafting/paper_from_sawdust'})
event.remove({id:'cosmopolis:gravity_generator'})
event.remove({id:'caveopolis:fragments/glowstone'})

  
//Replace

event.replaceInput({id: 'rechiseled:chisel'}, 'minecraft:iron_ingot', 'minecraft:flint')
event.replaceInput({id: 'rechiseled:chisel'}, '#forge:rods/wooden', 'cosmopolis:artificial_stick')
event.replaceInput({id: 'immersiveengineering:crafting/furnace_heater'}, 'minecraft:redstone', 'minecraft:flint')

event.replaceInput({id: 'engineersdecor:independent/factory_placer_recipe'}, 'minecraft:dispenser', 'astropolis:machinist_research_pack')
event.replaceInput({id: 'engineersdecor:independent/factory_dropper_recipe'}, 'minecraft:dropper', 'astropolis:machinist_research_pack')
event.replaceInput({id: 'engineersdecor:independent/small_electrical_furnace_recipe'}, 'minecraft:furnace', 'engineersdecor:small_lab_furnace')
event.replaceInput({id: 'engineersdecor:independent/factory_hopper_recipe'}, 'engineersdecor:metal_bar', 'engineersdecor:old_industrial_wood_planks')

event.replaceInput({id: 'quark:tweaks/crafting/utility/misc/charcoal_to_black_dye'}, 'minecraft:charcoal', 'cosmopolis:mini_charcoal')
event.replaceInput({id: 'watersources:water_source_tier_1'}, 'minecraft:water_bucket', 'astropolis:water_core')
event.replaceInput({id: 'watersources:water_source_tier_2'}, 'minecraft:glass_pane', 'engineersdecor:old_industrial_wood_planks')

event.replaceInput({id: 'cosmopolis:organic_powder_fungus_block'}, '#forge:mushrooms', 'minecraft:string')
event.replaceInput({id: 'rftoolsbase:dimensionalshard'}, 'minecraft:glass', 'cosmopolis:cheese')

event.replaceInput({id: 'immersiveengineering:crafting/workbench'}, 'minecraft:iron_ingot', 'minecraft:flint')
event.replaceInput({id: 'minecraft:hopper'}, 'minecraft:chest', '#forge:chests/wooden')

event.replaceInput({mod: 'functionalstorage'}, 'minecraft:hopper', 'woodenhopper:wooden_hopper')
event.replaceInput({mod: 'extendedcrafting'}, 'minecraft:nether_star', 'astropolis:ingot_of_ingots')
event.replaceInput({mod: 'constructionwand'}, 'minecraft:nether_star', 'astropolis:ingot_of_ingots')
})
