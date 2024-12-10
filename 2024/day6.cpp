#include <iostream>
#include <sstream>
#include <string>
#include <unordered_set>
#include <vector>

#include "../util.hpp"

using lli = long long int;

constexpr int dirs[4][2] = {
    {-1, 0}, {0, 1}, {1, 0}, {0, -1}
};

bool hasLoop(int x, int y, int n, int m, std::unordered_set<lli> &obs){
    int d = 0;
    std::unordered_set<lli> visited;
    while (util::inRange(x, 0, n) && util::inRange(y, 0, m)){
        int z = (x * m + y) * 4 + d;
        if (util::contains(z, visited)){
            return true;
        }
        visited.insert(z);
        int xx = x + dirs[d][0], yy = y + dirs[d][1];
        if (util::contains(xx * m + yy, obs)){
            d = (d + 1) % 4;
        } else {
            x = xx;
            y = yy;
        }
    }
    return false;
}

int main(int, char**){
    std::stringstream inpStream;
    util::getInput(2024, 6, inpStream);
    std::vector<std::string> labMap(util::splitline(inpStream));
    int n = labMap.size(), m = labMap[0].size();
    int x0, y0;
    std::unordered_set<lli> obs;
    for (int i = 0; i < n; ++i){
        for (int j = 0; j < m; ++j){
            if (labMap[i][j] == '^'){
                x0 = i;
                y0 = j;
            } else if (labMap[i][j] == '#'){
                obs.insert(i * m + j);
            }
        }
    }

    // part 1
    int x = x0, y = y0, d = 0;
    std::unordered_set<lli> visited;
    while (util::inRange(x, 0, n) && util::inRange(y, 0, m)){
        visited.insert(x * m + y);
        int xx = x + dirs[d][0], yy = y + dirs[d][1];
        if (util::contains(xx * m + yy, obs)){
            d = (d + 1) % 4;
        } else {
            x = xx;
            y = yy;
        }
    }
    std::cout << visited.size() << std::endl;

    // part 2
    int count = 0;
    for (lli pt : visited){
        int xx = pt / m, yy = pt % m;
        if (xx == x0 && yy == y0){
            continue;
        }
        obs.insert(xx * m + yy);
        count += hasLoop(x0, y0, n, m, obs);
        obs.erase(xx * m + yy);
    }
    std::cout << count << std::endl;

    return 0;
}
