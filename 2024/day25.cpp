#include <vector>

#include "../util.hpp"

int main(int, char**){
    std::vector<std::vector<int>> locks, keys;
    for (const std::string &line : util::split(util::getInput(2024, 25), "\n\n")){
        std::vector<std::string> pins = util::splitline(line);
        int pinMaxLen = pins.size(), pinCount = pins[0].size();
        std::vector<int> counts;
        for (int j = 0; j < pinCount; ++j){
            int count = -1;
            for (int i = 0; i < pinMaxLen; ++i){
                count += pins[i][j] == '#';
            }
            counts.push_back(count);
        }
        if (pins[0][0] == '#'){
            locks.push_back(counts);
        } else {
            keys.push_back(counts);
        }
    }

    // part 1
    int count = 0;
    for (auto k : keys){
        for (auto l : locks){
            int n = k.size();
            bool fits = true;
            for (int i = 0; i < n; ++i){
                if (k[i] + l[i] > 5){
                    fits = false;
                    break;
                }
            }
            count += fits;
        }
    }
    util::output(count);


    // part 2
    // no part 2

    return 0;
}
