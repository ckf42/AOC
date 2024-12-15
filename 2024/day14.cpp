#include <bitset>
#include <string>
#include <vector>

#include "../util.hpp"

constexpr int w = 101, h = 103;
constexpr int N = w * h;

int countConnected(const std::bitset<N> &grid){
    std::bitset<N> visited;
    int count = 0, coor = 0;
    for (int i = 0; i < w; ++i){
        for (int j = 0; j < h; ++j){
            ++coor;
            if (!grid[coor] || visited[coor]){
                continue;
            }
            ++count;
            std::vector<int> st;
            st.push_back(coor);
            while (!st.empty()){
                int idx = st.back();
                st.pop_back();
                if (visited[idx]){
                    continue;
                }
                visited[idx] = true;
                int x = idx / h, y = idx % h;
                for (const auto &pr : util::neighbourGridPoint(x, y, w, h)){
                    int idxx = pr.first * h + pr.second;
                    if (grid[idxx]){
                        st.push_back(idxx);
                    }
                }
            }
        }
    }
    return count;
}

int main(int, char**){
    std::vector<std::vector<int>> robots;
    for (const auto &line : util::splitline(util::getInput(2024, 14))){
        robots.push_back(util::extract_int(line));
        if (robots.back()[2] < 0){
            robots.back()[2] += w;
        }
        if (robots.back()[3] < 0){
            robots.back()[3] += h;
        }
    }

    // part 1
    int t = 100, quadCount[4] = {0};
    for (auto &bot : robots){
        int x = (bot[0] + bot[2] * t) % w,
            y = (bot[1] + bot[3] * t) % h;
        if (x == w / 2 || y == h / 2){
            continue;
        }
        ++quadCount[(x < w / 2) + 2 * (y < h / 2)];
    }
    unsigned long long int res = 1;
    for (int i = 0; i < 4; ++i){
        res *= quadCount[i];
    }
    util::output(res);

    // part 2
    int n = robots.size();
    std::vector<int> locs(n);
    for (int i = 0; i < n; ++i){
        locs[i] = robots[i][0] * h + robots[i][1];
    }
    std::bitset<N> grid;
    for (int t = 1; t <= w * h; ++t){
        grid.reset();
        for (int i = 0; i < n; ++i){
            int x = locs[i] / h, y = locs[i] % h;
            x = (x + robots[i][2]) % w;
            y = (y + robots[i][3]) % h;
            locs[i] = x * h + y;
            grid[locs[i]] = true;
        }
        if (countConnected(grid) < n / 3){
            util::output(t);
            break;
        }
    }

    return 0;
}
