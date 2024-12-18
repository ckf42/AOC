#include <queue>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

#include "../util.hpp"

using pr = std::pair<int, int>;

constexpr int DIRS[4][2] = {
    {0, 1},
    {1, 0},
    {0, -1},
    {-1, 0}
};

int main(int, char**){
    std::string inp = util::getInput(2024, 16);
    std::vector<std::string> graph = util::splitline(inp);
    int n = graph.size(), m = graph[0].size();
    int sidx = inp.find('S'), eidx = inp.find('E');
    sidx = (sidx / (m + 1)) * m + (sidx % (m + 1));
    eidx = (eidx / (m + 1)) * m + (eidx % (m + 1));

    // part 1
    int minCost = -1;
    std::priority_queue<pr, std::vector<pr>, std::greater<pr>> pq;
    pq.push({0, sidx * 4 * 4});
    std::unordered_map<int, int> visited, prevActions;
    std::vector<int> buff;
    while (!pq.empty()){
        auto [cost, x] = pq.top();
        pq.pop();
        int lastAct = x % 4;
        x /= 4;
        int currState = x, d = x % 4;
        x /= 4;
        int y = x % m;
        x /= m;
        if (util::getWithDefault(currState, visited, cost) == cost){
            prevActions[currState] |= (1 << lastAct);
        }
        if (currState / 4 == eidx){
            if (minCost == -1){
                util::output(cost);
                minCost = cost;
            }
            buff.push_back(currState);
            continue;
        }
        if (util::contains(currState, visited)){
            continue;
        }
        if (minCost != -1 && cost > minCost){
            break;
        }
        visited[currState] = cost;
        int newState = (x * m + y) * 4 + (d + 1) % 4;
        if (util::getWithDefault(newState, visited, cost + 1000) == cost + 1000){
            pq.push({cost + 1000, newState * 4 + 1});
        }
        newState = (x * m + y) * 4 + (d + 3) % 4;
        if (util::getWithDefault(newState, visited, cost + 1000) == cost + 1000){
            pq.push({cost + 1000, newState * 4 + 2});
        }
        x += DIRS[d][0];
        y += DIRS[d][1];
        newState = (x * m + y) * 4 + d;
        if (graph[x][y] != '#' && util::getWithDefault(newState, visited, cost + 1) == cost + 1){
            pq.push({cost + 1, newState * 4 + 3});
        }
    }

    // part 2
    std::vector<bool> tiles(n * m, false), added(n * m * 4, false);
    while (!buff.empty()){
        int state = buff.back();
        buff.pop_back();
        tiles[state / 4] = true;
        if (state != sidx * 4 && !added[state]){
            added[state] = true;
            int d = state % 4, coor = state / 4;
            int y = coor % m, x = coor / m;
            for (int i = 1; i <= 3; ++i){
                if ((prevActions[state] & (1 << i)) == 0){
                    continue;
                }
                switch (i){
                    case 1:
                        buff.push_back((x * m + y) * 4 + (d + 3) % 4);
                        break;
                    case 2:
                        buff.push_back((x * m + y) * 4 + (d + 1) % 4);
                        break;
                    case 3:
                        buff.push_back(((x - DIRS[d][0]) * m + y - DIRS[d][1]) * 4 + d);
                        break;
                }
            }
        }
    }
    util::output(util::sum<int>(tiles));

    return 0;
}
