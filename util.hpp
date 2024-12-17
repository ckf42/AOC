#ifndef AOC_UTIL_HPP
#define AOC_UTIL_HPP

#include <filesystem>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace util{

inline void getInput(int year, int day, std::stringstream &outputStream){
    const std::string inputFilePath = "../" + std::to_string(year) + "/input" + std::to_string(day);
    if (!std::filesystem::exists(inputFilePath)){
        throw std::runtime_error("Input file not found: " + inputFilePath.substr(3));
    }
    std::ifstream inputFile(inputFilePath);
    if (!inputFile){
        throw std::runtime_error("Unable to read input file: " + inputFilePath.substr(3));
    }
    outputStream << inputFile.rdbuf();
}

inline std::string getInput(int year, int day){
    std::stringstream ss;
    getInput(year, day, ss);
    return ss.str();
}

inline void splitline(std::stringstream &inputStream, std::stringstream &outputStream){
    std::string buff;
    while (std::getline(inputStream, buff, '\n')){
        if (buff.size() == 0){
            continue;
        }
        outputStream << buff;
    }
}

inline std::vector<std::string> splitline(std::stringstream &inputStream){
    std::vector<std::string> res;
    std::string buff;
    while (std::getline(inputStream, buff, '\n')){
        if (buff.size() == 0){
            continue;
        }
        res.push_back(buff);
    }
    return res;
}

inline std::vector<std::string> splitline(
        const std::string &s,
        const std::string &sepChars = "\n\r"
        ){
    std::vector<std::string> res;
    auto n = s.size();
    decltype(n) ptr = 0, idx;
    while (ptr != n){
        ptr = s.find_first_not_of(sepChars, ptr);
        if (ptr == std::string::npos){
            break;
        }
        idx = s.find_first_of(sepChars, ptr);
        if (idx == std::string::npos){
            idx = n;
        }
        res.push_back(s.substr(ptr, idx - ptr));
        ptr = idx;
    }
    return res;
}

inline std::vector<std::string> split(
        const std::string &s,
        const std::string &sep = "\n"
        ){
    std::vector<std::string> res;
    auto n = s.size(), l = sep.size();
    decltype(n) ptr = 0, idx;
    while (ptr < n){
        idx = s.find(sep, ptr);
        if (idx == std::string::npos){
            idx = n;
        }
        res.push_back(s.substr(ptr, idx - ptr));
        ptr = idx + (idx != n ? l : 0);
    }
    return res;
}

inline std::vector<std::string> string_extract_of(
        const std::string &s,
        const std::string &takeChars
        ){
    std::vector<std::string> res;
    auto n = s.size();
    decltype(n) ptr = 0, idx;
    while (ptr != n){
        ptr = s.find_first_of(takeChars, ptr);
        if (ptr == std::string::npos){
            break;
        }
        idx = s.find_first_not_of(takeChars, ptr);
        if (idx == std::string::npos){
            idx = n;
        }
        res.push_back(s.substr(ptr, idx - ptr));
        ptr = idx;
    }
    return res;
}

template <class T = int>
inline std::vector<T> getInts(std::stringstream &inputStream){
    std::vector<T> res;
    T buff;
    while (inputStream >> buff){
        res.push_back(buff);
    }
    return res;
}

template <class T = int>
inline std::vector<T> getInts(const std::string &s){
    std::stringstream ss(s);
    return getInts<T>(ss);
}

template <class T = int>
inline std::vector<std::vector<T>> getInts(const std::vector<std::string> &lines){
    std::vector<std::vector<T>> res;
    for (const std::string &line : lines){
        res.push_back(getInts<T>(line));
    }
    return res;
}

inline std::vector<int> extract_int(const std::string &s){
    std::vector<int> res;
    for (const std::string &digitSeq : string_extract_of(s, "-0123456789")){
        res.push_back(std::stoi(digitSeq));
    }
    return res;
}

inline bool inRange(int x, int s, int e){
    return x >= s && x < e;
}

inline bool in2DRange(int x, int y, int ex, int ey){
    return inRange(x, 0, ex) && inRange(y, 0, ey);
}
inline bool in2DRange(const std::pair<int, int> &x, int ex, int ey){
    return in2DRange(x.first, x.second, ex, ey);
}
inline bool in2DRange(int x, int y, int sx, int ex, int sy, int ey){
    return inRange(x, sx, ex) && inRange(y, sy, ey);
}
inline bool in2DRange(const std::pair<int, int> &x, int sx, int ex, int sy, int ey){
    return in2DRange(x.first, x.second, sx, ex, sy, ey);
}

// starting from downward, then rotate anticlockwise
constexpr int FOUR_DIRECTIONS[4][2] = {
    {1, 0}, {0, 1}, {-1, 0}, {0, -1}
};
constexpr int EIGHT_DIRECTIONS[8][2] = {
    {1, 0}, {1, 1}, {0, 1}, {-1, 1},
    {-1, 0}, {-1, -1}, {0, -1}, {1, -1}
};
constexpr int DIAG_DIRECTIONS[4][2] = {
    {1, 1}, {-1, 1}, {-1, -1}, {1, -1}
};

template <class T>
inline std::vector<std::pair<T, T>> neighbourGridPoint(
        T x, T y,
        T sx, T ex, T sy, T ey,
        bool isFourDir = true
        ){
    std::vector<std::pair<T, T>> res;
    T xx, yy;
    // TODO: can these two branches be merged into one?
    if (isFourDir){
        for (const auto &offset : FOUR_DIRECTIONS){
            xx = x + static_cast<T>(offset[0]);
            yy = y + static_cast<T>(offset[1]);
            if (util::in2DRange(xx, yy, sx, ex, sy, ey)){
                res.push_back({xx, yy});
            }
        }
    } else {
        for (const auto &offset : EIGHT_DIRECTIONS){
            xx = x + static_cast<T>(offset[0]);
            yy = y + static_cast<T>(offset[1]);
            if (util::in2DRange(xx, yy, sx, ex, sy, ey)){
                res.push_back({xx, yy});
            }
        }
    }
    return res;
}
template <class T>
inline std::vector<std::pair<T, T>> neighbourGridPoint(
        T x, T y,
        T ex, T ey,
        bool isFourDir = true
        ){
    return neighbourGridPoint<T>(x, y, 0, ex, 0, ey, isFourDir);
}

// C++20 comp
template <class T, class Container>
inline bool contains(const T &x, const Container &container){
    return container.find(x) != container.end();
}

template <class Key, class T>
inline const T& getWithDefault(
        const Key &key,
        const std::unordered_map<Key, T> &umap,
        const T &defaultVal
        ){
    auto it = umap.find(key);
    if (it == umap.end()){
        return defaultVal;
    } else {
        return it->second;
    }
}

template <class T, class U>
inline void extendVec(std::vector<T> &target, const std::vector<U> &src){
    target.reserve(target.size() + src.size());
    target.insert(target.end(), src.cbegin(), src.cend());
}

template <class Arg, class... Args>
inline void output(const Arg &x, const Args &... y){
    std::cout << x;
    ((std::cout << ", " << y), ...);
    std::cout << std::endl;
}

template <class T>
inline void printVec(const std::vector<T> &vec, const std::string &sep = ", "){
    using std::to_string;
    auto n = vec.size();
    if (n == 0){
        std::cout << std::endl;
        return;
    }
    std::cout << to_string(vec[0]);
    for (decltype(n) i = 1; i < n; ++i){
        std::cout << sep << to_string(vec[i]);
    }
    std::cout << std::endl;
}

inline void print2DStr(const std::vector<std::string> &vec){
    for (const std::string &s : vec){
        std::cout << s << std::endl;
    }
}

template <class T>
inline void printVec(const T *begin, const T *end, const std::string &sep = ", "){
    using std::to_string;
    std::cout << to_string(*(begin++));
    while (begin != end){
        std::cout << sep << to_string(*(begin++));
    }
    std::cout << std::endl;
}

template <class ResType, class Container>
inline ResType sum(const Container &vec, ResType init = ResType()){
    for (const auto &x : vec){
        init += static_cast<ResType>(x);
    }
    return init;
}

template <class T>
inline std::string joinStr(
        const std::vector<T> &vec,
        const std::string &sep = ", "
        ){
    using std::to_string;
    auto n = vec.size();
    std::string res;
    if (n == 0){
        return res;
    }
    res += to_string(vec[0]);
    for (decltype(n) i = 1; i < n; ++i){
        res += sep;
        res += to_string(vec[i]);
    }
    return res;
}
template <>
inline std::string joinStr(
        const std::vector<std::string> &vec,
        const std::string &sep
        ){
    auto n = vec.size();
    std::string res;
    if (n == 0){
        return res;
    }
    res += vec[0];
    for (decltype(n) i = 1; i < n; ++i){
        res += sep;
        res += vec[i];
    }
    return res;
}

};  // namespace util

#endif
