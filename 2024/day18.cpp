#include <string>
#include <tuple>
#include <unordered_set>
#include <utility>
#include <vector>
#include <queue>

#include "../util.hpp"

constexpr int blkSize = 70 + 1;
constexpr int count = 1024;

using NodeState = std::tuple<int, int, int>;

bool isDisconnected(const std::unordered_set<int> &blocked){
    std::vector<int> buff(1, 0);
    std::unordered_set<int> visited;
    while (!buff.empty()){
        int idx = buff.back();
        buff.pop_back();
        if (util::contains(idx, visited)){
            continue;
        }
        visited.insert(idx);
        if (idx == blkSize * blkSize - 1){
            break;
        }
        for (const auto &nb : util::neighbourGridPoint(idx / blkSize, idx % blkSize, blkSize, blkSize)){
            int nbidx = nb.first * blkSize + nb.second;
            if (!util::contains(nbidx, blocked)){
                buff.push_back(nbidx);
            }
        }
    }
    return !util::contains(blkSize * blkSize - 1, visited);
}

int main(int, char**){
    std::vector<int> allCorrupted;
    for (auto &line : util::splitline(util::getInput(2024, 18))){
        auto v = util::extract_int(line);
        allCorrupted.push_back(v[0] * blkSize + v[1]);
    }

    // part 1
    std::queue<NodeState> q;
    std::unordered_set<int> corrupted(allCorrupted.cbegin(), allCorrupted.cbegin() + count), visited;
    q.push({0, 0, 0});
    while (!q.empty()){
        auto [cost, x, y] = q.front();
        q.pop();
        if (x == blkSize - 1 && y == blkSize - 1){
            util::output(cost);
            break;
        }
        if (util::contains(x * blkSize + y, visited)){
            continue;
        }
        visited.insert(x * blkSize + y);
        for (const auto &nb : util::neighbourGridPoint(x, y, blkSize, blkSize)){
            if (util::contains(nb.first * blkSize + nb.second, corrupted)){
                continue;
            }
            q.push({cost + 1, nb.first, nb.second});
        }
    }

    // part 2
    int s = 0, e = allCorrupted.size();
    while (s < e){
        int m = (s + e) / 2;
        if (isDisconnected(std::unordered_set<int>(allCorrupted.cbegin(), allCorrupted.cbegin() + m + 1))){
            e = m;
        } else {
            s = m + 1;
        }
    }
    util::printVec({allCorrupted[s] / blkSize, allCorrupted[s] % blkSize}, ",");

    return 0;
}
