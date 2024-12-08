#include <sstream>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include "..\util.h"

int main(int, char**){
    std::stringstream inpStream;
    util::getInput(2024, 8, inpStream);
    std::vector<std::string> nodeMap(util::splitline(inpStream));
    int n = nodeMap.size(), m = nodeMap[0].size();
    std::unordered_map<char, std::vector<int>> nodeDict;
    for (int i = 0; i < n; ++i){
        for (int j = 0; j < m; ++j){
            if (nodeMap[i][j] == '.'){
                continue;
            }
            nodeDict[nodeMap[i][j]].push_back(i * m + j);
        }
    }

    // part 1
    std::unordered_set<int> anodes;
    for (auto &pr : nodeDict){
        const auto &v = pr.second;
        int l = v.size();
        for  (int i = 0; i < l - 1; ++i){
            for (int j = i + 1; j < l; ++j){
                int xi = v[i] / m, xj = v[j] / m, yi = v[i] % m, yj = v[j] % m;
                if (util::in2DRange(2 * xi - xj, 2 * yi - yj, n, m)){
                    anodes.insert(2 * v[i] - v[j]);
                }
                if (util::in2DRange(2 * xj - xi, 2 * yj - yi, n, m)){
                    anodes.insert(2 * v[j] - v[i]);
                }
            }
        }
    }
    util::output(anodes.size());

    // part 2

    anodes.clear();
    for (auto &pr : nodeDict){
        const auto &v = pr.second;
        int l = v.size();
        for  (int i = 0; i < l - 1; ++i){
            for (int j = i + 1; j < l; ++j){
                anodes.insert(v[i]);
                int xi = v[i] / m, xj = v[j] / m, yi = v[i] % m, yj = v[j] % m;
                int xx = xi, yy = yi, xdelta = xj - xi, ydelta = yj - yi;
                while (util::in2DRange(xx, yy, n, m)){
                    anodes.insert(xx * m + yy);
                    xx += xdelta;
                    yy += ydelta;
                }
                xx = xi;
                yy = yi;
                while (util::in2DRange(xx, yy, n, m)){
                    anodes.insert(xx * m + yy);
                    xx -= xdelta;
                    yy -= ydelta;
                }
            }
        }
    }
    util::output(anodes.size());
    return 0;
}
