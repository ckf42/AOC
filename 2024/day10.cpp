#include <string>
#include <unordered_set>
#include <vector>

#include "../util.hpp"

int main(int, char**){
    std::vector<std::string> hikemap = util::splitline(util::getInput(2024, 10));
    int n = hikemap.size(), m = hikemap[0].size();

    // part 1
    std::vector<std::unordered_set<int>> reach(n * m);
    int counter = 0;
    std::vector<int> st;
    for (int i = 0; i < n; ++i){
        for (int j = 0; j < m; ++j){
            if (hikemap[i][j] == '9'){
                st.push_back((counter++ * n + i) * m + j);
            }
        }
    }
    while (!st.empty()){
        int item = st.back();
        st.pop_back();
        int j = item % m;
        item /= m;
        int idx = item / n, i = item % n;
        for (const auto &pt : util::neighbourGridPoint(i, j, n, m)){
            auto [ii, jj] = pt;
            if (util::in2DRange(ii, jj, n, m) 
                    && hikemap[ii][jj] == hikemap[i][j] - 1
                    && !util::contains(idx, reach[ii * m + jj])){
                reach[ii * m + jj].insert(idx);
                st.push_back((idx * n + ii) * m + jj);
            }
        }
    }
    int res = 0;
    for (int i = 0; i < n; ++i){
        for (int j = 0; j < m; ++j){
            if (hikemap[i][j] == '0'){
                res += reach[i * m + j].size();
            }
        }
    }
    util::output(res);

    // part 2
    st.clear();
    for (int i = 0; i < n; ++i){
        for (int j = 0; j < m; ++j){
            if (hikemap[i][j] == '9'){
                st.push_back(i * m + j);
            }
        }
    }
    res = 0;
    while (!st.empty()){
        int coor = st.back();
        st.pop_back();
        int i = coor / m, j = coor % m;
        if (hikemap[i][j] == '0'){
            ++res;
            continue;
        }
        for (const auto &pt : util::neighbourGridPoint(i, j, n, m)){
            auto [ii, jj] = pt;
            if (util::in2DRange(ii, jj, n, m) && hikemap[ii][jj] == hikemap[i][j] - 1){
                st.push_back(ii * m + jj);
            }
        }
    }
    util::output(res);



    return 0;
}
