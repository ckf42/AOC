inp = File.read('input5')
patterns = [/[aeiou].*[aeiou].*[aeiou]/, /(.)\1/] + (
  %w[ab cd pq xy].map { |p| Regexp.new("^((?!#{p}).)*$") }
)

# part 1
puts(inp.split.map { |line| patterns.map { |p| p.match? line }.all? ? 1 : 0 }.sum)

# part 2
puts(inp.split.map { |line| [/(..).*\1/, /(.).\1/].map { |p| p.match? line }.all? ? 1 : 0 }.sum)
