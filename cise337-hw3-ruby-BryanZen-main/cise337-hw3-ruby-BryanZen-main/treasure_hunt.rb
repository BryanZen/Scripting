class ValueError < RuntimeError
end

class Cave
  def initialize()
    @edges = [[1, 2], [2, 10], [10, 11], [11, 8], [8, 1], [1, 5], [2, 3], [9, 10], [20, 11], [7, 8], [5, 4],
                      [4, 3], [3, 12], [12, 9], [9, 19], [19, 20], [20, 17], [17, 7], [7, 6], [6, 5], [4, 14], [12, 13],
                      [18, 19], [16, 17], [15, 6], [14, 13], [13, 18], [18, 16], [16, 15], [15, 14]]
    @rooms = {1 => Room.new(1), 2 => Room.new(2), 3 => Room.new(3), 4 => Room.new(4), 5 => Room.new(5),
              6 => Room.new(6), 7 => Room.new(7), 8 => Room.new(8), 9 => Room.new(9), 10 => Room.new(10),
              11 => Room.new(11), 12 => Room.new(12), 13 => Room.new(13), 14 => Room.new(14), 15 => Room.new(15),
              16 => Room.new(16), 17 => Room.new(17), 18 => Room.new(18), 19 => Room.new(19), 20 => Room.new(20)}
    @edges.each { |edge|
      @rooms[edge[0]].connect(@rooms[edge[1]])
    }
    # add cave attributes
  end
  def add_hazard(h, n)
    n.times do
      added = false
      while !added
        x = random_room
        if !x.has?(h)
          x.add(h)
          added = true
        end
      end
    end
  end
  def random_room
    n = rand 1..20
    return @rooms[n]
  end
  def room_with(hazard)
    (1..20).each do |n|
      if @rooms[n].has?(hazard)
        return @rooms[n]
      end
    end
    return nil
  end
  def move(hazard, frm, to)
    if !frm.has?(hazard)
      raise ValueError
    end
    frm.remove(hazard)
    to.add(hazard)
  end
  def room(n)
    if @rooms.key?(n)
      return @rooms[n]
    else
      return nil
    end
  end
  def entrance
    (1..20).each do |n|
      if @rooms[n].safe?
        return @rooms[n]
      end
    end
    return nil
  end
  # add cave methods
end

class Player
  attr_reader :room
  def initialize()
    @senses = {}
    @encounters = {}
    @actions = {}
    @room = nil
  end
  # add specified Player methods
  def sense(hazard, &callback)
    @senses[hazard] = callback
  end
  def encounter(hazard, &callback)
    @encounters[hazard] = callback
  end
  def action(act, &callback)
    @actions[act] = callback
  end
  def enter(room)
    @room = room
    if room.hazards.length() > 0
      @encounters.keys().each { |hazard|
        if room.has?(hazard)
          return @encounters[hazard].call()
        end
      }
      end
  end
  def explore_room
    @room.neighbors.each { |room|
      if room.hazards.length > 0
        room.hazards.each{|hazard|
          @senses[hazard].call()
        }
      end
    }
  end
  def act(action, destination)
    if @actions[action] == nil
      raise KeyError, "No such action #(action)"
    else
      @actions[action].call(destination)
    end
  end
end

class Room
  attr_reader :number, :hazards, :neighbors
  def initialize(room)
    @number = room
    @hazards = []
    @neighbors = []
  end
  def add(hazard)
    @hazards.append(hazard)
  end
  def has?(hazard)
    @hazards.include?(hazard)
  end
  def remove(hazard)
      if @hazards.include?(hazard) == true
        @hazards.delete(hazard)
      else
        raise ValueError
    end
  end
  def empty?
    if @hazards.length > 0
      return false
    else
      return true
    end
  end
  def safe?
    if @hazards.length > 0
      return false
    else
      @neighbors.each { |neighbor|
        if neighbor.hazards.length > 0
          return false
        end
      }
    end
    return true
  end
  def connect(other_room)
    if !@neighbors.include?(other_room)
      @neighbors.append(other_room)
    end
    if !other_room.neighbors.include?(itself)
      other_room.neighbors.append(itself)
    end
  end
  def exits
    l = []
    @neighbors.each { |neighbor|
      l.append(neighbor.number)
    }
    return l
  end
  def neighbor(number)
    @neighbors.each { |neighbor|
      if neighbor.number == number
        return neighbor
      end
    }
    return nil
  end
  def random_neighbor
    if @neighbors.length > 0
      return @neighbors.sample
    else
      raise IndexError
    end
  end
  # add specified Room methods
end

class Console
  def initialize(player, narrator)
    @player   = player
    @narrator = narrator
  end

  def show_room_description
    @narrator.say "-----------------------------------------"
    @narrator.say "You are in room #{@player.room.number}."

    @player.explore_room

    @narrator.say "Exits go to: #{@player.room.exits.join(', ')}"
  end

  def ask_player_to_act
    actions = {"m" => :move, "s" => :shoot, "i" => :inspect }

    accepting_player_input do |command, room_number|
      @player.act(actions[command], @player.room.neighbor(room_number))
    end
  end

  private

  def accepting_player_input
    @narrator.say "-----------------------------------------"
    command = @narrator.ask("What do you want to do? (m)ove or (s)hoot?")

    unless ["m","s"].include?(command)
      @narrator.say "INVALID ACTION! TRY AGAIN!"
      return
    end

    dest = @narrator.ask("Where?").to_i

    unless @player.room.exits.include?(dest)
      @narrator.say "THERE IS NO PATH TO THAT ROOM! TRY AGAIN!"
      return
    end

    yield(command, dest)
  end
end

class Narrator
  def say(message)
    $stdout.puts message
  end

  def ask(question)
    print "#{question} "
    $stdin.gets.chomp
  end

  def tell_story
    yield until finished?

    say "-----------------------------------------"
    describe_ending
  end

  def finish_story(message)
    @ending_message = message
  end

  def finished?
    !!@ending_message
  end

  def describe_ending
    say @ending_message
  end
end
