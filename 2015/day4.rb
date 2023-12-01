require 'digest'

inp = File.read('input4').chomp

# part 1
p1 = (1..).find { |n| Digest::MD5.hexdigest(inp + n.to_s).match(/^0{5,}/) }
puts p1

# part 2
puts((p1..).find { |n| Digest::MD5.hexdigest(inp + n.to_s).match(/^0{6,}/) })
