#include <string>
#include <unordered_map>

#include "../util.hpp"

using ulli = unsigned long long int;
using CacheType = std::unordered_map<ulli, std::unordered_map<short, ulli>>;

ulli getGenLen(ulli x, short count, CacheType &cache){
    if (count == 0){
        return 1;
    }
    if (!util::contains(count, cache[x])){
        ulli res;
        if (x == 0){
            res = getGenLen(1, count - 1, cache);
        } else {
            std::string s = std::to_string(x);
            if (s.size() & 1){
                res = getGenLen(x * 2024, count - 1, cache);
            } else {
                res = getGenLen(std::stoull(s.substr(0, s.size() / 2)), count - 1, cache) 
                    + getGenLen(std::stoull(s.substr(s.size() / 2)), count - 1, cache);
            }
        }
        cache[x][count] = res;
    }
    return cache[x][count];
}

int main(int, char**){
    std::vector<int> nums = util::getInts(util::getInput(2024, 11));
    CacheType cache;

    // part 1
    ulli res = 0;
    for (int x : nums){
        res += getGenLen(x, 25, cache);
    }
    util::output(res);

    // part 2
    res = 0;
    for (int x : nums){
        res += getGenLen(x, 75, cache);
    }
    util::output(res);

    return 0;
}
