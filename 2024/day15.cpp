#include <string>
#include <utility>
#include <queue>

#include "../util.hpp"

inline std::pair<int, int> getDirs(char c){
    switch (c){
        case '>':
            return {0, 1};
        case '<':
            return {0, -1};
        case 'v':
            return {1, 0};
        case '^':
            return {-1, 0};
    }
    return {0, 0};
}

inline std::string part2Extend(char c){
    switch (c){
        case '#':
            return "##";
        case 'O':
            return "[]";
        case '.':
            return "..";
        case '@':
            return "@.";
    }
    return "";
}

int main(int, char**){
    std::vector<std::string> inp = util::split(util::getInput(2024, 15), "\n\n");
    std::vector<std::string> warehouse = util::splitline(inp[0]);
    std::string inst;
    for (const std::string &line : util::splitline(inp[1])){
        inst += line;
    }
    int idx = inp[0].find('@'), n = warehouse.size(), m = warehouse[0].size();
    int x = idx / (m + 1), y = idx % (m + 1);

    // part 1
    for (char c : inst){
        auto [dx, dy] = getDirs(c);
        int xx = x, yy = y;
        std::vector<int> moveSt;
        while (true){
            char obs = warehouse[xx][yy];
            if (obs == '#'){
                moveSt.clear();
                break;
            }
            if (obs == '.'){
                break;
            }
            moveSt.push_back(xx * m + yy);
            xx += dx;
            yy += dy;
        }
        while (!moveSt.empty()){
            int idx = moveSt.back();
            moveSt.pop_back();
            int ptx = idx / m, pty = idx % m;
            std::swap(warehouse[xx][yy], warehouse[ptx][pty]);
            x = xx; y = yy;
            xx = ptx; yy = pty;
        }
    }
    unsigned long long int gpss = 0;
    for (int i = 0; i < n; ++i){
        for (int j = 0; j < m; ++j){
            if (warehouse[i][j] == 'O'){
                gpss += 100 * i + j;
            }
        }
    }
    util::output(gpss);

    // part 2
    int counter = 0;
    for (const auto &line : util::splitline(inp[0])){
        std::string buff;
        for (char c : line){
            buff += part2Extend(c);
        }
        warehouse[counter++] = buff;
    }
    x = idx / (m + 1);
    y = (idx % (m + 1)) * 2;
    m *= 2;
    warehouse[x][y] = '.';

    for (char c : inst){
        auto [dx, dy] = getDirs(c);
        std::vector<int> moveSt;
        std::queue<int> toMove;
        toMove.push(x * m + y);
        std::vector<bool> willMove(n * m, false);
        while (!toMove.empty()){
            int idx = toMove.front();
            toMove.pop();
            if (willMove[idx]){
                continue;
            }
            willMove[idx] = true;
            moveSt.push_back(idx);
            int xx = idx / m, yy = idx % m;
            int newX = xx + dx, newY = yy + dy;
            char obs = warehouse[newX][newY];
            if (obs == '#'){
                moveSt.clear();
                break;
            }
            if (obs == '.'){
                continue;
            }
            toMove.push(newX * m + newY);
            if (dx != 0){
                int otherX = newX, otherY = newY + (obs == '[' ? 1 : -1);
                toMove.push(otherX * m + otherY);
            }
        }
        while (!moveSt.empty()){
            int idx = moveSt.back();
            moveSt.pop_back();
            int xx = idx / m, yy = idx % m;
            x = xx + dx; y = yy + dy;
            std::swap(warehouse[x][y], warehouse[xx][yy]);
        }
    }
    gpss = 0;
    for (int i = 0; i < n; ++i){
        for (int j = 0; j < m; ++j){
            if (warehouse[i][j] == '['){
                gpss += 100 * i + j;
            }
        }
    }
    util::output(gpss);

    return 0;
}
