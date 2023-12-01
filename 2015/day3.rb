require 'set'

WALK_DIR = { '>' => [1, 0], '<' => [-1, 0], '^' => [0, 1], 'v' => [0, -1] }.freeze
class SantaFactory
  attr_reader :house_visited

  def initialize
    @house_visited = Set[[0, 0]]
    @x = 0
    @y = 0
  end

  def walk(dir_sym)
    walk_dir = WALK_DIR[dir_sym]
    @x += walk_dir[0]
    @y += walk_dir[1]
    @house_visited.add([@x, @y])
  end
end

inp = File.read('input3')

# part 1
santa = SantaFactory.new
inp.each_char do |c|
  santa.walk c
end
puts santa.house_visited.size

# part 2
santa = SantaFactory.new
robo_santa = SantaFactory.new
inp.scan(/../).each do |cmd|
  santa.walk cmd[0]
  robo_santa.walk cmd[1]
end
puts (santa.house_visited | robo_santa.house_visited).size
