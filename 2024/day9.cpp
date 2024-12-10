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
    std::vector<ulli> offsets(n, 0);
    currOffset = 0;
    checksum = 0;
    for (int i = 0; i < n; ++i){
        blocks[i] = inp[i] - '0';
        if ((i ^ 1) & 1){
            checksum += (i / 2) * (currOffset * 2 + blocks[i] - 1) * blocks[i] / 2;
        }
        offsets[i] = currOffset;
        currOffset += blocks[i];
    }
    for (int i = n - 1; i >= 2; i -= 2){
        int idx = 1;
        for (; idx < i; idx += 2){
            if (blocks[idx] >= blocks[i]){
                break;
            }
        }
        if (idx < i){
            checksum -= (i / 2) * blocks[i] * (offsets[i] - offsets[idx]);
            blocks[idx] -= blocks[i];
            offsets[idx] += blocks[i];
        }
    }
    util::output(checksum);

    return 0;
}
