#include "../util.hpp"

using lli = long long int;

constexpr lli offset = 10000000000000;

int main(int, char**){
    std::vector<std::string> machineSpecs = util::split(util::getInput(2024, 13), "\n\n");
    lli part1Res = 0, part2Res = 0;
    for (const std::string &spec : machineSpecs){
        std::vector<int> nums = util::extract_int(spec);
        lli det = nums[0] * nums[3] - nums[1] * nums[2];
        lli e = nums[4], f = nums[5];
        lli x = nums[3] * e - nums[2] * f,
            y = nums[0] * f - nums[1] * e,
            xx = nums[3] * (e + offset) - nums[2] * (f + offset),
            yy = nums[0] * (f + offset) - nums[1] * (e + offset);
        if (det < 0){
            det = -det;
            x = -x; y = -y;
            xx = -xx; yy = -yy;
        }
        if (x >= 0 && y >= 0 && x % det == 0 && y % det == 0){
            part1Res += 3 * (x / det) + y / det;
        }
        if (xx >= 0 && yy >= 0 && xx % det == 0 && yy % det == 0){
            part2Res += 3 * (xx / det) + yy / det;
        }
    }
    util::output(part1Res);
    util::output(part2Res);

    return 0;
}
