#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include "../util.hpp"

using ulli = unsigned long long int;
using seti = std::unordered_set<int>;

int main(int, char**){
    std::unordered_map<int, std::vector<int>> edges;
    std::unordered_map<std::string, int> nodeIndex;
    std::vector<std::string> nodeNames;
    for (const std::string &line : util::splitline(util::getInput(2024, 23))){
        int idx = line.find('-');
        std::string a = line.substr(0, idx);
        int aIdx = util::getWithDefault(a, nodeIndex, static_cast<int>(nodeNames.size()));
        if (aIdx == nodeNames.size()){
            nodeIndex[a] = aIdx;
            nodeNames.push_back(a);
        }
        std::string b = line.substr(idx + 1);
        int bIdx = util::getWithDefault(b, nodeIndex, static_cast<int>(nodeNames.size()));
        if (bIdx == nodeNames.size()){
            nodeIndex[b] = bIdx;
            nodeNames.push_back(b);
        }
        edges[aIdx].push_back(bIdx);
        edges[bIdx].push_back(aIdx);
    }
    int N = nodeNames.size();

    // part 1
    std::unordered_set<ulli> cliques;
    for (int i = 0; i < N; ++i){
        if (nodeNames[i][0] != 't'){
            continue;
        }
        int n = edges[i].size();
        for (int j = 0; j < n; ++j){
            for (int k = j + 1; k < n; ++k){
                int aIdx = i, bIdx = edges[i][j], cIdx = edges[i][k];
                if (util::contains(bIdx, edges[cIdx])){
                    util::orderVars(aIdx, bIdx, cIdx);
                    cliques.insert((static_cast<ulli>(aIdx * N + bIdx) * N + cIdx));
                }
            }
        }
    }
    util::output(cliques.size());

    // part 2
    std::vector<std::tuple<seti, seti, seti>> buff;
    seti p, x;
    for (int i = 0; i < N; ++i){
        x.insert(i);
    }
    for (int v = 0; v < N; ++v){
        p.insert(v);
        x.erase(v);
        buff.push_back({
                {v},
                util::setIntersection(p, edges[v]),
                util::setIntersection(x, edges[v])
        });
    }
    seti maxClique;
    while (!buff.empty()){
        auto [rr, pp, xx] = buff.back();
        buff.pop_back();
        if (pp.empty() && xx.empty()){
            if (rr.size() > maxClique.size()){
                std::swap(maxClique, rr);
            }
            continue;
        }
        int pivot = pp.empty() ? *xx.begin() : *pp.begin();
        for (int v : util::setDifference(pp, edges[pivot])){
            buff.push_back({
                    util::setUnion(rr, std::vector<int>{v}),
                    util::setIntersection(pp, edges[v]),
                    util::setIntersection(xx, edges[v])
            });
            pp.erase(v);
            xx.insert(v);
        }
    }
    std::vector<std::string> maxCliqMembers;
    for (int idx : maxClique){
        maxCliqMembers.push_back(nodeNames[idx]);
    }
    std::sort(maxCliqMembers.begin(), maxCliqMembers.end());
    util::printVec(maxCliqMembers, ",");

    return 0;
}
