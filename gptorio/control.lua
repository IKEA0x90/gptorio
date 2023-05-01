local json = require("json")

local file_name = "events.txt"

function append_event(data)
  local event_json = json.encode(data)
  -- game.print(event_json)
  local file = game.write_file(file_name, event_json .. "\n", true)
end

function on_built_entity(event)
  if event.created_entity.name ~= "entity-ghost" or event.created_entity.name ~= "tile-ghost" then 
    local data = {
      type = "on_built_entity",
      data = {
        player = game.get_player(event.player_index).name,
        entity = event.created_entity.name
      }
    }
    append_event(data)
  end
end

function on_build_base_arrived(event)
  local data = {
    type = "on_build_base_arrived",
    data = {
    }
  }
  append_event(data)
end

function on_cancelled_upgrade(event)
  local player
  if event.player_index then player = game.get_player(event.player_index).name 
  else player = "unkown player" end 
  local data = {
    type = "on_cancelled",
    data = {
      cancel = "upgrade",
      player = player,
      entity = event.entity.name
    }
  }

  append_event(data)
end

function on_character_corpse_expired(event)
  local data = {
    type = "on_character_corpse_expired",
    data = {
    }
  }
  append_event(data)
end

function on_chunk_generated(event)
  local data = {
    type = "on_chunk_generated",
    data = {
      surface = event.surface.name
    }
  }
  append_event(data)
end

function on_console_command(event)
  local player
  if event.player_index then player = game.get_player(event.player_index).name 
  else player = "unkown player" end
  local data = {
    type = "on_console_command",
    data = {
      player = game.get_player(event.player_index).name
    }
  }
  append_event(data)
end

function on_entity_died(event)
  if event.entity.name ~= "character" then
    local data = {
      type = "on_entity_died",
      data = {
        entity = event.entity.name,
        cause = event.cause.name or "unkown cause"
      }
    }
    append_event(data)
  end
end

function on_player_built_tile(event)
  local data = {
    type = "on_built_entity",
    data = {
      player = game.get_player(event.player_index).name,
      entity = event.tile.name
    }
  }
  append_event(data)
end

function on_player_changed_surface(event)
  local data = {
    type = "on_player_changed_surface",
    data = {
      player = game.get_player(event.player_index).name,
      old_surface = game.get_surface(event.surface_index).name,
      new_surface = game.get_player(event.player_index).surface.name
    }
  }
  append_event(data)
end

function on_player_died(event)
  local data = {
    type = "on_player_died",
    data = {
      player = game.get_player(event.player_index).name,
      cause = event.cause.name or "unkown cause"
    }
  }
  append_event(data)
end

function on_player_flushed_fluid(event)
  local data = {
    type = "on_player_flushed_fluid",
    data = {
      player = game.get_player(event.player_index).name,
      fluid = event.fluid,
      amount = event.amount
    }
  }
  append_event(data)
end

function on_player_left_game(event)
  local data = {
    type = "on_player_left_game",
    data = {
      player = game.get_player(event.player_index).name
    }
  }
  append_event(data)
end

function on_robot_built_entity(event)
  local data = {
    type = "on_robot_built_entity",
    data = {
      entity = event.created_entity.name
    }
  }
  append_event(data)
end

function on_robot_mined(event)
  local data = {
    type = "on_robot_mined",
    data = {
      entity = event.item_stack.name
    }
  }
  append_event(data)
end

function on_rocket_launched(event)
  local data = {
    type = "on_rocket_launched",
    data = {
    }
  }
  append_event(data)
end

function on_player_mined_entity(event)
  if event.entity.name ~= "entity-ghost" or event.entity.name ~= "tile-ghost" then 
    local data = {
      type = "on_player_mined_entity",
      data = {
        player = game.get_player(event.player_index).name,
        entity = event.entity.name
      }
    }
    append_event(data)
  end
end

function on_research_finished(event)
  local data = {
    type = "on_research_finished",
    data = {
      research = event.research.name
    }
  }
  append_event(data)
end

function on_player_joined_game(event)
  local data = {
    type = "on_player_joined_game",
    data = {
      player = game.get_player(event.player_index).name,
    }
  }
  append_event(data)
end

function on_player_crafted_item(event)
  local data = {
    type = "on_player_crafted_item",
    data = {
      player = game.get_player(event.player_index).name,
      item = event.item_stack.name
    }
  }
  append_event(data)
end

function on_train_created(event)
  local data = {
    type = "on_train_created",
    data = {
    }
  }
  append_event(data)
end

function on_cancelled_deconstruction(event)
  local player
  if event.player_index then player = game.get_player(event.player_index).name 
  else player = "unkown player" end 
  local data = {
    type = "on_cancelled",
    data = {
      cancel = "deconstruction",
      entity = event.entity.name,
      player = player
    }
  }
  append_event(data)
end

function on_marked_for_upgrade(event)
  local player
  if event.player_index then player = game.get_player(event.player_index).name 
  else player = "unkown player" end 
  local data = {
    type = "on_marked",
    data = {
      marked = "upgrade",
      entity = event.entity.name,
      player = player
    }
  }
  append_event(data)
end

function on_marked_for_deconstruction(event)
  local player
  if event.player_index then player = game.get_player(event.player_index).name 
  else player = "unkown player" end 
  local data = {
    type = "on_marked",
    data = {
      marked = "deconstruction",
      entity = event.entity.name,
      player = player
    }
  }
  append_event(data)
end

function on_robot_built_tile(event)
  local data = {
    type = "on_robot_built_entity",
    data = {
      entity = event.tile.name
    }
  }
  append_event(data)
end

function on_robot_mined_tile(event)
  local data = {
    type = "on_robot_mined",
    data = {
      entity = event.tile.name
    }
  }
  append_event(data)
end

script.on_event(defines.events.on_built_entity, on_built_entity) --works
script.on_event(defines.events.on_build_base_arrived, on_build_base_arrived) --works
script.on_event(defines.events.on_cancelled_upgrade, on_cancelled_upgrade) --works
script.on_event(defines.events.on_character_corpse_expired, on_character_corpse_expired) --works
script.on_event(defines.events.on_chunk_generated, on_chunk_generated) --works
script.on_event(defines.events.on_console_command, on_console_command) --works
script.on_event(defines.events.on_entity_died, on_entity_died) --works
script.on_event(defines.events.on_player_built_tile, on_player_built_tile) --works
script.on_event(defines.events.on_player_changed_surface, on_player_changed_surface) --works
script.on_event(defines.events.on_player_died, on_player_died) --works
script.on_event(defines.events.on_player_flushed_fluid, on_player_flushed_fluid) --works
script.on_event(defines.events.on_player_left_game, on_player_left_game) --??
script.on_event(defines.events.on_robot_built_entity, on_robot_built_entity) --works
script.on_event(defines.events.on_robot_mined, on_robot_mined) --works
script.on_event(defines.events.on_rocket_launched, on_rocket_launched) --works
script.on_event(defines.events.on_player_mined_entity, on_player_mined_entity) --works
script.on_event(defines.events.on_research_finished, on_research_finished) --works
script.on_event(defines.events.on_player_joined_game, on_player_joined_game) --??
script.on_event(defines.events.on_player_crafted_item, on_player_crafted_item) --works
script.on_event(defines.events.on_train_created, on_train_created) --works
script.on_event(defines.events.on_cancelled_deconstruction, on_cancelled_deconstruction) --works
script.on_event(defines.events.on_marked_for_upgrade, on_marked_for_upgrade) --works
script.on_event(defines.events.on_marked_for_deconstruction, on_marked_for_deconstruction) --works
script.on_event(defines.events.on_robot_built_tile, on_robot_built_tile) --works