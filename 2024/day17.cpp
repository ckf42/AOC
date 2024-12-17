#include <algorithm>
#include <string>
#include <utility>
#include <vector>

#include "../util.hpp"

using ulli = unsigned long long int;

inline int getCombo(int oper, int a, int b, int c){
    if (oper <= 3){
        return oper;
    }
    switch (oper){
        case 4:
            return a;
        case 5:
            return b;
        case 6:
            return c;
        default:
            return 0;
    }
}

std::string runProg(int a, int b, int c, const std::vector<int> &prog){
    int n = prog.size();
    std::vector<int> output;
    int ptr = 0;
    while (ptr < n){
        int inst = prog[ptr], oper = prog[ptr + 1];
        switch (inst){
            case 0:
                a >>= getCombo(oper, a, b, c);
                break;
            case 1:
                b ^= oper;
                break;
            case 2:
                b = (getCombo(oper, a, b, c) & 7);
                break;
            case 3:
                if (a != 0){
                    ptr = oper - 2;
                }
                break;
            case 4:
                b ^= c;
                break;
            case 5:
                output.push_back(getCombo(oper, a, b, c) & 7);
                break;
            case 6:
                b = (a >> getCombo(oper, a, b, c));
                break;
            case 7:
                c = (a >> getCombo(oper, a, b, c));
                break;
        }
        ptr += 2;
    }
    return util::joinStr(output, ",");
}

int main(int, char**){
    std::vector<std::string> inp = util::split(util::getInput(2024, 17), "\n\n");
    std::vector<int> initReg = util::extract_int(inp[0]), prog = util::extract_int(inp[1]);

    // part 1
    util::output(runProg(initReg[0], initReg[1], initReg[2], prog));

    // part 2
    std::vector<ulli> aList(1, 0), newAList;
    int n = prog.size();
    for (int i = n - 1; i >= 0; --i){
        newAList.clear();
        for (ulli aPref : aList){
            for (int r = 0; r < 8; ++r){
                ulli a = ((aPref << 3) | r);
                ulli c = (a >> (r ^ 7));
                if (((r ^ c) & 7) == prog[i]){
                    newAList.push_back(a);
                }
            }
        }
        std::swap(newAList, aList);
    }
    util::output(*std::min_element(aList.cbegin(), aList.cend()));

    return 0;
}
