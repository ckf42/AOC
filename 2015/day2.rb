inp = File.read('input2').split.map { |line| line.scan(/\d+/).map(&:to_i) }

# part 1
puts inp.map { |arr| arr.sum**2 - arr.map { |x| x**2 }.sum + arr.inject(:*) / arr.max }.sum

# part 2
puts inp.map { |arr| 2 * (arr.sum - arr.max) + arr.inject(:*) }.sum
