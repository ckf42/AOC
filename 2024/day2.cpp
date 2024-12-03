#include <iostream>
#include <string>
#include <vector>

#include "../util.h"

using ulli = unsigned long long int;

bool isSafeRow(const std::vector<int> &row){
    int n = row.size();
    bool incFail = false, decFail = false;
    for (int i = 1; i < n; ++i){
        int delta = row[i] - row[i - 1];
        if (!(1 <= delta && delta <= 3)){
            incFail = true;
        }
        if (!(-3 <= delta && delta <= -1)){
            decFail = true;
        }
        if (incFail && decFail){
            return false;
        }
    }
    return true;
}

int main(int, char**){
    std::string inp = util::getInput(2024, 2);
    std::vector<std::vector<int>> nums;
    for (auto &s : util::splitline(inp)){
        nums.push_back(util::getInts(s));
    }

    // part 1
    int n = nums.size();
    std::vector<bool> passState(n, false);
    int res = 0;
    for (int i = 0; i < n; ++i){
        res += passState[i] = isSafeRow(nums[i]);
    }
    std::cout << res << std::endl;


    // part 2
    res = 0;
    for (int i = 0; i < n; ++i){
        if (!passState[i]){
            std::vector<int> buff(nums[i].size() - 1);
            for (int j = 0; j < nums[i].size(); ++j){
                int wptr = 0;
                for (int k = 0; k < nums[i].size(); ++k){
                    if (k == j){
                        continue;
                    }
                    buff[wptr++] = nums[i][k];
                }
                if (isSafeRow(buff)){
                    passState[i] = true;
                    break;
                }
            }
        }
        res += passState[i];
    }
    std::cout << res << std::endl;

    return 0;
}
