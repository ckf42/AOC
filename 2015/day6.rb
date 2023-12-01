inp = File.read('input6').split("\n")

light_state = Hash.new(0)

# part 1
# inp.each do |line|
#   cmd = line.split[0]
#   inst = line.scan(/\d+/).map(&:to_i)
#   (inst[0]..inst[2]).to_a.product((inst[1]..inst[3]).to_a).each do |(x, y)|
#     light_state[x * 1000 + y] =
#       (if cmd == 'toggle'
#        then 1 - light_state.fetch(x * 1000 + y, 0)
#        elsif line.split[1] == 'on' then 1 else 0
#        end)
#   end
# end
# puts light_state.each_value.sum

# part 2
inp.each do |line|
  cmd = line.split[0]
  inst = line.scan(/\d+/).map(&:to_i)
  (inst[0]..inst[2]).to_a.product((inst[1]..inst[3]).to_a).each do |(x, y)|
    old_val = light_state.fetch(x * 1000 + y, 0)
    if cmd == 'toggle'
      light_state[x * 1000 + y] = old_val + 2
    elsif line.split[1] == 'on'
      light_state[x * 1000 + y] = old_val + 1
    else
      light_state[x * 1000 + y] = [0, old_val - 1].max
    end
  end
end
puts light_state.each_value.sum
