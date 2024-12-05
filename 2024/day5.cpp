#include <algorithm>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>

#include "../util.h"

bool isCorrOrder(
        const std::vector<int> &sect,
        const std::unordered_map<int, std::unordered_set<int>> &edges){
    int n = sect.size();
    for (int i = 0; i < n - 1; ++i){
        for (int j = i + 1; j < n; ++j){
            auto &node = edges.at(sect[j]);
            if (node.find(sect[i]) != node.end()){
                return false;
            }
        }
    }
    return true;
}

int main(int, char**){
    std::stringstream inpStream;
    util::getInput(2024, 5, inpStream);

    std::unordered_map<int, std::unordered_set<int>> edges;
    std::vector<std::vector<int>> sects;

    std::string buffLine;
    bool allRulesSeen = false;
    while (std::getline(inpStream, buffLine, '\n')){
        if (buffLine == ""){
            allRulesSeen = true;
            continue;
        }
        if (!allRulesSeen){
            size_t idx = buffLine.find('|');
            int a = std::stoi(buffLine.substr(0, idx)), b = std::stoi(buffLine.substr(idx + 1));
            edges[a].insert(b);
            edges[b];
        } else {
            std::vector<int> secNumBuff;
            size_t s = 0, e;
            while (s < buffLine.size()){
                e = buffLine.find(',', s);
                if (e == std::string::npos){
                    e = buffLine.size();
                }
                secNumBuff.push_back(std::stoi(buffLine.substr(s, e - s)));
                s = e + 1;
            }
            sects.push_back(secNumBuff);
        }
    }

    // part 1
    int count = 0, n = sects.size();
    std::vector<bool> corrState(n, false);
    for (int i = 0; i < n; ++i){
        if (isCorrOrder(sects[i], edges)){
            corrState[i] = true;
        }
        if (corrState[i]){
            count += sects[i][sects[i].size() / 2];
        }
    }
    std::cout << count << std::endl;

    // part 1
    count = 0;
    for (int i = 0; i < n; ++i){
        if (corrState[i]){
            continue;
        }
        std::sort(
                sects[i].begin(), sects[i].end(), 
                [&edges](int a, int b){return edges[a].find(b) != edges[a].end();});
        count += sects[i][sects[i].size() / 2];
    }
    std::cout << count << std::endl;

    return 0;
}
