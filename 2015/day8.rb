inp = File.read('input8').split "\n"

# part 1
puts (inp.map do |line|
  line.scan(/\\"|\\\\/).size + 3 * line.scan(/\\x[0-9a-fA-F]{2}/).size + 2
end).sum

# part 2
puts (inp.map { |line| line.scan(/\\|"/).size + 2 }).sum
