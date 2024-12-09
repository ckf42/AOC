#ifndef AOC_UTIL_H
#define AOC_UTIL_H

#include <filesystem>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
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

inline std::vector<int> getInts(std::stringstream &inputStream){
    std::vector<int> res;
    int buff;
    while (inputStream >> buff){
        res.push_back(buff);
    }
    return res;
}

inline std::vector<int> getInts(const std::string &s){
    std::stringstream ss(s);
    return getInts(ss);
}

inline std::vector<std::vector<int>> getInts(const std::vector<std::string> &lines){
    std::vector<std::vector<int>> res;
    for (const auto &line : lines){
        res.push_back(getInts(line));
    }
    return res;
}

inline bool inRange(int x, int a, int b){
    return x >= a && x < b;
}

inline bool in2DRange(int x, int y, int a, int b){
    return inRange(x, 0, a) && inRange(y, 0, b);
}
inline bool in2DRange(const std::pair<int, int> &x, int a, int b){
    return in2DRange(x.first, x.second, a, b);
}

// C++20 comp
template <class T, class Container>
inline bool contains(const T &x, const Container &container){
    return container.find(x) != container.end();
}

template <class T, class U>
inline void extendVec(std::vector<T> &target, const std::vector<U> &src){
    target.reserve(target.size() + src.size());
    target.insert(target.end(), src.cbegin(), src.cend());
}

template <class T>
inline void output(const T &x){
    std::cout << x << std::endl;
}

template <class T>
inline void printVec(const std::vector<T> &vec, const std::string &sep = ", "){
    int n = vec.size();
    std::cout << std::to_string(vec[0]);
    for (int i = 1; i < n; ++i){
        std::cout << sep << std::to_string(vec[i]);
    }
    std::cout << std::endl;
}

};  // namespace util

#endif
