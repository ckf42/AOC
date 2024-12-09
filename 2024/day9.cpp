#include <string>
#include <vector>

#include "../util.h"

using ulli = unsigned long long int;

int main(int, char**){
    std::string inp = util::getInput(2024, 9);
    while (inp.back() == '\n'){
        inp.pop_back();
    }
    int n = inp.size();
    std::vector<short> blocks(n, 0);
    for (int i = 0; i < n; ++i){
        blocks[i] = inp[i] - '0';
    }

    // part 1
    ulli checksum = 0;
    ulli blankPtr = 1, dataPtr = n - 1;
    ulli dataId = dataPtr / 2, currOffset = blocks[0];
    while (blankPtr < dataPtr){
        ulli blkToMove = std::min(blocks[blankPtr], blocks[dataPtr]);
        checksum += dataId * (currOffset * 2 + blkToMove - 1) * blkToMove / 2;
        currOffset += blkToMove;
        blocks[blankPtr] -= blkToMove;
        blocks[dataPtr] -= blkToMove;
        if (blocks[blankPtr] == 0){
            ++blankPtr;
            ulli blklen = blocks[blankPtr];
            checksum += (blankPtr / 2) * (currOffset * 2 + blklen - 1) * blklen / 2;
            currOffset += blklen;
            ++blankPtr;
        }
        if (blocks[dataPtr] == 0){
            --dataId;
            ----dataPtr;
        }
    }
    util::output(checksum);

    // part 2
    for (int i = 0; i < n; ++i){
        blocks[i] = inp[i] - '0';
    }
    std::vector<int> data((n + 1) / 2, 0), blank(n / 2);
    std::vector<int> dataOffset((n + 1) / 2, 0), blankOffset(n / 2);
    checksum = 0;
    currOffset = 0;
    ulli ptr = 0; 
    for (; ptr < blankOffset.size(); ++ptr){
        data[ptr] = blocks[ptr * 2];
        blank[ptr] = blocks[ptr * 2 + 1];
        checksum += ptr * (currOffset * 2 + data[ptr] - 1) * data[ptr] / 2;
        dataOffset[ptr] = currOffset;
        currOffset += data[ptr];
        blankOffset[ptr] = currOffset;
        currOffset += blank[ptr];
    }
    dataOffset.back() = blankOffset.back() + blank.back();
    data.back() = blocks.back();
    checksum += blank.size() * (currOffset * 2 + data.back() - 1) * data.back() / 2;
    for (ptr = blank.size(); ptr > 0; --ptr){
        ulli idx = 0;
        for (; idx < ptr; ++idx){
            if (blank[idx] >= data[ptr]){
                break;
            }
        }
        if (idx != ptr){
            checksum -= ptr * data[ptr] * (dataOffset[ptr] - blankOffset[idx]);
            blank[idx] -= data[ptr];
            blankOffset[idx] += data[ptr];
        }
    }
    util::output(checksum);

    return 0;
}
