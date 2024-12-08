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
        util::extendVec(numBuff, util::getInts(line.substr(idx + 1)));
        nums.push_back(numBuff);
    }

    // part 1
    int n = nums.size();
    lli res = 0;
    std::vector<bool> evalState(n, false);
    for (int i = 0; i < n; ++i){
        std::unordered_set<lli> buff, newBuff;
        buff.insert(nums[i][0]);
        for (int j = nums[i].size() - 1; j >= 2; --j){
            newBuff.clear();
            for (lli x : buff){
                if (x >= nums[i][j]){
                    newBuff.insert(x - nums[i][j]);
                }
                if (x % nums[i][j] == 0){
                    newBuff.insert(x / nums[i][j]);
                }
            }
            std::swap(buff, newBuff);
        }
        if (util::contains(nums[i][1], buff)){
            evalState[i] = true;
            res += nums[i][0];
        }
    }
    util::output(res);

    // part 2
    // TODO: same speed as python. need to speed up
    for (int i = 0; i < n; ++i){
        if (evalState[i]){
            continue;
        }
        std::unordered_set<lli> buff, newBuff;
        buff.insert(nums[i][0]);
        for (int j = nums[i].size() - 1; j >= 2; --j){
            newBuff.clear();
            for (lli x : buff){
                if (x >= nums[i][j]){
                    newBuff.insert(x - nums[i][j]);
                }
                if (x % nums[i][j] == 0){
                    newBuff.insert(x / nums[i][j]);
                }
                std::string
                    strx = std::to_string(x),
                    stry = std::to_string(nums[i][j]);
                if (strx.size() > stry.size() && stry == strx.substr(strx.size() - stry.size())){
                    newBuff.insert(std::stoll(strx.substr(0, strx.size() - stry.size())));
                }
            }
            std::swap(buff, newBuff);
        }
        if (util::contains(nums[i][1], buff)){
            res += nums[i][0];
        }
    }
    util::output(res);

    return 0;
}
