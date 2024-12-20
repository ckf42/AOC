#include <string>
#include <queue>
#include <unordered_map>
#include <utility>

#include "../util.hpp"

int main(int, char**){
    std::string inp = util::getInput(2024, 20);
    std::vector<std::string> grid = util::splitline(inp);
    int n = grid.size(), m = grid[0].size();
    int sIdx = inp.find('S'), eIdx = inp.find('E');
    int sCoor = (sIdx / (m + 1) * m) + (sIdx % (m + 1)),
        eCoor = (eIdx / (m + 1) * m) + (eIdx % (m + 1));
    std::unordered_map<int, int> costFromStart, costFromEnd;
    std::queue<std::pair<int, int>> q;
    int normalCost = -1;
    q.push({0, sCoor});
    while (!q.empty()){
        auto [cost, pt] = q.front();
        q.pop();
        if (util::contains(pt, costFromStart)){
            continue;
        }
        costFromStart[pt] = cost;
        if (pt == eCoor){
            if (normalCost == -1){
                normalCost = cost;
            }
            continue;
        }
        for (const auto &nb : util::neighbourGridPoint(pt / m, pt % m, n, m)){
            if (grid[nb.first][nb.second] != '#'){
                q.push({cost + 1, nb.first * m + nb.second});
            }
        }
    }
    q.push({0, eCoor});
    while (!q.empty()){
        auto [cost, pt] = q.front();
        q.pop();
        if (util::contains(pt, costFromEnd)){
            continue;
        }
        costFromEnd[pt] = cost;
        if (pt == sCoor){
            continue;
        }
        for (const auto &nb : util::neighbourGridPoint(pt / m, pt % m, n, m)){
            if (grid[nb.first][nb.second] != '#'){
                q.push({cost + 1, nb.first * m + nb.second});
            }
        }
    }

    // part 1
    int count = 0;
    int cheatTime = 2;
    for (auto [pt1, cost1] : costFromStart){
        for (int dx = -cheatTime; dx <= cheatTime; ++dx){
            for (int dy = -(cheatTime - std::abs(dx)); dy <= cheatTime - std::abs(dx); ++dy){
                int pt2 = pt1 + dx * m + dy;
                if (!util::in2DRange(pt1 / m + dx, pt1 % m + dy, n, m) || !util::contains(pt2, costFromEnd)){
                    continue;
                }
                int newCost = cost1 + costFromEnd[pt2] + std::abs(dx) + std::abs(dy);
                if (normalCost - newCost >= 100){
                    ++count;
                }
            }
        }
    }
    util::output(count);

    // part 2
    count = 0;
    cheatTime = 20;
    for (auto [pt1, cost1] : costFromStart){
        for (int dx = -cheatTime; dx <= cheatTime; ++dx){
            for (int dy = -(cheatTime - std::abs(dx)); dy <= cheatTime - std::abs(dx); ++dy){
                int pt2 = pt1 + dx * m + dy;
                if (!util::in2DRange(pt1 / m + dx, pt1 % m + dy, n, m) || !util::contains(pt2, costFromEnd)){
                    continue;
                }
                int newCost = cost1 + costFromEnd[pt2] + std::abs(dx) + std::abs(dy);
                if (normalCost - newCost >= 100){
                    ++count;
                }
            }
        }
    }
    util::output(count);





    return 0;
}
