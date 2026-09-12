/// priority: 0

console.info('Hello, World! (You will only see this line once in console, during startup)')

// New Items

StartupEvents.registry('item', event => {
  event.create('astropolis:machinist_research_pack').texture('astropolis:item/machinist_research_pack')
  event.create('astropolis:foodies_research_pack').texture('astropolis:item/foodies_research_pack')
  event.create('astropolis:miners_research_pack').texture('astropolis:item/miners_research_pack')
  event.create('astropolis:water_core').texture('astropolis:item/water_core')
  event.create('astropolis:ingot_of_ingots').glow(true).texture('astropolis:item/ingot_of_ingots')
  event.create('astropolis:gem_of_gems').glow(true).texture('astropolis:item/gem_of_gems')
  event.create('astropolis:ruby').texture('astropolis:item/ruby')
  event.create('astropolis:sapphire').texture('astropolis:item/sapphire')
  event.create('astropolis:overworld_core').texture('astropolis:item/overworld_core')
  event.create('astropolis:shard_of_shards').glow(true).texture('astropolis:item/shard_of_shards')
  
//  event.create('astropolis:ancient_seeds').texture('astropolis:item/ancient_seeds')
})

BlockEvents.modification(event => {
  event.modify('cosmopolis:asteroid_block', block => {
	  block.destroySpeed = 0.5
	  block.requiresTool = false
	})
})

	


// New Blocks


StartupEvents.registry('block', event => {
  event.create('astropolis:never_ender_ore_base')

})






//Disable Nether Portals

/*

onForgeEvent('net.minecraftforge.event.world.BlockEvent$PortalSpawnEvent', event => {
  event.setCanceled(true)
})
*/

