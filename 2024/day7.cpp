#include <iostream>
#include <sstream>
#include <string>
#include <unordered_set>
#include <vector>

#include "../util.h"

using lli = long long int;


int main(int, char**){
    std::stringstream inpStream;
    util::getInput(2024, 7, inpStream);
    std::vector<std::string> lines(util::splitline(inpStream));
    std::vector<std::vector<lli>> nums;
    for (auto &line : lines){
        std::vector<lli> numBuff;
        int idx = line.find(':');
        numBuff.push_back(std::stoll(line.substr(0, idx)));
        for (int x : util::getInts(line.substr(idx + 1))){
            numBuff.push_back(x);
        }
        nums.push_back(numBuff);
    }

    // part 1
    int n = nums.size();
    lli res = 0;
    std::vector<bool> evalState(n, false);
    for (int i = 0; i < n; ++i){
        std::unordered_set<lli> buff, newBuff;
        buff.insert(nums[i][1]);
        for (int j = 2; j < nums[i].size(); ++j){
            newBuff.clear();
            for (lli x : buff){
                for (lli y : {x + nums[i][j], x * nums[i][j]}){
                    if (y <= nums[i][0]){
                        newBuff.insert(y);
                    }
                }
            }
            std::swap(buff, newBuff);
        }
        if (util::contains(nums[i][0], buff)){
            evalState[i] = true;
            res += nums[i][0];
        }
    }
    std::cout << res << std::endl;

    // part 2
    // TODO: same speed as python. need to speed up
    for (int i = 0; i < n; ++i){
        if (evalState[i]){
            continue;
        }
        std::unordered_set<lli> buff, newBuff;
        buff.insert(nums[i][1]);
        for (int j = 2; j < nums[i].size(); ++j){
            newBuff.clear();
            for (lli x : buff){
                for (lli y : {
                            x + nums[i][j],
                            x * nums[i][j],
                            std::stoll(std::to_string(x) + std::to_string(nums[i][j]))
                        }){
                    if (y <= nums[i][0]){
                        newBuff.insert(y);
                    }
                }
            }
            std::swap(buff, newBuff);
        }
        if (util::contains(nums[i][0], buff)){
            res += nums[i][0];
        }
    }
    std::cout << res << std::endl;

    return 0;
}
