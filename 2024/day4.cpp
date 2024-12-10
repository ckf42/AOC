#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "../util.hpp"

constexpr char pattPart1[] = "XMAS";
constexpr int dirs[8][3][2] = {    
    {{0, 1}, {0, 2}, {0, 3}},
    {{1, 0}, {2, 0}, {3, 0}},
    {{0, -1}, {0, -2}, {0, -3}},
    {{-1, 0}, {-2, 0}, {-3, 0}},
    {{1, 1}, {2, 2}, {3, 3}},
    {{1, -1}, {2, -2}, {3, -3}},
    {{-1, -1}, {-2, -2}, {-3, -3}},
    {{-1, 1}, {-2, 2}, {-3, 3}}
};
constexpr char pattPart2[] = "MMSS";
constexpr int offsets[4][2] = {
    {-1, -1}, {-1, 1}, {1, 1}, {1, -1}
};

int main(int, char**){
    std::stringstream inpStream;
    util::getInput(2024, 4, inpStream);
    std::vector<std::string> lines = util::splitline(inpStream);
    int n = lines.size(), m = lines[0].size();

    // part 1
    int count = 0;
    for (int i = 0; i < n; ++i){
        for (int j = 0; j < m; ++j){
            if (lines[i][j] != 'X'){
                continue;
            }
            for (int d = 0; d < 8; ++d){
                ++count;
                for (int k = 0; k < 3; ++k){
                    int ii = i + dirs[d][k][0], jj = j + dirs[d][k][1];
                    if (!(ii >= 0 && ii < n 
                            && jj >= 0 && jj < m
                            && lines[ii][jj] == pattPart1[k + 1])){
                        --count;
                        break;
                    }
                }
            }
        }
    }
    std::cout << count << std::endl;

    // part 2
    count = 0;
    for (int i = 1; i < n - 1; ++i){
        for (int j = 1; j < m - 1; ++j){
            if (lines[i][j] != 'A'){
                continue;
            }
            for (int d = 0; d < 4; ++d){
                ++count;
                for (int k = 0; k < 4; ++k){
                    int ii = i + offsets[(d + k) & 3][0], jj = j + offsets[(d + k) & 3][1];
                    if (lines[ii][jj] != pattPart2[k]){
                        --count;
                        break;
                    }
                }
            }
        }
    }
    std::cout << count << std::endl;

    return 0;
}
