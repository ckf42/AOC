inp = File.read('input1').chars.map { |x| { '(' => 1, ')' => -1 }[x] }

# part 1
puts inp.sum

# part 2
(1...inp.size).to_a.each_with_index { |e, i| inp[e] += inp[i] }
puts (0...inp.size).find { |i| inp[i] == -1 } + 1
