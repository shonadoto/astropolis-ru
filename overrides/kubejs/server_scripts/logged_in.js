// Listen to player login event
/*

onEvent('player.logged_in', event => {
    // Check if player doesn't have "starting_items" stage yet
    if (!event.player.stages.has('starting_items_new')) {
      // Add the stage
      event.player.stages.add('starting_items_new')
      // Give some items to player
      event.player.setEquipment(SLOT_HEAD, Item.of('cosmopolis:space_suit_helmet'))
      event.player.setEquipment(SLOT_LEGS, Item.of('cosmopolis:space_suit_chestplate'))
      event.player.setEquipment(SLOT_CHEST, Item.of('cosmopolis:space_suit_leggings'))
      event.player.setEquipment(SLOT_FEET, Item.of('cosmopolis:space_suit_boots'))
    }
  })

  */