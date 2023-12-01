class Circut
  @@Symb_map = {
    'AND' => :&,
    'OR' => :|,
    'RSHIFT' => :>>,
    'LSHIFT' => :<<
  }.freeze

  def initialize
    @dependency = Hash.new
    @eval_res = Hash.new
  end

  def add_rec(line)
    x, y = line.split(' -> ')
    @dependency[y] = x.split
  end

  def cal(name)
    if name.match? /\d+/
      return name.to_i
    end

    unless @eval_res.include? name
      dep = @dependency[name]
      @eval_res[name] = \
        case dep.size
        when 1
          dep[0].match?(/\d+/) ? dep[0].to_i : cal(dep[0])
        when 2
          65536 + ~cal(dep[1])
        when 3
          cal(dep[0]).send(@@Symb_map.fetch(dep[1]), cal(dep[2]))
        end
    end
    @eval_res.fetch name
  end

  def reset
    @eval_res.clear
  end
end

inp = File.read('input7')

# part 1
circ = Circut.new
inp.each_line { |line| circ.add_rec line.chomp }
a_val = circ.cal 'a'
puts a_val

# part 2
circ.reset
circ.add_rec "#{a_val} -> b"
puts circ.cal 'a'
