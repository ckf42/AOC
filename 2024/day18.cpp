#include <string>
#include <unordered_set>
#include <utility>
#include <vector>
#include <queue>

#include "../util.hpp"

constexpr int blkSize = 70 + 1;
constexpr int count = 1024;

using DijkState = std::pair<int, std::pair<int, int>>;

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
    std::priority_queue<DijkState, std::vector<DijkState>, std::greater<DijkState>> pq;
    std::unordered_set<int> corrupted(allCorrupted.cbegin(), allCorrupted.cbegin() + count), visited;
    pq.push({0, {0, 0}});
    while (!pq.empty()){
        auto [cost, pt] = pq.top();
        pq.pop();
        if (pt.first == blkSize - 1 && pt.second == blkSize - 1){
            util::output(cost);
            break;
        }
        if (util::contains(pt.first * blkSize + pt.second, visited)){
            continue;
        }
        visited.insert(pt.first * blkSize + pt.second);
        for (const auto &nb : util::neighbourGridPoint(pt.first, pt.second, blkSize, blkSize)){
            if (util::contains(nb.first * blkSize + nb.second, corrupted)){
                continue;
            }
            pq.push({cost + 1, nb});
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
