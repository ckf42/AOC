#include <iostream>
#include <string>

#include <re2/re2.h>
#include <re2/stringpiece.h>
#include "../util.h"

using ulli = unsigned long long int;

int main(int, char**){
    std::string inp = util::getInput(2024, 3);

    // part 1
    RE2 mulPatt("mul\\((\\d+),(\\d+)\\)");
    int m1, m2;
    ulli res = 0;
    {
        re2::StringPiece inp_view(inp);
        while (RE2::FindAndConsume(&inp_view, mulPatt, &m1, &m2)){
            res += m1 * m2;
        }
    }
    std::cout << res << std::endl;
    
    // part 2
    res = 0;
    size_t ptr = 0, loc;
    while (ptr != std::string::npos){
        loc = inp.find("don't()", ptr);
        if (loc == std::string::npos){
            loc = inp.size();
        }
        {
            re2::StringPiece substr_view = re2::StringPiece(inp).substr(ptr, loc - ptr);
            while (RE2::FindAndConsume(&substr_view, mulPatt, &m1, &m2)){
                res += m1 * m2;
            }
        }
        ptr = inp.find("do()", loc);
    }
    std::cout << res << std::endl;

    return 0;
}
