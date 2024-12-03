#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

#include "../util.h"

using ulli = unsigned long long int;

int main(int, char**){
    std::string inp = util::getInput(2024, 1);
    std::vector<int> nums[2];
    for (std::string &s : util::splitline(inp)){
        auto buff = util::getInts(s);
        nums[0].push_back(buff[0]);
        nums[1].push_back(buff[1]);
    }
    std::sort(nums[0].begin(), nums[0].end());
    std::sort(nums[1].begin(), nums[1].end());
    int n = nums[0].size();
    
    // part 1
    ulli res = 0;
    for (int i = 0; i < n; ++i){
        res += std::abs(nums[0][i] - nums[1][i]);
    }
    std::cout << res << std::endl;

    // part 2
    res = 0;
    std::unordered_map<int, int> c;
    for (auto x: nums[1]){
        ++c[x];
    }
    for (auto x: nums[0]){
        res += x * c[x];
    }
    std::cout << res << std::endl;

    return 0;
}