#include <string>
#include <vector>
#include <unordered_map>

#include "../util.hpp"

inline int getNextSecret(int x){
    x = ((x ^ (x << 6)) & 0xffffff);
    x = ((x ^ (x >> 5)) & 0xffffff);
    x = ((x ^ (x << 11)) & 0xffffff);
    return x;
}

int main(int, char**){
    std::vector<int> initSecrets = util::getInts(util::getInput(2024, 22));
    unsigned long long int part1Sum = 0;
    std::unordered_map<int, int> totalCounter, counter;
    for (int s : initSecrets){
        counter.clear();
        int coor = 0, oldPrice = s % 10;
        for (int c = 1; c <= 2000; ++c){
            int ss = getNextSecret(s);
            int price = ss % 10;
            coor = coor / 19 + (price - oldPrice + 9) * 6859;  // 19 ** 3 == 6859
            if (c >= 4 && !util::contains(coor, counter)){
                counter[coor] = price;
            }
            oldPrice = price;
            s = ss;
        }
        part1Sum += s;
        for (auto [coor, val] : counter){
            totalCounter[coor] += val;
        }
    }
    util::output(part1Sum);
    int maxval = -1;
    for (auto [coor, val] : totalCounter){
        if (val > maxval){
            maxval = val;
        }
    }
    util::output(maxval);

    return 0;
}
