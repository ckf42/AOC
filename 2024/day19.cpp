#include <array>
#include <string>
#include <unordered_map>
#include <vector>

#include "../util.hpp"

using ulli = unsigned long long int;

struct TrieNode {
    bool hasItem;
    std::array<int, 26> child;
    
    TrieNode(): hasItem(false), child() {}
};

int main(int, char**){
    std::vector<std::string> inp = util::split(util::getInput(2024, 19), "\n\n");
    std::vector<std::string> designs = util::splitline(inp[1]);
    std::vector<TrieNode> trie(1);
    for (const std::string &patt : util::split(inp[0], ", ")){
        int ptr = 0;
        for (char c : patt){
            if (trie[ptr].child[c - 'a'] == 0){
                trie[ptr].child[c - 'a'] = trie.size();
                trie.push_back(TrieNode());
            }
            ptr = trie[ptr].child[c - 'a'];
        }
        trie[ptr].hasItem = true;
    }

    ulli part1 = 0, part2 = 0;
    for (const std::string &design : designs){
        std::unordered_map<int, ulli> buff, newBuff;
        buff[0] = 1;
        for (char c : design){
            newBuff.clear();
            for (auto [ptr, freq] : buff){
                int newPtr = trie[ptr].child[c - 'a'];
                if (newPtr != 0){
                    newBuff[newPtr] += freq;
                    if (trie[newPtr].hasItem){
                        newBuff[0] += freq;
                    }
                }
            }
            std::swap(buff, newBuff);
        }
        part1 += util::contains(0, buff);
        part2 += buff[0];
    }
    util::output(part1);
    util::output(part2);

    return 0;
}
