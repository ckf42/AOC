#include <bitset>
#include <string>
#include <utility>
#include <vector>

#include "../util.hpp"

using ulli = unsigned long long int;

int main(int, char**){
    std::vector<std::string> garden = util::splitline(util::getInput(2024, 12));
    int n = garden.size(), m = garden[0].size();

    // part 1
    ulli res = 0;
    std::vector<bool> visited(n * m, false);
    std::vector<std::pair<int, int>> buff;
    for (int i = 0; i < n; ++i){
        for (int j = 0; j < m; ++j){
            if (visited[i * m + j]){
                continue;
            }
            buff.push_back({i, j});
            ulli area = 0, peri = 0;
            char tag = garden[i][j];
            while (!buff.empty()){
                auto [x, y] = buff.back();
                buff.pop_back();
                if (visited[x * m + y]){
                    continue;
                }
                visited[x * m + y] = true;
                ++area;
                peri += 4;
                for (const auto &pt : util::neighbourGridPoint(x, y, n, m)){
                    if (garden[pt.first][pt.second] == tag){
                        --peri;
                        if (!visited[pt.first * m + pt.second]){
                            buff.push_back(pt);
                        }
                    }
                }
            }
            res += area * peri;
        }
    }
    util::output(res);

    
    // part 2
    res = 0;
    visited.flip();
    buff.clear();
    for (int i = 0; i < n; ++i){
        for (int j = 0; j < m; ++j){
            if (visited[i * m + j]){
                continue;
            }
            buff.push_back({i, j});
            ulli area = 0, cornerCount = 0;
            char tag = garden[i][j];
            while (!buff.empty()){
                auto [x, y] = buff.back();
                buff.pop_back();
                if (visited[x * m + y]){
                    continue;
                }
                visited[x * m + y] = true;
                ++area;
                short nbBits = 0, mask = 1;
                for (int k = 0; k < 8; ++k){
                    int xx = x + util::EIGHT_DIRECTIONS[k][0],
                        yy = y + util::EIGHT_DIRECTIONS[k][1];
                    if (util::in2DRange(xx, yy, n, m) && garden[xx][yy] == tag){
                        nbBits |= mask;
                        if (!(k & 1)){
                            buff.push_back({xx, yy});
                        }
                    }
                    mask <<= 1;
                }
                for (int k = 0; k < 4; ++k){
                    switch (nbBits & 7){
                        case 0:
                        case 2:
                        case 5:
                            ++cornerCount;
                            break;
                    }
                    short lower = nbBits & 3;
                    nbBits >>= 2;
                    nbBits |= lower << 6;
                }
            }
            res += area * cornerCount;
        }
    }
    util::output(res);

    return 0;
}
