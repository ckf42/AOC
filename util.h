#ifndef AOC_UTIL_H
#define AOC_UTIL_H

#include <filesystem>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
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
        outputStream << buff;
    }
}

inline std::vector<std::string> splitline(std::stringstream &inputStream){
    std::vector<std::string> res;
    std::string buff;
    while (std::getline(inputStream, buff, '\n')){
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

inline bool inRange(int x, int a, int b){
    return x >= a && x < b;
}

};  // namespace util

#endif
