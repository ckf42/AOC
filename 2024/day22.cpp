#include <algorithm>
#include <string>
#include <vector>
#include <array>
#include <bitset>

#include "../util.hpp"

inline int getNextSecret(int x){
    x = ((x ^ (x << 6)) & 0xffffff);
    x = ((x ^ (x >> 5)) & 0xffffff);
    x = ((x ^ (x << 11)) & 0xffffff);
    return x;
}

constexpr int M = 19 * 19 * 19;
constexpr int N = M * 19;

int main(int, char**){
    std::vector<int> initSecrets = util::getInts(util::getInput(2024, 22));
    unsigned long long int part1Sum = 0;
    std::array<int, N> totalCounter;
    totalCounter.fill(0);
    for (int s : initSecrets){
        std::bitset<N> seen;
        int coor = 0, oldPrice = s % 10;
        for (int c = 1; c <= 2000; ++c){
            int ss = getNextSecret(s);
            int price = ss % 10;
            coor = coor / 19 + (price - oldPrice + 9) * M;
            if (c >= 4 && !seen[coor]){
                seen[coor] = true;
                totalCounter[coor] += price;
            }
            oldPrice = price;
            s = ss;
        }
        part1Sum += s;
    }
    util::output(part1Sum);
    int maxval = *std::max_element(totalCounter.cbegin(), totalCounter.cend());
    util::output(maxval);

    return 0;
}
