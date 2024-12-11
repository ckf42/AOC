#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include "../util.hpp"

int main(int, char**){
    std::vector<std::string> hikemap = util::splitline(util::getInput(2024, 10));
    int n = hikemap.size(), m = hikemap[0].size();

    // part 1
    std::unordered_map<int, std::unordered_set<int>> buff;
    for (int i = 0; i < n; ++i){
        for (int j = 0; j < m; ++j){
            if (hikemap[i][j] == '9'){
                buff[i * m + j].insert(i * m + j);
            }
        }
    }
    std::unordered_map<int, std::unordered_set<int>> newBuff;
    for (int k = 0; k < 9; ++k){
        newBuff.clear();
        for (auto &pr : buff){
            int i = pr.first / m, j = pr.first % m;
            for (const auto &nb : util::neighbourGridPoint(i, j, n, m)){
                if (hikemap[nb.first][nb.second] == hikemap[i][j] - 1){
                    newBuff[nb.first * m + nb.second].insert(pr.second.cbegin(), pr.second.cend());
                }
            }
        }
        std::swap(buff, newBuff);
    }
    int res = 0;
    for (auto &pr : buff){
        res += pr.second.size();
    }
    util::output(res);

    // part 2
    std::unordered_map<int, int> buffPart2;
    for (int i = 0; i < n; ++i){
        for (int j = 0; j < m; ++j){
            if (hikemap[i][j] == '9'){
                buffPart2[i * m + j] = 1;
            }
        }
    }
    std::unordered_map<int, int> newBuffPart2;
    for (int k = 0; k < 9; ++k){
        newBuffPart2.clear();
        for (const auto &pr : buffPart2){
            int i = pr.first / m, j = pr.first % m;
            for (const auto &nb : util::neighbourGridPoint(i, j, n, m)){
                if (hikemap[nb.first][nb.second] == hikemap[i][j] - 1){
                    newBuffPart2[nb.first * m + nb.second] += pr.second;
                }
            }
        }
        std::swap(buffPart2, newBuffPart2);
    }
    res = 0;
    for (const auto &pr : buffPart2){
        res += pr.second;
    }
    util::output(res);
    return 0;
}
