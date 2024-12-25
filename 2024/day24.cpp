#include <string>
#include <unordered_map>
#include <vector>

#include "../util.hpp"

using ulli = unsigned long long int;

bool evalReg(
        const std::string &reg,
        std::unordered_map<std::string, bool> &regCache,
        const std::unordered_map<std::string, std::vector<std::string>> &gates
        ){
    if (!util::contains(reg, regCache)){
        std::vector<std::string> plan = gates.at(reg);
        if (plan[0] == "OR"){
            regCache[reg] = (evalReg(plan[1], regCache, gates) | evalReg(plan[2], regCache, gates));
        } else if (plan[0] == "AND"){
            regCache[reg] = (evalReg(plan[1], regCache, gates) & evalReg(plan[2], regCache, gates));
        } else {
            regCache[reg] = (evalReg(plan[1], regCache, gates) ^ evalReg(plan[2], regCache, gates));
        }
    }
    return regCache[reg];
}

int main(int, char**){
    std::vector<std::string> inp = util::split(util::getInput(2024, 24), "\n\n");
    std::unordered_map<std::string, std::vector<std::string>> gates;
    for (const std::string &line : util::splitline(inp[1])){
        std::vector<std::string> parts = util::split(line, " ");
        gates[parts[4]] = {parts[1], parts[0], parts[2]};
    }
    std::unordered_map<std::string, bool> regVals; 
    for (const std::string &line : util::splitline(inp[0])){
        int idx = line.find(": ");
        regVals[line.substr(0, idx)] = line[idx + 2] == '1';
    }

    // part 1
    ulli z = 0;
    int i = 0;
    for (; i < 100; ++i){
        std::string regName = "z";
        regName += (i < 10 ? "0" : "") + std::to_string(i);
        if (!util::contains(regName, gates)){
            break;
        }
        z <<= 1;
        z |= evalReg(regName, regVals, gates);
    }
    ulli zz = 0;
    while (i-- > 0){
        zz <<= 1;
        zz |= (z & 1);
        z >>= 1;
    }
    util::output(zz);


    // part 2
    // ?????

    return 0;
}
